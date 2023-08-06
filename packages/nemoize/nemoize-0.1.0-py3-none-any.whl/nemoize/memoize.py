import functools
import inspect
from collections import OrderedDict
from typing import Callable


def memoize(f=None, max_size: int = None, cache_exceptions: bool = False, arg_hash_function: Callable = hash):
    """Decorator utility to memoize a class, function, or method.

    Using this decorator will memoize the wrapped entity.

    If the wrapped entity is a regular function call, and none of the extra features are set (i.e. all the parameters
    are set to their defaults), this will delegate to functools.lru_cache to avoid the performance hit overhead of
    using a callable class with instance methods and attributes.

    There is some overhead to the memoization logic due to the cache constructs, and functions around such, so you
    should really only memoize a function or class that contains potentially expensive computations.
    i.e. Don't use this just to cache very simple property objects or functions.

    For classes, uses the memoized class' __init__ *args and **kwargs as keys.
    For functions/methods, uses the *args and **kwargs as keys.

    Note: If using this on a class, to preserve behavior of obj.__class__ and id(obj.__class__), you must implement
    the function manually:

        @property
        def __class__(self):
            return ContentType

    :param f: Class to memoize
    :param max_size: Max number of entries to memoize for the particular class
    :param cache_exceptions: True to also cache exceptions raised during object creation of the memoized class and
        raise the cached exception if creating again with the same args.
    :param arg_hash_function: Hash function to call the args list and EACH keyword-arg key/value to ultimately use as
        the cache key.  Default is the hash() function.  You can try str() or a custom function to support lists.
        Note: This can heavily impact performance.
    :return: The memoized Class after wrapping it with the memoizer
    """

    class Memoized:

        def __init__(self, func, maxsize: int = None, cache_exc: bool = False, arg_hash_func: Callable = hash):
            """Constructor.

            This should only be called once per entity (class, function, method) that has the @memoize annotation.

            TODO: Add fully custom hash functions

            :param func: Entity (class, function, method) to memoize
            :param maxsize: Max number of entries to memoize for the particular entity
            :param cache_exc: True to also cache exceptions raised during object creation of the memoized class, or
                invoking the function/method and raise the cached exception if called again with the same args.
            :param arg_hash_func: Hash function to call on EACH arg and keyword-arg to ultimately use as the cache key.
                Default is the hash() function.  You can try str() function or a custom function to support lists.
                Note: This can heavily impact performance.
            """
            self._f = func
            self._maxsize = maxsize
            self._cache_exceptions = cache_exc
            self._arg_hash_func = arg_hash_func
            self._cache: OrderedDict = OrderedDict()
            # Make the Memoized class masquerade as the object we are memoizing.
            # Preserve class attributes
            functools.update_wrapper(self, func)
            # Preserve static methods
            # From https://stackoverflow.com/questions/11174362
            for k, v in func.__dict__.items():
                self.__dict__[k] = v.__func__ if type(v) is staticmethod else v

        def __call__(self, *args, **kwargs):
            """Called when the memoized entity is attempting to be constructed.

            Checks the cache using *args and *kwargs as the keys and:

            1. For classes, return a cached object instance of the memoized class if available, else construct a new
                object and then cache it.
            2. For function/methods, return the cached results of the memoized function

            If cache_exceptions was set to True, also raises any cached Exceptions.

            :param args: args to the func
            :param kwargs: keyword-args to the func
            """
            # Generate key
            key = (self._arg_hash_func(args))
            if kwargs:
                key += (object())
                for k, v in kwargs.items():
                    key += (self._arg_hash_func(k))
                    key += (self._arg_hash_func(v))
            key = hash(key)
            # Fetch from cache or call callable
            if key in self._cache:
                res = self._cache[key]
                if self._maxsize:
                    self._cache.move_to_end(key)
                if isinstance(res, Exception):
                    raise res
                return res
            else:
                should_pop = self._maxsize and len(self._cache) >= self._maxsize
                try:
                    res = self._f(*args, **kwargs)
                    if should_pop:
                        self._cache.popitem(False)
                    self._cache[key] = res
                    return res  # noqa: R504
                except Exception as e:
                    if self._cache_exceptions:
                        if should_pop:
                            self._cache.popitem(False)
                        self._cache[key] = e
                    raise e

        def __get__(self, instance, owner):
            """Crazy magic.

            Turns this Memoized into a descriptor so if @memoize is used on an instance method, as it is an
            attribute of a class, this __get__ gets invoked, transforming that attribute lookup into this partial call
            which adds the memoized object instance to the function call as the first parameter to __call__.

            From https://stackoverflow.com/questions/30104047/how-can-i-decorate-an-instance-method-with-a-decorator-class
            """
            return functools.partial(self.__call__, instance)

        def __instancecheck__(self, other):
            """Make isinstance() work"""
            return isinstance(other, self._f)

    @functools.lru_cache(maxsize=max_size)
    def _lru_func_call(*args, **kwargs):
        return f(*args, **kwargs)

    if f:
        if not cache_exceptions and not inspect.isclass(f) and arg_hash_function == hash:
            # Delegate to functools.lru_cache if none of the other extra features we added are being used to avoid
            # performance hits of using a callable class with instance methods
            return _lru_func_call
        else:
            return Memoized(f)
    else:
        def wrapper(func):
            return Memoized(func, max_size, cache_exceptions, arg_hash_function)

        return wrapper
