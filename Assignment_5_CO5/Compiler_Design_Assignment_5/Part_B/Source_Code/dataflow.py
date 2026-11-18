"""Bit-vector data-flow analyses."""


class BitVectorDataFlow:
    def __init__(self, blocks):
        self.blocks = blocks
        self.set_operations = 0
        self.iterations = 0

    def union(self, sets):
        self.set_operations += 1
        out = set()
        for s in sets:
            out |= s
        return out

    def reaching_definitions(self, succ, pred):
        n = len(self.blocks)
        definitions = {}
        gen = [set() for _ in range(n)]
        kill = [set() for _ in range(n)]
        variable_defs = {}
        for i, block in enumerate(self.blocks):
            for j, inst in enumerate(block):
                if getattr(inst, "result", ""):
                    variable_defs.setdefault(inst.result, set()).add((i, j))
        for i, block in enumerate(self.blocks):
            for j, inst in enumerate(block):
                if getattr(inst, "result", ""):
                    d = (i, j)
                    gen[i].add(d)
                    kill[i].update(variable_defs[inst.result] - {d})
        inn, out = [set() for _ in range(n)], [set() for _ in range(n)]
        order = list(range(n))
        changed = True
        while changed:
            changed = False
            self.iterations += 1
            for i in order:
                new_in = self.union([out[p] for p in pred[i]]) if pred[i] else set()
                new_out = gen[i] | (new_in - kill[i])
                self.set_operations += 2
                if new_in != inn[i] or new_out != out[i]:
                    inn[i], out[i] = new_in, new_out
                    changed = True
        return gen, kill, inn, out

    def live_variables(self, succ, pred):
        n = len(self.blocks)
        use, defs = [set() for _ in range(n)], [set() for _ in range(n)]
        for i, block in enumerate(self.blocks):
            seen_defs = set()
            for inst in block:
                for operand in (getattr(inst, "arg1", ""), getattr(inst, "arg2", "")):
                    if operand and not operand.isdigit() and operand not in seen_defs:
                        use[i].add(operand)
                if getattr(inst, "result", ""):
                    result = inst.result
                    defs[i].add(result)
                    seen_defs.add(result)
        inn, out = [set() for _ in range(n)], [set() for _ in range(n)]
        changed = True
        while changed:
            changed = False
            self.iterations += 1
            for i in range(n - 1, -1, -1):
                new_out = self.union([inn[s] for s in succ[i]]) if succ[i] else set()
                new_in = use[i] | (new_out - defs[i])
                self.set_operations += 2
                if new_in != inn[i] or new_out != out[i]:
                    inn[i], out[i] = new_in, new_out
                    changed = True
        return use, defs, inn, out


def reverse_postorder(succ):
    visited, post = set(), []
    def visit(v):
        visited.add(v)
        for w in sorted(succ[v]):
            if w not in visited:
                visit(w)
        post.append(v)
    for v in sorted(succ):
        if v not in visited:
            visit(v)
    return list(reversed(post))
