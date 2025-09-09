class DummyClass:
    def __init__(self, method, obj):
        self.method = method
        self.obj = obj
    
    def __eq__(self, another):
        return self.method == another.method and self.obj == another.obj

    def __hash__(self):
        return hash(self.method) ^ hash(self.obj)

def test():
    a12 = DummyClass(method='1', obj='2')
    b12 = DummyClass(method='1', obj='2')
    assert a12 == b12
    a22 = DummyClass(method='2', obj='2')
    assert a12 != a22
    
    assert len(set((a12, b12, a22))) == 2

    instance = DummyClass(method='3', obj='4')
    print(type(instance))
    a = set()
    a.add(instance)
    assert instance in a
    new_instance = DummyClass(method='3', obj='4')
    assert new_instance == instance and new_instance in a
    del instance
    assert new_instance in a
    assert isinstance(a.pop(), DummyClass)
    
