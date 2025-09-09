"""
在set中插入相同的元素，第二个元素会被丢弃
"""

OTHER_IDX = 0

def get_idx():
    global OTHER_IDX
    OTHER_IDX += 1
    return OTHER_IDX

class Other:
    def __init__(self, value=1):
        self.value = value
        self.index = get_idx()

    def __eq__(self, another):
        assert isinstance(another, Other)
        return self.value == another.value
    
    def __hash__(self):
        return hash(self.value)

    def get(self):
        return self.value
    
    def __del__(self):
        print('other del...', self.index)
        self.value=0

class DummyClass:
    def __init__(self):
        self.value = set()

def f(a: DummyClass):
    other = Other()
    a.value.add(other)
    return a

a = DummyClass()
print('function call 1')
f(a)
print('function call 2')
f(a)
print('done')