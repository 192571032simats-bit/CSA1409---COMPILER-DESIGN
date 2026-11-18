"""Example programs and end-to-end target interpreter."""
import sys
from ir import parse_program, is_int
from codegen import SimpleCodeGenerator


LOOP_PROGRAM = """\
c = 3
L1:
c = c - 1
ifFalse c goto L2
goto L1
L2:
result = c
"""


def execute_ir(instructions, env=None):
    env = dict(env or {})
    pc = 0
    labels = {i.label: j for j, i in enumerate(instructions) if i.op == "label"}
    steps = 0
    while pc < len(instructions):
        inst = instructions[pc]
        steps += 1
        if steps > 10000:
            raise RuntimeError("IR execution exceeded 10000 steps")
        if inst.op == "copy":
            env[inst.result] = env.get(inst.arg1, int(inst.arg1) if is_int(inst.arg1) else 0)
        elif inst.op in ("+", "-", "*", "/", "%"):
            a = env.get(inst.arg1, int(inst.arg1) if is_int(inst.arg1) else 0)
            b = env.get(inst.arg2, int(inst.arg2) if is_int(inst.arg2) else 0)
            env[inst.result] = {"+" : a+b, "-" : a-b, "*" : a*b,
                                "/" : a//b if b else 0, "%" : a%b if b else 0}[inst.op]
        elif inst.op == "goto":
            pc = labels[inst.label]
            continue
        elif inst.op == "if_false":
            if not env.get(inst.arg1, 0):
                pc = labels[inst.label]
                continue
        elif inst.op == "label":
            pass
        pc += 1
    return env


def execute_target(target, env=None):
    env = dict(env or {})
    registers = [0] * 20
    pc = 0
    labels = {}
    for i, inst in enumerate(target):
        if inst.op == "LABEL":
            labels[inst.arg1] = i
    executed = 0
    while pc < len(target):
        inst = target[pc]
        executed += 1
        if inst.op == "LI":
            registers[int(inst.result)] = int(inst.arg1)
        elif inst.op == "COPY":
            registers[int(inst.result)] = registers[int(inst.arg1)]
        elif inst.op in ("ADD", "SUB", "MUL", "DIV"):
            def operand(text):
                if text.startswith("#"):
                    return int(text[1:])
                if text.isdigit():
                    return registers[int(text)]
                return env.get(text, 0)
            a = operand(inst.arg1)
            b = operand(inst.arg2)
            registers[int(inst.result)] = {"ADD":a+b, "SUB":a-b, "MUL":a*b, "DIV":a//b if b else 0}[inst.op]
        elif inst.op == "LOAD":
            registers[int(inst.result)] = env.get(inst.arg1, int(inst.arg1) if is_int(inst.arg1) else 0)
        elif inst.op == "STORE":
            env[inst.arg1] = registers[int(inst.result)]
        elif inst.op == "GOTO":
            pc = labels[inst.arg1]
            continue
        elif inst.op == "IF_FALSE":
            if registers[int(inst.arg1)] == 0:
                pc = labels[inst.arg2]
                continue
        pc += 1
    return env, executed
