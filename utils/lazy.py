import copy
import operator

def new_method_proxy(func):
    """
    Util function to help us route functions
    to the nested object.
    """

    def inner(self, *args):
        if not self._is_init:
            self._setup()
        return func(self._wrapped, *args)

    return inner

class LazyObject:
    """
    Our LazyObject take a factory method as a argument in __init__.
    This factory method is the function that instantiate
    the object that we want to be lazy.
    For example we could do LazyObject(lambda: Context()) to provide
    a factory that instantiates a Context.
    Whenever we interact with any of the dunder methods
    (e.g. __setattr__, __getattr__, __len__ etc) we call _setup() which
    finally instantiates our object using the factory method. This means that
     we defer any instantiation until we for example try to get a value using __getattr__.
    Methods are routed to the _wrapped object using the new_method_proxy()
    utility function. This means that if we for example call len() on our LazyObject,
     it will actually route that call to call len() on our wrapped object.
    """
    _empty = object()
    _wrapped = None
    _is_init = False

    def __init__(self,wrapped):
        self.__dict__['_factory'] = wrapped

    def _setup(self):
        self._wrapped = self._factory()
        self._is_init = True

    def __reduce__(self):
        if self._wrapped is self._empty:
            self._setup()
        return (unpickle_lazyobject, (self._wrapped,))

    def __copy__(self):
        if self._wrapped is self._empty:
            # If uninitialized, copy the wrapper. Use type(self), not
            # self.__class__, because the latter is proxied.
            return type(self)()
        else:
            # If initialized, return a copy of the wrapped object.
            return copy.copy(self._wrapped)

    def __deepcopy__(self, memo):
        if self._wrapped is self._empty:
            # We have to use type(self), not self.__class__, because the
            # latter is proxied.
            result = type(self)()
            memo[id(self)] = result
            return result
        return copy.deepcopy(self._wrapped, memo)

    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)

    # Introspection support
    __dir__ = new_method_proxy(dir)

    # Need to pretend to be the wrapped class, for the sake of objects that
    # care about this (especially in equality tests)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __lt__ = new_method_proxy(operator.lt)
    __gt__ = new_method_proxy(operator.gt)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)

    # List/Tuple/Dictionary methods support
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)

def unpickle_lazyobject(wrapped):
    return wrapped


