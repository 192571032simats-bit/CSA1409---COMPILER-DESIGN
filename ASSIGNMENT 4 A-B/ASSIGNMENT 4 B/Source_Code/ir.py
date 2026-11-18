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
        return f"T{self.temp_count}"

    def makelist(self, index):
        return [index]

    @staticmethod
    def merge(left, right):
        return list(left) + list(right)

    def backpatch(self, indexes, target):
        lookup = {instruction.index: instruction for instruction in self.code}
        for index in indexes:
            if index in lookup:
                lookup[index].text = lookup[index].text.replace("_", str(target))

    def finish(self):
        self.emit("HALT")
