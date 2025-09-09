class LinearSweep:
    def __iter__(self):
        for v in [1,2,3]:
            yield v


def a():
    yield from LinearSweep()

for _ in a():
    print(_)