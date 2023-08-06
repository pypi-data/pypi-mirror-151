
import functools
import logging
import os
import threading
from asyncio import iscoroutinefunction
from collections import defaultdict
from inspect import isawaitable
from time import time
from types import MethodType
from typing import Any, Callable, Iterable, Optional

logger = logging.getLogger("lazy_logging")

if os.environ.get("LL_DEBUG", False):
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)


levels_down_the_rabbit_hole = defaultdict(lambda: defaultdict(int))

def iterup():
    levels_down_the_rabbit_hole[os.getpid()][threading.get_ident()] += 1

def iterdown():
    levels_down_the_rabbit_hole[os.getpid()][threading.get_ident()] -= 1


class LazyLoggerFactory:
    """
    Used to quickly create multiple LazyLogger objects with the same key so you can set the level of all of them at once, even if they are separate loggers.
    In the example below, both `logger_a` and `logger_b` will have their logging level set to `logging.DEBUG`
    ```
    import logging, os
    from lazy_name_tbd import LazyLoggerFactory

    myLazyLogger = LazyLoggerFactory('ME')
    logger_a = logging.getLogger("i.am.a.logger")
    logger_b = logging.getLogger("i.am.a.logger.too")

    @myLazyLogger(logger_a)
    def my_function_a():
        return 0

    @myLazyLogger(logger_b)
    def my_function_b():
        return 1
        
    os.environ["LL_LEVEL_ME"] = "DEBUG"
    ```
    """
    def __init__(self, key: str) -> None:
        if not isinstance(key, str):
            TypeError(f"`key` must be an instance of `str`. You passed a(n) {type(key)} type: {key}.")
        self.key = 'LL_LEVEL' if not key else key if key.startswith("LL_LEVEL") else f'LL_LEVEL_{key}'

    def __call__(self, logger: logging.Logger) -> "LazyLogger":
        """ Creates a LazyLogger instance for `logger`. """
        if not isinstance(logger, logging.Logger):
            TypeError(f"`logger` must be an instance of `logging.Logger`. You passed a(n) {type(logger)} type: {logger}.")
        return LazyLogger(logger,self.key)
    
    def __repr__(self) -> str:
        return f"<LazyLoggerFactory key='{self.key}'>"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, LazyLoggerFactory):
            raise TypeError("Can only compare with other LazyLoggerFactory objects.")
        return self.key == __o.key


class LazyLogger:
    """
    Used to decorate functions for lazy logging.
    ```
    import logging
    from lazy_name_tbd import LazyLogger

    logger = logging.getLogger("i.am.a.logger")

    @LazyLogger(logger)
    def my_function():
        return "some value"
    ```
    """
    def __init__(self, logger: logging.Logger = None, key: str = "") -> None:
        if not isinstance(logger, logging.Logger):
            TypeError(f"`logger` must be an instance of `logging.Logger`. You passed a(n) {type(logger)} type: {logger}.")
        if not isinstance(key, str):
            TypeError(f"`key` must be an instance of `str`. You passed a(n) {type(key)} type: {key}.")
        self.logger = logger or logging.getLogger(__name__)
        self.key = 'LL_LEVEL' if not key else key if key.startswith("LL_LEVEL") else f'LL_LEVEL_{key}'
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())

    def __call__(self, func: Callable[...,Any]) -> "LazyLoggerWrapped[...,Any]":
        """
        Wraps a Callable or Awaitable `func` into a LazyLoggerWrapped object using the attributes of `self`.
        """
        if iscoroutinefunction(func):
            wrapped = LazyLoggerWrappedCoroutineFunction(func)
        # async cached property libs will trigger this branch
        elif not callable(func):
            wrapped = LazyLoggerWrappedGettableCoroutineFunction(func)
        else:
            wrapped = LazyLoggerWrappedCallable(func)

        wrapped.logger = self.logger
        wrapped.log_level = self.log_level
        return wrapped

    def __repr__(self) -> str:
        if self.key == "LL_LEVEL":
            return f"<LazyLogger '{self.logger.name}'>"
        return f"<LazyLogger '{self.logger.name}' key='{self.key}'>"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, LazyLogger):
            raise TypeError("Can only compare with other LazyLogger objects.")
        return self.logger == __o.logger and self.key == __o.key
    
    @property
    def log_level(self) -> int:
        return getattr(logging,os.environ[self.key]) if self.key in os.environ else None


class LazyLoggerWrapped:
    logger: logging.Logger
    log_level: Optional[int]

    def __init__(self, func: Callable[...,Any]) -> None:
        self.func = func
        self.func_string = f"{self.func.__module__}.{self.func.__name__}" if self.func.__module__ else self.func.__name__
        functools.update_wrapper(self, self.func)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return MethodType(self, obj)
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, LazyLoggerWrapped):
            raise TypeError("Can only compare with other LazyLoggerWrapped objects.")
        return self.func == __o.func
    
    def pre_execution(self, *args: Any, **kwargs: Any) -> None:
        if self.log_level is not None:
            self.logger.setLevel(self.log_level)
        self.logger.debug(f'Fetching {self.describer_string(*args,**kwargs)}...')
        iterup()
    
    def post_execution(self, start: float, return_value: Any, *args: Any, **kwargs: Any) -> None:
        iterdown()
        self.logger.debug(f'{self.describer_string(*args,**kwargs)} returns: {return_value}')
        self.record_duration(start, self.describer_string(*args,**kwargs))
    
    @property
    def spacing(self) -> str:
        return '  ' * levels_down_the_rabbit_hole[os.getpid()][threading.get_ident()]

    def describer_string(self, *args: Any, **kwargs: Any) -> str:
        if args:
            args = str(tuple([*args]))[1:-1]
            if args.endswith(','):
                args = args[:-1]
        if kwargs:
            kwargs = "".join(f"{kwarg}={value}," for kwarg, value in kwargs.items())[:-1]
        all_args = "" if not args and not kwargs else args if not kwargs else kwargs if not args else f"{args},{kwargs}"
        return f'{self.func_string}({all_args})'
    
    def record_duration(self, start: float, describer_string: str) -> None:
        # TODO implement this with an env var flag
        return
        record_duration(self.func.__name__, describer_string, time() - start)


class LazyLoggerWrappedCallable(LazyLoggerWrapped):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        assert hasattr(self,'logger'), "You need to set `self.logger` first."
        assert hasattr(self,'log_level'), "You need to set `self.log_level` first."
        start = time()
        self.pre_execution(*args,**kwargs)
        return_value = self.func(*args,**kwargs)
        self.post_execution(start,return_value,*args,**kwargs)
        return return_value
    
    def __repr__(self) -> str:
        return f"<LazyLoggerWrappedCallable '{self.func.__module__}.{self.func.__name__}'>"
    
    def __hash__(self):
        return hash((self.func,self.func_string))


class LazyLoggerWrappedCoroutineFunction(LazyLoggerWrapped):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        assert hasattr(self,'logger'), "You need to set `self.logger` first."
        assert hasattr(self,'log_level'), "You need to set `self.log_level` first."
        awaitable = LazyLoggerWrappedAwaitable(self.func, *args, **kwargs)
        awaitable.logger = self.logger
        awaitable.log_level = self.log_level
        return awaitable
    
    def __repr__(self) -> str:
        return f"<LazyLoggerWrappedCoroutineFunction '{self.func.__module__}.{self.func.__name__}'>"
    
    def __hash__(self):
        return hash((self.func,self.func_string))


class LazyLoggerWrappedGettableCoroutineFunction(LazyLoggerWrapped):
    def __init__(self, func) -> None:
        assert hasattr(func,'__get__')
        self.func = func
        self.func_string = f"{self.func.__module__}.{self.func.__name__}" if self.func.__module__ else self.func.__name__
        functools.update_wrapper(self, func)
    
    def awaitable(self, instance, owner):
        logger.debug(f'instance: {instance}')
        logger.debug(f'owner: {owner}')
        awaitable = LazyLoggerWrappedAwaitable(self.func.__get__,instance,owner=owner)
        assert isawaitable(awaitable)
        awaitable.logger = self.logger
        awaitable.log_level = self.log_level
        return awaitable

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        awaitable = self.awaitable(instance, owner)
        return awaitable

    
class LazyLoggerWrappedAwaitable(LazyLoggerWrapped):
    def __init__(self, func, *args, **kwargs) -> None:
        awaitable = func(*args, **kwargs)
        assert isawaitable(awaitable)
        self.func = func
        self.func_string = f"{self.func.__module__}.{self.func.__name__}" if self.func.__module__ else self.func.__name__
        self.args = args
        self.kwargs = kwargs
        self.awaitable = awaitable
    
    def __hash__(self):
        args = (arg if not isinstance(arg, Iterable) else tuple(arg) for arg in self.args)
        return hash((self.func,self.func_string,args,tuple(self.kwargs)))

    def __await__(self) -> Any:
        start = time()
        assert hasattr(self,'logger'), "You need to set `self.logger` first."
        assert hasattr(self,'log_level'), "You need to set `self.log_level` first."
        logger.debug(self.func)
        logger.debug(self.args)
        logger.debug(self.kwargs)
        self.pre_execution(*self.args,**self.kwargs)
        return_value = yield from self.awaitable.__await__()
        logger.debug(f'awaited once: {type(return_value)}')
        if isawaitable(return_value):
            return_value = yield from return_value.__await__()
            logger.debug(f'awaited twice: {type(return_value)}')
        self.post_execution(start,return_value,*self.args,**self.kwargs)
        return return_value
