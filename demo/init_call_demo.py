class A:
    def __init__(self, ops):
        w = self()
        for op in ops:
            op = op()
            w = op(w)
        print(w)
    
    def __call__(self):
        print('call A')
        return []

class op:
    def __init__(self):
        self.value = 0

class op1(op):
    def __init__(self):
        self.value = 1

    def __call__(self, w):
        w.append(self.value)
        return w

class op2(op):
    def __init__(self):
        self.value = 2
    
    def __call__(self, w):
        w.append(self.value)
        return w

A([op1,op2])