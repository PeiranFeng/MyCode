class MyConfPath:
    def __init__(self, *args):
        self.config_name = ''.join([str(_) for _ in args])
    def toPath(self, hook):
        return hook(self.config_name)


Base = MyConfPath


class AConfPath(Base):
    def __init__(self, config_name):
        super().__init__(config_name)