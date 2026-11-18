class DAG:
    def __init__(self):
        self.nodes = {}

    def expression(self, op, left, right):
        key = (op, left, right)
        if key in self.nodes:
            return self.nodes[key]
        node = f"N{len(self.nodes)}"
        self.nodes[key] = node
        return node

    def eliminate_common_subexpressions(self, instructions):
        seen = {}
        rewritten = []
        for instruction in instructions:
            if " = " in instruction and " " in instruction.split(" = ", 1)[1]:
                target, expression = instruction.split(" = ", 1)
                parts = expression.split()
                if len(parts) == 3:
                    key = (parts[1], parts[0], parts[2])
                    if key in seen:
                        rewritten.append(f"{target} = {seen[key]}")
                        continue
                    seen[key] = target
            rewritten.append(instruction)
        return rewritten
