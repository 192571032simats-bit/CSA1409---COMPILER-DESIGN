"""Print a fixed-point reaching-definitions example for the report."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ir import parse_program, basic_blocks, control_flow
from dataflow import BitVectorDataFlow

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "Execution_Outputs")

TEXT = """\
i = 3
L1:
i = i - 1
ifFalse i goto L2
goto L1
L2:
result = i
"""

if __name__ == "__main__":
    inst = parse_program(TEXT)
    blocks = basic_blocks(inst)
    succ, pred = control_flow(inst)
    df = BitVectorDataFlow(blocks)
    gen, kill, inn, out = df.reaching_definitions(succ, pred)
    lines = ["A5 reaching-definitions fixed-point trace", "GEN and KILL sets:"]
    for i, block in enumerate(blocks):
        lines.append(f"B{i}: GEN={gen[i]}, KILL={kill[i]}, IN={inn[i]}, OUT={out[i]}")
    lines.append(f"Iterations: {df.iterations}")
    lines.append(f"Set operations: {df.set_operations}")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "a5_fixed_point.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
