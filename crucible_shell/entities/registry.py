class Registry:

    def __init__(self):
        self.entries = {}

    def add(self, item):
        self.entries[item.__name__] = item

    def add_class(self, cls):
        self.add(cls)
        return cls


