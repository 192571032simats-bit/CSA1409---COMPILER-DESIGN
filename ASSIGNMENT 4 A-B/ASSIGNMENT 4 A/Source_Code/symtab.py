class Entry:
    def __init__(self, name, typ, address, scope, width, dimensions=None):
        self.name = name
        self.type = typ
        self.address = address
        self.scope = scope
        self.width = width
        self.dimensions = dimensions or ()

    def __repr__(self):
        return f"Entry({self.name}, {self.type}, address={self.address}, width={self.width}, scope={self.scope})"


class Scope:
    WIDTHS = {"int": 4, "float": 8, "boolean": 1, "char": 1, "pointer": 4}

    def __init__(self, name="global", parent=None):
        self.name = name
        self.parent = parent
        self.entries = {}
        self.offset = 0
        self.trace = []

    def enter(self, name, typ, width=None, dimensions=None):
        if name in self.entries:
            raise ValueError(f"duplicate declaration of '{name}'")
        width = width if width is not None else self.width_of(typ)
        entry = Entry(name, typ, self.offset, self.name, width, dimensions)
        self.entries[name] = entry
        self.offset += width
        self.trace.append(("enter", f"enter({name}, {typ}, {entry.address}) w={width}"))
        return entry

    @classmethod
    def width_of(cls, typ):
        if isinstance(typ, tuple) and typ[0] == "array":
            count = 1
            for size in typ[2]:
                count *= size
            return typ[1] * count
        return cls.WIDTHS.get(str(typ), 4)

    def lookup(self, name):
        scope = self
        while scope:
            if name in scope.entries:
                return scope.entries[name]
            scope = scope.parent
        return None


class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global")
        self.current = self.global_scope
        self.scopes = [self.global_scope]

    def enter_scope(self, name):
        scope = Scope(name, self.current)
        self.scopes.append(scope)
        self.current = scope
        return scope

    def leave_scope(self):
        if self.current.parent:
            self.current = self.current.parent

    def declare(self, name, typ, dimensions=None):
        width = dimensions
        if dimensions is not None:
            count = 1
            for size in dimensions:
                count *= size
            base_width = Scope.width_of(typ)
            typ = ("array", base_width, tuple(dimensions))
            width = base_width * count
        return self.current.enter(name, typ, width, dimensions)
