class Metric:
    def __init__(self, backend, t):
        print('Metric init..')
        self.backend = backend
        self.t = t

class Backend:
    def __init__(self, *values):
        self.values = values
        print([*values], [type(_) for _ in values])

class cell:
    def __init__(self):
        print('cell init')
class Tuple:
    def __init__(self, *args):
        self.value = tuple(args)
