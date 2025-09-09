"""
装饰过的函数和原函数不相同
"""

from functools import wraps
import inspect

_origen_method_ = dict()

def decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print('wrapper')
        print('can detect method: ',inspect.ismethod(func))
        print('self: ',isinstance(self, DummyClass))
        print('cls: ', isinstance(self, type))
        _origen_method_[self] = func
        return func(self, *args, **kwargs)
    print('decorator')
    return wrapper

class DummyClass():
    def __init__(self, data):
        print('init')
        self.data = data
    @decorator
    def get(self):
        return self.data
    @classmethod
    @decorator
    def class_method(cls):
        print('class method')

if __name__ == '__main__':
    print('start')
    a = DummyClass('A')
    print('\ta.get')
    a.get()
    assert a.get != _origen_method_[a]
    print('\tclass method')
    DummyClass.class_method()
    print('end')

