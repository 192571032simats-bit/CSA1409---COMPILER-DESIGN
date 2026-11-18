from dag import DAG


def constant_fold(instructions):
    constants = {}
    output = []
    for text in instructions:
        if " = " in text:
            target, expression = text.split(" = ", 1)
            parts = expression.split()
            if len(parts) == 3:
                left, op, right = parts
                if left.lstrip("-").isdigit() and right.lstrip("-").isdigit():
                    left_value = int(left)
                    right_value = int(right)
                    value = {
                        "+": left_value + right_value,
                        "-": left_value - right_value,
                        "*": left_value * right_value,
                        "/": int(left_value / right_value) if right_value else "TRAP",
                    }.get(op)
                    if value != "TRAP":
                        output.append(f"{target} = {value}")
                        constants[target] = value
                        continue
        output.append(text)
    return output


def optimize(instructions, level=1):
    result = list(instructions)
    if level >= 1:
        result = constant_fold(result)
    if level >= 2:
        result = DAG().eliminate_common_subexpressions(result)
    return result
