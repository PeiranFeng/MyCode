"""Use this demo to test figure out type of method object.(bound method, unbound method, etc.)
"""

import inspect
from functools import wraps

# _cache_ = dict()

def decorator(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if not isinstance(self, type):
            if not hasattr(self, 'cache'):
                print('Initial attr cache')
                self.__setattr__('cache', dict())
            cache = self.__getattribute__('cache')
            cache_hit = cache.get((func.__name__), None)
            if cache_hit:
                print('bound method cache hit!')
                return cache_hit
            else:
                print('Call bound method just one time.')
                ret = func(self, *args, **kwargs)
                cache[(func.__name__)] = ret
                self.__setattr__('cache', cache)
                return ret
        return func(self, *args, **kwargs)
    print('type of wrapped decorated by wraps()', type(wrapped))
    return wrapped

def pro_decorator(func):
    def wrapped(*args, **kwargs):
        attr = '__dict__'
        try:
            value = getattr(func, attr)
        except AttributeError:
            print('fail to getattr')
            pass
        else:
            print(attr, value)

        return func(*args, **kwargs)
    return wrapped

class DummyClass:
    def __init__(self, data):
        self.data = data
    
    @decorator
    def bound_func(self):
        return f"Bound method called with data: {self.data}"

    @pro_decorator
    def bound_func2(self):
        return f"Bound method called with data: {self.data}"

    @classmethod
    def class_method(cls):
        return f"Class method called with class: {cls.__name__}"

def test_inspect():
    instance = DummyClass('test inspect')
    assert inspect.ismethod(instance.bound_func)
    assert inspect.ismethod(instance.class_method)
    assert not inspect.isfunction(instance.bound_func)
    assert not inspect.isfunction(instance.class_method)

def test_bound():
    instance = DummyClass('Here I am!')
    assert not hasattr(instance, 'cache')
    instance.bound_func()
    assert hasattr(instance, 'cache')
    assert instance.cache.get('bound_func') == 'Bound method called with data: Here I am!'
    assert instance.bound_func() == 'Bound method called with data: Here I am!'

    another = DummyClass('Another one.')
    assert not hasattr(another, 'cache')

def test_pro_decorator():
    instance = DummyClass('test')
    instance.bound_func2()

