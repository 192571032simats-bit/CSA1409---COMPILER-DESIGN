"""Generate actual B1-B4 measurements and CSV files."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ir import parse_program, basic_blocks, control_flow
from codegen import SimpleCodeGenerator
from program import execute_ir, execute_target, LOOP_PROGRAM
from dataflow import BitVectorDataFlow, reverse_postorder
from opt import optimize_level


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "Execution_Outputs")
MEAS = os.path.join(ROOT, "Measurements")
os.makedirs(OUT, exist_ok=True)
os.makedirs(MEAS, exist_ok=True)


TESTS = {
    "loop": LOOP_PROGRAM,
    "redefinition": "a = 10\na = a + 5\nb = a * 2\nresult = b",
    "straight_line": "t1 = 10 + 20\nt2 = t1 * 3\nresult = t2",
    "single_instruction": "result = 42",
    "jump_to_last": "goto L1\nx = 100\nL1:\nresult = 7",
}


def run_b1():
    rows = []
    log = []
    for name, text in TESTS.items():
        inst = parse_program(text)
        env = execute_ir(inst, {"a": 2})
        for k in (2, 3, 4, 8):
            for strategy in ("first_free", "farther"):
                cg = SimpleCodeGenerator(k, strategy)
                target = cg.generate(inst)
                target_env, executed = execute_target(target, {"a": 2})
                if name == "loop" and target_env.get("a") != env.get("a"):
                    passed = "FAIL"
                else:
                    passed = "PASS" if all(target_env.get(x) == v for x, v in env.items()) else "FAIL"
                rows.append({"test": name, "registers": k, "strategy": strategy,
                             "basic_blocks": len(basic_blocks(inst)),
                             "target_instructions": cg.counters["target_instructions"],
                             "loads": cg.counters["loads"], "stores": cg.counters["stores"],
                             "spills": cg.counters["spills"], "cost": cg.counters["cost"],
                             "interpreter_instructions": executed, "result": passed})
        log.append(f"{name}: original={env}, PASS/FAIL checked against target")
    with open(os.path.join(MEAS, "b1_register_measurements.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with open(os.path.join(OUT, "b1_test_results.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    return rows


def run_b2():
    programs = {
        "block_a": "t1 = a + b\nt2 = c + d\nt3 = t1 + t2\nx = t3 + e\nx1 = x + f\nx2 = x1 + g\nresult = x2",
        "block_b": "t1 = a + b\nt2 = c + d\nt3 = e + f\nt4 = g + h\nt5 = t1 + t2\nt6 = t3 + t4\nresult = t5 + t6",
        "block_b_reordered": "t5 = t1 + t2\nt1 = a + b\nt2 = c + d\nt6 = t3 + t4\nt3 = e + f\nt4 = g + h\nresult = t5 + t6",
    }
    rows = []
    for name, text in programs.items():
        inst = parse_program(text)
        cg = SimpleCodeGenerator(2, "farther")
        target = cg.generate(inst)
        peak_live = len(set().union(*[{x.arg1, x.arg2} for x in inst if x.arg1 or x.arg2]))
        rows.append({"block": name, "ir_instructions": len(inst), "target_instructions": len(target),
                     "loads": cg.counters["loads"], "stores": cg.counters["stores"],
                     "spills": cg.counters["spills"], "peak_live_values": peak_live,
                     "estimated_cost": cg.counters["cost"]})
    with open(os.path.join(MEAS, "b2_adversarial.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def run_b3():
    programs = {
        "straight": "a = 2\nb = a + 3\nc = b * 4\nresult = c",
        "if_else": "a = 1\nifFalse a goto L2\nb = 5\ngoto L3\nL2:\nb = 7\nL3:\nresult = b",
        "loop": "i = 3\nL1:\ni = i - 1\nifFalse i goto L2\ngoto L1\nL2:\nresult = i",
    }
    rows = []
    for name, text in programs.items():
        inst = parse_program(text)
        blocks = basic_blocks(inst)
        succ, pred = control_flow(inst)
        df = BitVectorDataFlow(blocks)
        gen, kill, inn, out = df.reaching_definitions(succ, pred)
        use, defs, live_in, live_out = df.live_variables(succ, pred)
        original = execute_ir(inst, {})
        optimized = optimize_level(inst, 2)
        opt_env = execute_ir(optimized, {})
        match = "PASS" if original.get("result") == opt_env.get("result") else "FAIL"
        rows.append({"program": name, "blocks": len(blocks),
                     "iterations": df.iterations, "set_operations": df.set_operations,
                     "match": match})
    with open(os.path.join(MEAS, "b3_dataflow.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    scale_rows = []
    for n in (4, 6, 8, 10, 14, 18):
        inst = parse_program("\n".join([f"x{i} = {i}" for i in range(n)] + ["result = x" + str(n-1)]))
        blocks = basic_blocks(inst)
        succ, pred = control_flow(inst)
        for order_name, order in (("program", list(range(n))), ("reverse_postorder", reverse_postorder(succ))):
            df = BitVectorDataFlow(blocks)
            df.reaching_definitions(succ, pred)
            scale_rows.append({"blocks": n, "order": order_name, "definitions": n,
                               "iterations": df.iterations, "set_operations": df.set_operations})
    with open(os.path.join(MEAS, "b3_scalability.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(scale_rows[0].keys()))
        writer.writeheader()
        writer.writerows(scale_rows)
    return rows, scale_rows


def run_b4():
    text = "a = 2 + 3\nb = a * 4\nc = b - b\nb = 20\nd = b + 1\nresult = d"
    inst = parse_program(text)
    rows = []
    for level in (0, 1, 2):
        optimized = optimize_level(inst, level)
        cg = SimpleCodeGenerator(2, "farther")
        target = cg.generate(optimized)
        rows.append({"level": level, "instructions_before": len(inst),
                     "instructions_after": len(optimized), "target_cost": cg.counters["cost"],
                     "operations": sum(1 for x in optimized if x.op not in ("copy", "label")),
                     "compile_effort": "none" if level == 0 else ("local" if level == 1 else "local + global")})
    with open(os.path.join(MEAS, "b4_optimisation_levels.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    print("B1 rows:", len(run_b1()))
    print("B2 rows:", len(run_b2()))
    print("B3 rows:", len(run_b3()[0]))
    print("B4 rows:", len(run_b4()))
