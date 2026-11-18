"""DAG and local optimisation helpers."""


def constant_fold(op, a, b):
    try:
        x, y = int(a), int(b)
    except (ValueError, TypeError):
        return None
    return {"+": x+y, "-": x-y, "*": x*y, "/": x//y if y else None,
            "%": x%y if y else None}.get(op)


def peephole(instructions):
    out = []
    for inst in instructions:
        text = str(inst)
        if inst.op in ("+", "-", "*", "/"):
            folded = constant_fold(inst.op, inst.arg1, inst.arg2)
            if folded is not None:
                out.append(type(inst)("copy", str(folded), "", inst.result))
                continue
            if inst.op == "*" and inst.arg2 == "1":
                out.append(type(inst)("copy", inst.arg1, "", inst.result))
                continue
            if inst.op == "+" and inst.arg2 == "0":
                out.append(type(inst)("copy", inst.arg1, "", inst.result))
                continue
            if inst.op == "*" and inst.arg2 == "2":
                out.append(type(inst)("+", inst.arg1, inst.arg1, inst.result))
                continue
        out.append(inst)
    return out


def dag_optimize(instructions):
    """Remove repeated expressions within a linear block; operands are checked by value."""
    expr_map = {}
    out = []
    for inst in instructions:
        if inst.op in ("+", "-", "*", "/", "%"):
            key = (inst.op, inst.arg1, inst.arg2)
            if key in expr_map:
                out.append(type(inst)("copy", expr_map[key], "", inst.result))
            else:
                expr_map[key] = inst.result
                out.append(inst)
        else:
            out.append(inst)
    return peephole(out)


def weak_repeated_expression(instructions):
    seen = {}
    out = []
    for inst in instructions:
        if inst.op in ("+", "-", "*", "/", "%"):
            key = (inst.op, inst.arg1, inst.arg2)
            if key in seen:
                out.append(type(inst)("copy", seen[key], "", inst.result))
            else:
                seen[key] = inst.result
                out.append(inst)
        else:
            out.append(inst)
    return out
