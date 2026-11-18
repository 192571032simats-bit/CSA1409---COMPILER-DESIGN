"""Global constant propagation and dead-code elimination."""
from ir import is_int


def constant_propagation(instructions):
    if any(inst.op in ("goto", "if_false", "label") for inst in instructions):
        return list(instructions), 0
    constants = {}
    out = []
    changed = 0
    for inst in instructions:
        arg1 = constants.get(inst.arg1, inst.arg1)
        arg2 = constants.get(inst.arg2, inst.arg2)
        if arg1 != inst.arg1 or arg2 != inst.arg2:
            changed += 1
        inst = type(inst)(inst.op, str(arg1), str(arg2), inst.result, inst.label)
        out.append(inst)
        if inst.result:
            if inst.op == "copy" and is_int(inst.arg1):
                constants[inst.result] = inst.arg1
            elif inst.result in constants:
                constants.pop(inst.result)
    return out, changed


def dead_code_elimination(instructions, live_roots=None):
    live_roots = set(live_roots or {"d", "result", "out"})
    live = set(live_roots)
    out = [None] * len(instructions)
    for i in range(len(instructions) - 1, -1, -1):
        inst = instructions[i]
        if inst.result and inst.result not in live:
            continue
        out[i] = inst
        if inst.result:
            live.discard(inst.result)
        if inst.arg1 and not is_int(inst.arg1):
            live.add(inst.arg1)
        if inst.arg2 and not is_int(inst.arg2):
            live.add(inst.arg2)
    return [x for x in out if x is not None]


def optimize_level(instructions, level=2):
    if level == 0:
        return list(instructions)
    from dag import dag_optimize
    current = dag_optimize(instructions)
    if any(inst.op in ("goto", "if_false", "label") for inst in instructions):
        return current
    if level >= 2:
        current, _ = constant_propagation(current)
        current = dead_code_elimination(current)
    return current
