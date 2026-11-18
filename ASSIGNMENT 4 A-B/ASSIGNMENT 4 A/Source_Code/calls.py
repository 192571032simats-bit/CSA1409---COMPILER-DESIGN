class ProcedureGenerator:
    def __init__(self, emitter):
        self.emitter = emitter

    def call(self, name, arguments, result_type="void"):
        for argument in arguments:
            self.emitter.emit(f"param {argument}")
        if result_type == "void":
            result = None
        else:
            result = self.emitter.newtemp(result_type)
        self.emitter.emit(f"{result or ''} call {name}, {len(arguments)}")
        return result

    def return_value(self, place=None):
        self.emitter.emit("return" if place is None else f"return {place}")
