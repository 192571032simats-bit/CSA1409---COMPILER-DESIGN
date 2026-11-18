"""Three-address IR parsing and control-flow helpers."""
from dataclasses import dataclass
import re


@dataclass
class Instruction:
    op: str
    arg1: str
    arg2: str = ""
    result: str = ""
    label: str = ""

    def __str__(self):
        if self.op == "copy":
            return f"{self.result} = {self.arg1}"
        if self.op == "label":
            return f"{self.label}:"
        if self.op == "goto":
            return f"goto {self.label}"
        if self.op == "if_false":
            return f"ifFalse {self.arg1} goto {self.label}"
        if self.op == "return":
            return f"return {self.arg1}"
        return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


def parse_instruction(text: str, line_no: int = 0):
    text = text.strip()
    if not text:
        return None
    if text.startswith("L") and text.endswith(":"):
        return Instruction("label", "", "", "", text[:-1])
    m = re.match(r"goto\s+(\w+)$", text)
    if m:
        return Instruction("goto", "", "", "", m.group(1))
    m = re.match(r"ifFalse\s+(\S+)\s+goto\s+(\w+)$", text)
    if m:
        return Instruction("if_false", m.group(1), "", "", m.group(2))
    m = re.match(r"return\s+(\S+)$", text)
    if m:
        return Instruction("return", m.group(1))
    m = re.match(r"(\w+)\s*=\s*(.+)$", text)
    if not m:
        raise ValueError(f"Invalid IR instruction at line {line_no}: {text}")
    result, expr = m.groups()
    parts = expr.split()
    if len(parts) == 1:
        return Instruction("copy", parts[0], "", result)
    if len(parts) == 3:
        return Instruction(parts[1], parts[0], parts[2], result)
    raise ValueError(f"Invalid expression at line {line_no}: {text}")


def parse_program(text: str):
    instructions = []
    for line_no, line in enumerate(text.splitlines(), 1):
        inst = parse_instruction(line, line_no)
        if inst:
            instructions.append(inst)
    return instructions


def is_int(value: str):
    try:
        int(value)
        return True
    except ValueError:
        return False


def find_leaders(instructions):
    leaders = {0}
    labels = {inst.label: i for i, inst in enumerate(instructions) if inst.op == "label"}
    for i, inst in enumerate(instructions):
        if inst.op in ("goto", "if_false"):
            target = labels.get(inst.label)
            if target is not None:
                leaders.add(target)
            if i + 1 < len(instructions):
                leaders.add(i + 1)
    if instructions:
        for i, inst in enumerate(instructions):
            if inst.op == "label" and i not in leaders:
                leaders.add(i)
    return sorted(leaders)


def basic_blocks(instructions):
    leaders = find_leaders(instructions)
    result = []
    for pos, start in enumerate(leaders):
        end = (leaders[pos + 1] if pos + 1 < len(leaders) else len(instructions))
        result.append(instructions[start:end])
    return result


def control_flow(instructions):
    blocks = basic_blocks(instructions)
    label_to_block = {}
    for i, block in enumerate(blocks):
        if block and block[0].op == "label":
            label_to_block[block[0].label] = i
    succ = {i: set() for i in range(len(blocks))}
    pred = {i: set() for i in range(len(blocks))}
    for i, block in enumerate(blocks):
        last = block[-1]
        if last.op == "goto":
            target = label_to_block.get(last.label)
            if target is not None:
                succ[i].add(target)
        elif last.op == "if_false":
            target = label_to_block.get(last.label)
            if target is not None:
                succ[i].add(target)
            if i + 1 < len(blocks):
                succ[i].add(i + 1)
        elif i + 1 < len(blocks):
            succ[i].add(i + 1)
    for i, targets in succ.items():
        for j in targets:
            pred[j].add(i)
    return succ, pred


def next_use(instructions):
    """Backward next-use mapping: next position for variables in a block."""
    next_pos = {}
    tables = [dict() for _ in instructions]
    for i in range(len(instructions) - 1, -1, -1):
        inst = instructions[i]
        tables[i] = dict(next_pos)
        operands = ([inst.arg1] if inst.op in ("copy", "return") else
                    ([inst.arg1, inst.arg2] if inst.arg1 or inst.arg2 else []))
        if inst.op == "if_false":
            operands = [inst.arg1]
        for operand in operands:
            if operand and not is_int(operand):
                next_pos[operand] = i
        if inst.result and not is_int(inst.result):
            next_pos.pop(inst.result, None)
    return tables
