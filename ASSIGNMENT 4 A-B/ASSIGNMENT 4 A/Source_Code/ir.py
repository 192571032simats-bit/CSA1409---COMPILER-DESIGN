class Instruction:
    def __init__(self, index, text):
        self.index = index
        self.text = text

    def __str__(self):
        return f"{self.index}: {self.text}"


class Emitter:
    def __init__(self, start=100):
        self.code = []
        self.nextquad = start
        self.temp_count = 0

    def emit(self, text):
        instruction = Instruction(self.nextquad, text)
        self.code.append(instruction)
        self.nextquad += 1
        return instruction.index

    def newtemp(self, typ="int"):
        self.temp_count += 1
        return f"T{self.temp_count}({typ})"

    @staticmethod
    def makelist(index):
        return [index]

    def merge(self, left, right):
        return list(left) + list(right)

    def backpatch(self, indexes, target):
        for index in indexes:
            if 0 <= index - self.code[0].index < len(self.code):
                instruction = self.code[index - self.code[0].index]
                instruction.text = instruction.text.replace("_", str(target))

    def emit_halt(self):
        self.emit("HALT")
