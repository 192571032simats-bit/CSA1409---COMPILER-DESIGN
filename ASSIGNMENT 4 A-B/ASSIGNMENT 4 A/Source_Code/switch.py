class SwitchGenerator:
    def __init__(self, emitter):
        self.emitter = emitter

    def sequential(self, expression, cases, default=None):
        tests = []
        for value, body in cases:
            tests.append(self.emitter.emit(f"if {expression} == {value} goto _"))
        tests.append(self.emitter.emit("goto _"))
        body_targets = {}
        return tests, body_targets

    def binary_search(self, expression, cases, default=None):
        ordered = sorted(cases)
        if not ordered:
            return
        instructions = []
        for value, body in ordered:
            instructions.append(self.emitter.emit(f"if {expression} == {value} goto _"))
        instructions.append(self.emitter.emit("goto _"))
        return instructions

    def jump_table(self, expression, cases, default=None):
        if not cases:
            raise ValueError("jump table requires at least one case")
        minimum = min(value for value, _ in cases)
        maximum = max(value for value, _ in cases)
        self.emitter.emit(f"{expression}_jump_table = [{minimum}..{maximum}]")
