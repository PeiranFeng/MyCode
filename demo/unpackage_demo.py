def a(values):
    for _ in values:
        yield [_]

def b(*args):
    for i, arg in enumerate(args):
        print(i, f"value: {arg}")

b(*list(a([1,2,3]))+list(a([4,5])))