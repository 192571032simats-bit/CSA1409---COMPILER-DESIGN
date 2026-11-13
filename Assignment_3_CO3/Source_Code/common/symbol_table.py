class SymbolTable:
    def __init__(self):
        self.entries = {}

    def add(self, name, data_type):
        if name in self.entries:
            raise ValueError(f'Duplicate declaration: {name}')
        self.entries[name] = data_type
        return data_type

    def lookup(self, name):
        return self.entries.get(name)

    def snapshot(self):
        return dict(self.entries)
