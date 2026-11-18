"""Simple target-code generator and register descriptors."""
from dataclasses import dataclass
from ir import is_int, next_use


@dataclass
class TargetInstruction:
    op: str
    arg1: str = ""
    arg2: str = ""
    result: str = ""

    def __str__(self):
        if self.op == "LOAD":
            return f"LOAD {self.result}, {self.arg1}"
        if self.op == "STORE":
            return f"STORE {self.arg1}, {self.result}"
        if self.op == "OP":
            return f"{self.op} {self.result}, {self.arg1}, {self.arg2}"
        if self.op in ("COPY", "ADD", "SUB", "MUL", "DIV"):
            if self.op == "COPY":
                return f"COPY {self.result}, {self.arg1}"
            return f"{self.op} {self.result}, {self.arg1}, {self.arg2}"
        return f"{self.op} {self.result}"


class SimpleCodeGenerator:
    def __init__(self, k=2, strategy="farther"):
        self.k = k
        self.strategy = strategy
        self.reg_values = {r: None for r in range(k)}
        self.addr = {}
        self.counters = {"loads": 0, "stores": 0, "spills": 0,
                         "target_instructions": 0, "cost": 0}
        self.trace = []

    def _ensure_operand(self, value, target_instructions):
        if is_int(value):
            return value
        if value in self.reg_values.values():
            return next(r for r, v in self.reg_values.items() if v == value)
        for r in range(self.k):
            if self.reg_values[r] is None:
                target_instructions.append(TargetInstruction("LOAD", value, result=str(r)))
                self.reg_values[r] = value
                self.addr.setdefault(value, set()).add(r)
                self.counters["loads"] += 1
                self.counters["target_instructions"] += 1
                self.counters["cost"] += 1
                return r
        r = self.choose_victim({value})
        self._spill(r, target_instructions)
        target_instructions.append(TargetInstruction("LOAD", value, result=str(r)))
        self.reg_values[r] = value
        self.addr.setdefault(value, set()).add(r)
        self.counters["loads"] += 1
        self.counters["target_instructions"] += 1
        self.counters["cost"] += 1
        return r

    def choose_victim(self, live_now=None, next_table=None, index=-1):
        live_now = live_now or set()
        if self.strategy == "first_free":
            for r in range(self.k):
                if self.reg_values[r] is None:
                    return r
        candidates = list(range(self.k))
        if self.strategy == "farther":
            def priority(r):
                value = self.reg_values[r]
                if value not in live_now:
                    return (0, float("inf"))
                if next_table and value in next_table:
                    return (1, next_table[value])
                return (1, float("inf"))
            return min(candidates, key=priority)
        return 0

    def _spill(self, r, target_instructions):
        value = self.reg_values[r]
        if value is not None:
            target_instructions.append(TargetInstruction("STORE", value, result=str(r)))
            self.addr.setdefault(value, set()).discard(r)
            self.counters["stores"] += 1
            self.counters["spills"] += 1
            self.counters["target_instructions"] += 1
            self.counters["cost"] += 2
        self.reg_values[r] = None

    def generate(self, instructions):
        result = []
        block_tables = next_use(instructions)
        for i, inst in enumerate(instructions):
            before_regs = dict(self.reg_values)
            before_addr = {k: set(v) for k, v in self.addr.items()}
            if inst.op == "label":
                result.append(TargetInstruction("LABEL", inst.label))
                continue
            if inst.op == "goto":
                result.append(TargetInstruction("GOTO", inst.label))
                continue
            if inst.op == "if_false":
                rr = self._ensure_operand(inst.arg1, result)
                result.append(TargetInstruction("IF_FALSE", str(rr), inst.label))
                continue
            operands = [x for x in (inst.arg1, inst.arg2) if x]
            live_now = set(x for x in operands if not is_int(x))
            r1 = self._ensure_operand(inst.arg1, result) if inst.arg1 else None
            r2 = self._ensure_operand(inst.arg2, result) if inst.arg2 and not is_int(inst.arg2) else inst.arg2
            if inst.op == "copy":
                rd = next((r for r, v in self.reg_values.items() if v == inst.result), None)
                if rd is None:
                    free = next((r for r in range(self.k) if self.reg_values[r] is None), None)
                    rd = free if free is not None else self.choose_victim(live_now, block_tables[i], i)
                    if self.reg_values[rd] is not None:
                        self._spill(rd, result)
                if is_int(inst.arg1):
                    result.append(TargetInstruction("LI", inst.arg1, result=str(rd)))
                    self.counters["cost"] += 1
                else:
                    rr = r1 if isinstance(r1, int) else None
                    if rr is not None:
                        result.append(TargetInstruction("COPY", str(rr), result=str(rd)))
                        self.counters["cost"] += 1
            else:
                rd = next((r for r, v in self.reg_values.items() if v == inst.result), None)
                if rd is None:
                    free = next((r for r in range(self.k) if self.reg_values[r] is None), None)
                    rd = free if free is not None else self.choose_victim(live_now, block_tables[i], i)
                    if self.reg_values[rd] is not None:
                        self._spill(rd, result)
                op = {"+" : "ADD", "-" : "SUB", "*" : "MUL", "/" : "DIV"}.get(inst.op, inst.op.upper())
                a1 = str(r1) if isinstance(r1, int) else (f"#{r1}" if is_int(str(r1)) else str(r1))
                a2 = str(r2) if isinstance(r2, int) else (f"#{r2}" if is_int(str(r2)) else str(r2))
                if a2 in ("None", ""):
                    a2 = "#0"
                result.append(TargetInstruction(op, a1, a2, str(rd)))
                self.counters["cost"] += 1
            self.reg_values[rd] = inst.result
            self.addr.setdefault(inst.result, set()).add(rd)
            self.counters["target_instructions"] += len([0 for _ in ()]) + 1
            self.trace.append({
                "instruction": str(inst),
                "before_registers": before_regs,
                "before_addresses": before_addr,
                "after_registers": dict(self.reg_values),
                "after_addresses": {k: set(v) for k, v in self.addr.items()},
            })
        for r, value in list(self.reg_values.items()):
            if value is not None:
                result.append(TargetInstruction("STORE", value, result=str(r)))
                self.counters["stores"] += 1
                self.counters["target_instructions"] += 1
                self.counters["cost"] += 2
        self.counters["target_instructions"] = len(result)
        return result
