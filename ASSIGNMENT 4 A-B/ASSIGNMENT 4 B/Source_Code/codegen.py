from ir import Emitter


class CodeGenerator:
    def __init__(self):
        self.emitter = Emitter()
        self.loop_stack = []

    def expression(self, left, op, right, typ="int"):
        result = self.emitter.newtemp(typ)
        self.emitter.emit(f"{result} = {left} {op} {right}")
        return result

    def array_load(self, base, row, column, second_dimension):
        offset = self.emitter.newtemp("int")
        self.emitter.emit(f"{offset} = {row} * {second_dimension}")
        address = self.emitter.newtemp("int")
        self.emitter.emit(f"{address} = {offset} + {column}")
        result = self.emitter.newtemp("int")
        self.emitter.emit(f"{result} = {base}[{address}]")
        return result

    def array_store(self, base, row, column, second_dimension, value):
        offset = self.emitter.newtemp("int")
        self.emitter.emit(f"{offset} = {row} * {second_dimension}")
        address = self.emitter.newtemp("int")
        self.emitter.emit(f"{address} = {offset} + {column}")
        self.emitter.emit(f"{base}[{address}] = {value}")

    def inclusive_loop(self, variable, lower, upper, step, body):
        lower_temp = self.emitter.newtemp()
        upper_temp = self.emitter.newtemp()
        step_temp = self.emitter.newtemp()
        self.emitter.emit(f"{lower_temp} = {lower}")
        self.emitter.emit(f"{upper_temp} = {upper}")
        self.emitter.emit(f"{step_temp} = {step}")
        if step.isdigit() and int(step) == 0:
            raise ValueError("constant step 0 is invalid")
        header = self.emitter.nextquad
        self.emitter.emit(f"{variable} = {lower_temp}")
        positive_header = self.emitter.emit(f"if {variable} <= {upper_temp} goto _")
        negative_header = self.emitter.emit(f"if {variable} >= {upper_temp} goto _")
        increment = self.emitter.nextquad
        body(increment)
        exit_target = self.emitter.emit("goto _")
        increment_target = self.emitter.emit(f"{variable} = {variable} + {step_temp}")
        back_header = self.emitter.emit(f"goto {header}")
        exit_target_text = self.emitter.nextquad
        self.emitter.backpatch([positive_header, negative_header], exit_target_text)
        self.emitter.emit("TRAP step 0")
        self.emitter.finish()
