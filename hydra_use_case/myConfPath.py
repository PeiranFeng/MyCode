class MyConfPath:
    def __init__(self, config_name: str):
        self.config_name = config_name
    def toPath(self, hook):
        return hook(self.config_name)