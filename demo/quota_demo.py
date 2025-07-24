"""
python 以引用的方式传递参数
"""
g = []

def f(_g_, value):
    _g_.append(value)

f(g, 1)
assert len(g) == 1