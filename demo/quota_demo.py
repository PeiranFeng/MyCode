"""
python 以引用的方式传递参数
"""
g = []

def f(_g_, value):
    _g_.append(value)

f(g, 1)
assert len(g) == 1

class DummyClass:
    def __init__(self):
        pass

a = DummyClass()
a.__setattr__('mm', set())
s = a.__getattribute__('mm')
s.add(1)
assert len(a.__getattribute__('mm')) == 1
