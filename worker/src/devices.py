class Device:

    def __init__(self, name=None, config=None):
        self.name = name
        self.config = config

    def __repr__(self):
        return f'<{self.__class__.__name__} ({self.name})>'


class ConnectedDevice:

    def __init__(self, name=None, config=None, handler=None):
        self.name = name
        self.config = config
        self.handler = handler

    def __repr__(self):
        return f'<{self.__class__.__name__} ({self.name})>'
