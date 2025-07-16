"""Demo of cacheable decorator for class methods.
"""

class Stack:
    class EmptyError(Exception):
        pass
    def __init__(self):
        self.data = []
    def __len__(self):
        return len(self.data)
    def top(self):
        if self.empty():
            raise self.EmptyError
        return self.data[-1]
    def push(self, x):
        self.data.append(x)
    def pop(self):
        self.data.pop()
    def empty(self):
        return 0 == len(self.data)

_cache_stack_ = Stack()

class Cache:
    def __init__(self, enable=True):
        self.cache = {}
        self.enablements = Stack()
        self.enablements.push(enable)
    def __enter__(self):
        _cache_stack_.push(self)
    def __exit__(self, exc_type, exc_value, exc_traceback):
        assert self is _cache_stack_.top()
        _cache_stack_.pop()
        self.cache = {}
    def __contains__(self, key):
        return key in self.cache
    def __setitem__(self, key, value):
        self.cache[key] = value
    def __getitem__(self, key):
        return self.cache[key]
    @property
    def is_enabled(self):
        return self.enablements.top()

    class Controller:
        def __init__(self, enablement):
            self.enablement = enablement
            self.cache = None
        def __enter__(self):
            self.cache = _cache_stack_.top()
            self.cache.enablements.push(self.enablement)
        def __exit__(self, exc_type, exc_value, exc_traceback):
            if self.cache is not None:
                self.cache.enablements.pop()
    enabled = Controller(True)
    disabled = Controller(False)

import inspect

def _argument_key_(signature, args, kwargs):
    bound = signature.bind(*args, **kwargs)
    bound.apply_defaults()
    return tuple(item for item in sorted(bound.arguments.items()))

def cacheable(backend):
    signature = inspect.signature(backend)
    def wrapped(*args, **kwargs):
        cache_hit = False
        cache_store = False
        if not _cache_stack_.empty():
            cache = _cache_stack_.top()
            if cache.is_enabled:
                key = (backend,) + _argument_key_(signature, args, kwargs)
                if key in cache:
                    cache_hit = True
                else:
                    cache_store = True
        if cache_hit:
            output = cache[key]
        else:
            output = backend(*args, **kwargs)
        if cache_store:
            cache[key] = output
        return output
    wrapped.__signature__ = signature
    return wrapped

@cacheable
def normal_func(x, y):
    return x+y

if __name__ == '__main__':
    with Cache.enabled:
        print(normal_func(1, 2))  # Should compute and cache the result
        print(normal_func(1, 2))