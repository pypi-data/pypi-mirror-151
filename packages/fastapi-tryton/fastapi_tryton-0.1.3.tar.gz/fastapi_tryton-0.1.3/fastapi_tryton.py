# This file is part of fastapi_tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import ast
from functools import wraps
import contextvars

import logging
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseSettings
from typing import Optional

from trytond.config import config
from trytond.exceptions import UserError, UserWarning, ConcurrencyException

__all__ = ['Tryton']

# init our logger
logger = logging.getLogger("uvicorn.error")
logger.info('Starting FastAPI-Tryton....!')

database_retry = config.getint('database', 'retry')

global _request
_request = contextvars.ContextVar('_request')


def retry_transaction(retry):
    """Decorator to retry a transaction if failed. The decorated method
    will be run retry times in case of DatabaseOperationalError.
    """
    from trytond import backend
    from trytond.transaction import Transaction
    try:
        DatabaseOperationalError = backend.DatabaseOperationalError
    except AttributeError:
        DatabaseOperationalError = backend.get('DatabaseOperationalError')

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for count in range(retry, -1, -1):
                try:
                    return func(*args, **kwargs)
                except DatabaseOperationalError:
                    if count and not Transaction().readonly:
                        continue
                    raise
        return wrapper
    return decorator


class CustomRequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        _request.set(request)
        response = await call_next(request)
        return response


class Tryton(object):
    "Control the Tryton integration to one or more FastAPI applications."

    def __init__(self, app=None, configure_jinja=False):
        self.context_callback = None
        self.database_retry = None
        self._configure_jinja = configure_jinja
        if app is not None:
            self.init_app(app)
        app.add_middleware(CustomRequestMiddleware)

    def init_app(self, app):
        "Initialize an application for the use with this Tryton setup."
        database = app.settings.tryton_db
        user = app.settings.tryton_user
        configfile = app.settings.tryton_config
        self.database = database
        config.update_etc(configfile)

        from trytond.pool import Pool
        from trytond.transaction import Transaction

        self.database_retry = config.getint('database', 'retry')
        self.pool = Pool(database)
        self.app = app
        with Transaction().start(database, user, readonly=True):
            self.pool.init()

        if not hasattr(app, 'extensions'):
            self.app.extensions = {}

        self.app.extensions['Tryton'] = self
        if self._configure_jinja:
            app.jinja_env.filters.update(
                numberformat=self.format_number,
                dateformat=self.format_date,
                currencyformat=self.format_currency,
                timedeltaformat=self.format_timedelta,
            )

    def _get(self, model):
        "Return a model instance"
        from trytond.pool import Pool
        model = Pool(self.database).get(model)
        return Model(self.database, model)

    def transaction(self, readonly=None, user=None, context=None):
        """Decorator to run inside a Tryton transaction.
        The decorated method could be run multiple times in case of
        database operational error.

        If readonly is None then the transaction will be readonly except for
        PUT, POST, DELETE and PATCH request methods.

        If user is None then tryton_user will be used.

        readonly, user and context can also be callable.
        """
        from trytond import backend
        from trytond.cache import Cache
        from trytond.transaction import Transaction

        request = _request.get()
        try:
            DatabaseOperationalError = backend.DatabaseOperationalError
        except AttributeError:
            DatabaseOperationalError = backend.get('DatabaseOperationalError')

        def get_value(value):
            return value() if callable(value) else value

        def instanciate(value):
            if isinstance(value, _BaseProxy):
                return value()
            return value

        def decorator(func):
            @retry_transaction(self.database_retry)
            @wraps(func)
            def wrapper(*args, **kwargs):
                tryton = self.app.extensions['Tryton']
                database = self.app.settings.tryton_db
                if user is None and self.app.settings.tryton_user:
                    transaction_user = get_value(
                        int(self.app.settings.tryton_user)
                    )
                else:
                    transaction_user = get_value(user)

                if readonly is None:
                    is_readonly = tryton._readonly(request)
                else:
                    is_readonly = get_value(readonly)

                transaction_context = {}
                if tryton.context_callback or context:
                    with Transaction().start(database, transaction_user,
                            readonly=True):
                        if tryton.context_callback:
                            transaction_context = tryton.context_callback()
                        transaction_context.update(get_value(context) or {})

                # FIXME
                # is_secure: False
                host, port = request.scope['server']
                transaction_context.setdefault('_request', {}).update({
                    'remote_addr': request.client.host,
                    'http_host': ":".join([host, str(port)]),
                    'scheme': request.url.scheme,
                    'is_secure': False,
                })

                with Transaction().start(database, transaction_user,
                        readonly=is_readonly,
                        context=transaction_context) as transaction:
                    try:
                        result = func(*map(instanciate, args),
                            **dict((n, instanciate(v))
                                for n, v in kwargs.items()))
                        if hasattr(transaction, 'cursor') and not is_readonly:
                            transaction.cursor.commit()
                    except DatabaseOperationalError:
                        raise
                    except Exception as e:
                        if isinstance(e, (
                                    UserError,
                                    UserWarning,
                                    ConcurrencyException)):
                            raise HTTPException(status_code=404, detail=e.message)
                        raise

                from trytond.worker import run_task
                while transaction.tasks:
                    task_id = transaction.tasks.pop()
                    run_task(tryton.pool, task_id)
                return result
            return wrapper
        return decorator

    def default_context(self, callback):
        "Set the callback for the default transaction context"
        self.context_callback = callback
        return callback

    @property
    def language(self):
        "Return a language instance for the current request"
        from trytond.transaction import Transaction
        Lang = self.pool.get('ir.lang')
        # Do not use Transaction.language as it fallbacks to default language
        language = Transaction().context.get('language')
        if not language:
            #     language = request.accept_languages.best_match(
            #         Lang.get_translatable_languages())
            pass

        #FIXME: add multiple languages
        lang = Lang.get('en')
        return lang

    def format_date(self, value, lang=None, *args, **kwargs):
        from trytond.report import Report
        if lang is None:
            lang = self.language
        return Report.format_date(value, lang, *args, **kwargs)

    def format_number(self, value, lang=None, *args, **kwargs):
        from trytond.report import Report
        if lang is None:
            lang = self.language
        return Report.format_number(value, lang, *args, **kwargs)

    def format_currency(self, value, currency, lang=None, *args, **kwargs):
        from trytond.report import Report
        if lang is None:
            lang = self.language
        return Report.format_currency(value, lang, currency, *args, **kwargs)

    def format_timedelta(
            self, value, converter=None, lang=None, *args, **kwargs):
        from trytond.report import Report
        if not hasattr(Report, 'format_timedelta'):
            return str(value)
        if lang is None:
            lang = self.language
        return Report.format_timedelta(
            value, converter=converter, lang=lang, *args, **kwargs)

    def _readonly(self, request):
        return not (request
            and request.method in ('PUT', 'POST', 'DELETE', 'PATCH'))


class Model(object):

    def __init__(self, db, model):
        self.db = db
        self.model = model

    def is_readonly(self, request):
        return not (request and request.method in (
            'PUT', 'POST', 'DELETE', 'PATCH'))

    def in_transaction(func):
        "Execute transaction inside a context"

        def instanciate(value):
            if isinstance(value, _BaseProxy):
                return value()
            return value

        def wrapper(*args, **kwargs):
            from trytond.backend import DatabaseOperationalError
            from trytond.transaction import Transaction

            model, _args = args
            request = _request.get()
            host, port = request.scope['server']
            print( ' ------------ ', _args)
            ctx = _args.pop('context', {})
            # field_names = _args.pop('field_names', [])
            user = ctx.get('user', None)
            ctx.setdefault('_request', {}).update({
                'remote_addr': request.client.host,
                'http_host': ":".join([host, str(port)]),
                'scheme': request.url.scheme,
                'is_secure': False,
            })
            is_readonly = model.is_readonly(request)
            with Transaction().start(model.db, user=user, context=ctx,
                readonly=is_readonly):
                try:
                    result = func(*map(instanciate, args),
                        **dict((n, instanciate(v))
                            for n, v in kwargs.items()))
                    return result
                except DatabaseOperationalError:
                    raise
                except Exception as e:
                    if isinstance(e, (
                            UserError,
                            UserWarning,
                            ConcurrencyException)):
                        raise HTTPException(status_code=404, detail=e.message)
                    raise
        return wrapper

    @in_transaction
    def search_read(self, args):
        "Return records from method search_read"
        return self.model.search_read(**args)

    @in_transaction
    def search(self, args):
        "Return records from method search"
        """
        Method not implemented yet, sorry.
        But the moment isn't possible returns an instance in one request,
        so because no have sense return search, use search_read instead
        """
        # return self.model.search(**args)
        return []

    @in_transaction
    def browse(self, args):
        "Return records from method browse"
        """
        Method not implemented yet, sorry.
        But the moment isn't possible returns an instance in one request,
        so because no have sense return search, use search_read instead
        """
        ids = args.get('ids')
        fields = args.get('fields_names')
        domain = [('id', 'in', ids)]
        return self.model.search_read(domain, fields_names=fields)

    @in_transaction
    def create(self, args):
        "Create a record in Tryton"
        result = self.model.create([args['record']])
        return [rec.id for rec in result]

    @in_transaction
    def write(self, args):
        "Write a record in Tryton"
        records = self.model.browse(args['ids'])
        _result = self.model.write(records, args['values'])
        return _result

    @in_transaction
    def delete(self, args):
        "Delete a record in Tryton"
        records = self.model.browse(args['ids'])
        _result = self.model.delete(records)
        return _result

    @in_transaction
    def button_method(self, args):
        "Call a button method in model"
        """
        method: method in model
        args: Dict with args of method

        """
        method = getattr(self.model, args.pop('method'))
        records = self.model.browse(args['ids'])
        return method(records)

    @in_transaction
    def method(self, args):
        "Call a method in model"
        """
        method: method in model
        args: Dict with args of method

        """
        res = {}
        method = getattr(self.model, args.pop('method'))
        _args = args.get('args', {})
        _kwargs = args.get('kwargs', {})
        print('args.....', _args)
        print('kwargs.....', _kwargs)
        if _kwargs:
            res = method(**_kwargs)
        else:
            res = method(_args)
        return res

    @in_transaction
    def fields_get(self, args):
        "Call a all fields in model"
        """
        fields_names: fields in model
        """
        res = self.model.fields_get(args['fields_names'])
        return res


class _BaseProxy(object):
    pass


class _RecordsProxy(_BaseProxy):
    def __init__(self, model, ids):
        self.model = model
        self.ids = ids

    def __iter__(self):
        return iter(self.ids)

    def __call__(self):
        tryton = current_app.extensions['Tryton']
        Model = tryton.pool.get(self.model)
        return Model.browse(self.ids)


class _RecordProxy(_RecordsProxy):
    def __init__(self, model, id):
        super(_RecordProxy, self).__init__(model, [id])

    def __int__(self):
        return self.ids[0]

    def __call__(self):
        return super(_RecordProxy, self).__call__()[0]


# class RecordConverter(BaseConverter):
# This need a review
class RecordConverter():
    """This converter accepts record id of model::

        Rule('/page/<record("res.user"):user>')"""
    regex = r'\d+'

    def __init__(self, map, model):
        super(RecordConverter, self).__init__(map)
        self.model = model

    def to_python(self, value):
        return _RecordProxy(self.model, int(value))

    def to_url(self, value):
        return str(int(value))


# class RecordsConverter(BaseConverter):
# This need a review
class RecordsConverter():
    """This converter accepts record ids of model::

        Rule('/page/<records("res.user"):users>')"""
    regex = r'\d+(,\d+)*'

    def __init__(self, map, model):
        super(RecordsConverter, self).__init__(map)
        self.model = model

    def to_python(self, value):
        return _RecordsProxy(self.model, map(int, value.split(',')))

    def to_url(self, value):
        return ','.join(map(str, map(int, value)))


class Settings(BaseSettings):
    tryton_db: str
    tryton_user: Optional[int] = None
    tryton_config: str
