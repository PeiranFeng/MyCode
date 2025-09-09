class IterClass:
    def __init__(self):
        self.value = 1

    def __next__(self):
        if self.value>=5:
            raise StopIteration
        ret = self.value
        self.value+=1
        return ret
    
    def __iter__(self):
        return self

a = IterClass()
for _ in a:
    print(_)

print(a[0], a[1])