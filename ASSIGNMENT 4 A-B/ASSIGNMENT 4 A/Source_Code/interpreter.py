class InterpreterError(Exception):
    pass


class Interpreter:
    def __init__(self):
        self.variables = {}

    def run(self, instructions):
        ip = 0
        while ip < len(instructions):
            text = instructions[ip].text.strip()
            if text == "HALT":
                break
            if " = " in text:
                target, expression = text.split(" = ", 1)
                if "inttofloat" in expression:
                    _, value = expression.split(maxsplit=1)
                    result = float(self.value(value))
                elif expression.startswith("neg "):
                    result = -self.value(expression[4:].strip())
                else:
                    parts = expression.split()
                    if len(parts) == 3:
                        result = self.binary(self.value(parts[0]), parts[1], self.value(parts[2]))
                    else:
                        result = self.value(expression)
                self.variables[target] = result
            elif text.startswith("if ") and " goto " in text:
                condition, target = text[3:].rsplit(" goto ", 1)
                parts = condition.split()
                if len(parts) == 3 and self.binary(self.value(parts[0]), parts[1], self.value(parts[2])):
                    ip = self.find_index(instructions, target)
                    continue
            elif text.startswith("goto "):
                ip = self.find_index(instructions, text.split()[1])
                continue
            ip += 1
        return self.variables

    @staticmethod
    def find_index(instructions, target):
        target = int(target)
        for index, instruction in enumerate(instructions):
            if instruction.index == target:
                return index
        raise InterpreterError(f"invalid jump target {target}")

    def value(self, token):
        if token in self.variables:
            return self.variables[token]
        try:
            return float(token) if "." in token else int(token)
        except ValueError:
            return 0

    @staticmethod
    def binary(left, op, right):
        return {
            "+": left + right,
            "-": left - right,
            "*": left * right,
            "/": int(left / right) if isinstance(left, int) and isinstance(right, int) else left / right,
            "<": left < right,
            "<=": left <= right,
            ">": left > right,
            ">=": left >= right,
            "==": left == right,
            "!=": left != right,
        }[op]
