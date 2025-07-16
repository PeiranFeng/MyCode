from guppy import hpy
from copy import deepcopy, copy

def f():
    return [_ for _ in range(50000)]

def g(buffer):
    a = DummyClass()
    a.__setattr__('cache', buffer)

class DummyClass():
    def __init__(self):
        pass 

buffer = f()
hp = hpy()
base_line = hp.heap()
################################
# test memory
a = DummyClass()
a.__setattr__('cache', f())
del a
################################
print('#end',hp.heap() - base_line)
