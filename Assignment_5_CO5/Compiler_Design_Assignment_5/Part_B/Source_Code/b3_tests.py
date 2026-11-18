"""Three required data-flow tests with manual facts and execution comparison."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ir import parse_program, basic_blocks
from ir import control_flow
from dataflow import BitVectorDataFlow
from program import execute_ir
from opt import optimize_level

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "Execution_Outputs")

PROGRAMS = {
    "straight_line": ("a = 2\nb = a + 3\nresult = b",
                      {"manual_reaching": "At result, the latest definitions are d(a), d(b)",
                       "manual_live": "a and b are live at their defining/using points"}),
    "if_else": ("a = 1\nifFalse a goto L2\nb = 5\ngoto L3\nL2:\nb = 7\nL3:\nresult = b",
                {"manual_reaching": "At result, definitions of b in both branches reach",
                 "manual_live": "b is live at L3 merge; a is live at branch test"}),
    "loop": ("i = 3\nL1:\ni = i - 1\nifFalse i goto L2\ngoto L1\nL2:\nresult = i",
             {"manual_reaching": "The initial i=3 and i=i-1 definitions reach the loop header",
              "manual_live": "i is live in the loop increment and exit test"}),
}


def run():
    lines = []
    for name, (text, manual) in PROGRAMS.items():
        inst = parse_program(text)
        blocks = basic_blocks(inst)
        succ, pred = control_flow(inst)
        df = BitVectorDataFlow(blocks)
        gen, kill, inn, out = df.reaching_definitions(succ, pred)
        use, defs, live_in, live_out = df.live_variables(succ, pred)
        original = execute_ir(inst, {})
        optimized = optimize_level(inst, 2)
        opt_result = execute_ir(optimized, {})
        if "result" in original:
            status = "PASS" if original["result"] == opt_result.get("result") else "FAIL"
        else:
            status = "PASS" if original == opt_result else "FAIL"
        lines.append(f"{name}: {status}")
        lines.append(f"  Manual: {manual}")
        lines.append(f"  Generated: blocks={len(blocks)}, iterations={df.iterations}")
        lines.append(f"  original={original}")
        lines.append(f"  optimized={opt_result}")
        lines.append(f"  optimized IR: " + "; ".join(str(x) for x in optimized))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "b3_tests.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    print(f"Saved: {path}")


if __name__ == "__main__":
    run()
