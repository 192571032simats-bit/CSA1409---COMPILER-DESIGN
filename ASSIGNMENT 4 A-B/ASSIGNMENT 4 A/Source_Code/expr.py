from ir import Emitter


class ExprGenerator:
    NUMERIC = {"int", "float"}
    SCALAR = {"int", "float", "boolean"}

    def __init__(self, symbols, emitter=None):
        self.symbols = symbols
        self.emitter = emitter or Emitter()

    def require_numeric(self, typ):
        if typ not in self.NUMERIC:
            raise ValueError("numeric required")

    def require_scalar(self, typ):
        if typ not in self.SCALAR:
            raise ValueError("scalar required")

    def widen(self, place, source, target):
        if source == target:
            return place
        if source != "int" or target != "float":
            raise ValueError("invalid widening")
        result = self.emitter.newtemp("float")
        self.emitter.emit(f"{result} = inttofloat {place}")
        return result

    def common(self, left_place, left_type, right_place, right_type):
        self.require_numeric(left_type)
        self.require_numeric(right_type)
        target = "float" if "float" in (left_type, right_type) else "int"
        left_place = self.widen(left_place, left_type, target)
        right_place = self.widen(right_place, right_type, target)
        return left_place, right_place, target

    def binary(self, op, left_place, left_type, right_place, right_type):
        left_place, right_place, typ = self.common(left_place, left_type, right_place, right_type)
        result = self.emitter.newtemp(typ)
        self.emitter.emit(f"{result} = {left_place} {op} {right_place}")
        return result, typ

    def unary_minus(self, place, typ):
        self.require_numeric(typ)
        result = self.emitter.newtemp(typ)
        self.emitter.emit(f"{result} = neg {place}")
        return result, typ

    def identifier(self, name):
        entry = self.symbols.current.lookup(name)
        if entry is None:
            raise ValueError(f"undeclared name '{name}'")
        typ = "int" if isinstance(entry.type, tuple) else entry.type
        self.require_scalar(typ)
        return entry.name, typ

    def assign(self, name, place, typ):
        entry = self.symbols.current.lookup(name)
        if entry is None:
            raise ValueError(f"undeclared name '{name}'")
        entry_type = entry.type
        if entry_type == typ:
            pass
        elif entry_type == "float" and typ == "int":
            place = self.widen(place, "int", "float")
        else:
            raise ValueError("incompatible assignment")
        self.emitter.emit(f"{entry.name} = {place}")
