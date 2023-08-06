import datetime
import time
from contextlib import contextmanager
import logging
import functools
# from async_generator import asynccontextmanager

# https://stackoverflow.com/questions/37433157/asynchronous-context-manager


@contextmanager
def util_logger_context(fn_logger, prefix='test', width=80, fill=" "):
    try:
        now = time.time()
        yield
    finally:
        end = time.time()
        fn_logger('{}: cost {}s'.format(prefix, (end - now)).center(width, fill))


@contextmanager
def util_logger_statment_context(logger, msg='', method='info', width=80, fill="=", add_new_line=True):
    getattr(logger, method)("start {}".format(msg).center(width, fill))
    if add_new_line:
        getattr(logger, method)("")
    try:
        yield
    finally:
        if add_new_line:
            getattr(logger, method)("")
        getattr(logger, method)("end {}".format(msg).center(width, fill))


def prefix_concat(prefix1, prefix2):
    def prefix_to_str(prefix):
        if callable(prefix):
            return prefix()
        return prefix

    def _prefix():
        str1 = prefix_to_str(prefix1)
        str2 = prefix_to_str(prefix2)
        try:
            return str1 + str2
        except TypeError as e:
            raise TypeError("str1:{}, str2:{}, {}, prefix1:{}, prefix2:{}, callable:{}".format(str1, str2, e, prefix1, prefix2, callable(prefix2)))

        # return prefix_to_str(prefix1) + prefix_to_str(prefix2)
    return _prefix


class LoggerMultiLineLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger, enable=None):
        # super(LoggerAdapter, self).__init__(logger, {})
        if isinstance(prefix, (str, bytes)):
            def _new_prefix(val):
                # 没有这个val的话，会造成无线递归
                return val
            prefix = functools.partial(_new_prefix, prefix)
        local_prefix = ''
        # enable = True
        if isinstance(logger, LoggerMultiLineLoggerAdapter):
            local_prefix, logger, enable = logger._prefix, logger.logger, logger._enable
        local_prefix = prefix_concat(local_prefix, prefix)
        if enable is None:
            enable = True
        # return cls(prefix, logger, enable=enable)
        super().__init__(logger, {})
        self._prefix = local_prefix
        self._enable = enable

    def get_prefix(self):
        if isinstance(self._prefix, str):
            return self._prefix
        if callable(self._prefix):
            return self._prefix()
        raise TypeError("unsupported prefix error  {}".format(type(self._prefix)))

    def process(self, msg, kwargs):
        lines = msg.splitlines()
        lines = ['[%s] %s' % (self.get_prefix(), e) for e in lines]
        return lines, kwargs
        # return '[%s] %s' % (self.prefix, msg), kwargs

    def log(self, level, msg, *args, **kwargs):
        """
        Delegate a log call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        if self.isEnabledFor(level) and self._enable:
            msg, kwargs = self.process(msg, kwargs)
            if isinstance(msg, (list, tuple)):
                pass
            else:
                msg = [msg]
            for line in msg:
                self.logger.log(level, line, *args, **kwargs)

    @classmethod
    def add_datetime_to_logger(cls, logger, date_format, prefix=''):
        def prefix_func():
            return '{}{}'.format(prefix, datetime.datetime.now().strftime(date_format))
        return cls(prefix_func, logger)

    @classmethod
    def create_from_logger(cls, prefix, logger):
        return cls(prefix, logger)
        # local_prefix = ''
        # enable = True
        # if isinstance(logger, cls):
        #     local_prefix, logger, enable = logger._prefix, logger.logger, logger._enable
        # local_prefix += prefix
        # return cls(prefix, logger, enable=enable)
