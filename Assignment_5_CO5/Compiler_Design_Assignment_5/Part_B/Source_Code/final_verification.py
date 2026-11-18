import csv
import os
import sys

from docx import Document

sys.path.insert(0, os.path.dirname(__file__))
from ir import parse_program, basic_blocks, control_flow
from codegen import SimpleCodeGenerator
from program import execute_ir, execute_target, LOOP_PROGRAM
from dataflow import BitVectorDataFlow
from opt import optimize_level


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MEAS = os.path.join(ROOT, "Part_B", "Measurements")
OUT = os.path.join(ROOT, "Part_B", "Execution_Outputs")
SCREEN = os.path.join(ROOT, "Part_B", "Screenshots")
PART_A = os.path.join(ROOT, "Part_A")
REPORT = os.path.join(OUT, "FINAL_VERIFICATION_REPORT.md")


def read_csv(name):
    with open(os.path.join(MEAS, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(name, passed, detail):
    results.append((name, "PASS" if passed else "FAIL", detail))


results = []

# B1: every test, k value, strategy, and original/target final-value parity.
b1_tests = {
    "loop": LOOP_PROGRAM,
    "redefinition": "a = 10\na = a + 5\nb = a * 2\nresult = b",
    "straight_line": "t1 = 10 + 20\nt2 = t1 * 3\nresult = t2",
    "single_instruction": "result = 42",
    "jump_to_last": "goto L1\nx = 100\nL1:\nresult = 7",
}
b1_failures = []
b1_combinations = set()
for test_name, text in b1_tests.items():
    instructions = parse_program(text)
    original = execute_ir(instructions, {"a": 2})
    for k in (2, 3, 4, 8):
        for strategy in ("first_free", "farther"):
            b1_combinations.add((k, strategy))
            codegen = SimpleCodeGenerator(k, strategy)
            target = codegen.generate(instructions)
            target_values, _ = execute_target(target, {"a": 2})
            if any(target_values.get(variable) != value for variable, value in original.items()):
                b1_failures.append((test_name, k, strategy, original, target_values))
check(
    "B1 - 5 tests x k=2/3/4/8 x both strategies",
    not b1_failures
    and len(b1_combinations) == 8
    and len(read_csv("b1_register_measurements.csv")) == 40,
    "40 combinations in CSV; no original/target final-value mismatch"
    if not b1_failures else "; ".join(str(item) for item in b1_failures),
)

# Register counts and selection strategies are each separately represented.
b1_rows = read_csv("b1_register_measurements.csv")
check(
    "B1 - register counts k=2,3,4,8",
    {int(row["registers"]) for row in b1_rows} == {2, 3, 4, 8},
    "Observed k values: " + ", ".join(str(k) for k in sorted({int(row["registers"]) for row in b1_rows})),
)
check(
    "B1 - register-selection strategies",
    {row["strategy"] for row in b1_rows} == {"first_free", "farther"},
    "Observed strategies: " + ", ".join(sorted({row["strategy"] for row in b1_rows})),
)

# B2: exactly seven IR instructions in every adversarial block.
b2_text = {
    "block_a": "t1 = a + b\nt2 = c + d\nt3 = t1 + t2\nx = t3 + e\nx1 = x + f\nx2 = x1 + g\nresult = x2",
    "block_b": "t1 = a + b\nt2 = c + d\nt3 = e + f\nt4 = g + h\nt5 = t1 + t2\nt6 = t3 + t4\nresult = t5 + t6",
    "block_b_reordered": "t5 = t1 + t2\nt1 = a + b\nt2 = c + d\nt6 = t3 + t4\nt3 = e + f\nt4 = g + h\nresult = t5 + t6",
}
b2_lengths = {name: len(parse_program(text)) for name, text in b2_text.items()}
b2_rows = read_csv("b2_adversarial.csv")
check(
    "B2 - exactly seven IR instructions per block",
    all(length == 7 for length in b2_lengths.values()) and len(b2_rows) == 3,
    ", ".join(f"{name}={length}" for name, length in b2_lengths.items()),
)

# B3: program facts, fixed points, and original/optimised final results.
b3_programs = {
    "straight_line": "a = 2\nb = a + 3\nresult = b",
    "if_else": "a = 1\nifFalse a goto L2\nb = 5\ngoto L3\nL2:\nb = 7\nL3:\nresult = b",
    "loop": "i = 3\nL1:\ni = i - 1\nifFalse i goto L2\ngoto L1\nL2:\nresult = i",
}
b3_results = []
b3_failures = []
for name, text in b3_programs.items():
    instructions = parse_program(text)
    blocks = basic_blocks(instructions)
    successors, predecessors = control_flow(instructions)
    flow = BitVectorDataFlow(blocks)
    gen, kill, reaching_in, reaching_out = flow.reaching_definitions(successors, predecessors)
    use, defs, live_in, live_out = flow.live_variables(successors, predecessors)
    original = execute_ir(instructions, {})
    optimized = optimize_level(instructions, 2)
    optimized_values = execute_ir(optimized, {})
    output_match = original.get("result") == optimized_values.get("result")
    if not output_match:
        b3_failures.append(name)

    if name == "straight_line":
        fact_match = {"a", "b", "result"} <= defs[0] and len(blocks) == 1
    elif name == "if_else":
        b_def_blocks = [i for i, block in enumerate(blocks) if any(inst.result == "b" for inst in block)]
        fact_match = len(b_def_blocks) >= 2
    else:
        fact_match = "i" in use[1] and "i" in defs[1]

    b3_results.append((name, len(blocks), flow.iterations, fact_match, output_match))
check(
    "B3 - straight-line/if-else/loop programs and data-flow facts",
    all(fact and match for _, _, _, fact, match in b3_results) and not b3_failures,
    "; ".join(
        f"{name}: blocks={blocks}, iterations={iterations}, facts={'PASS' if fact else 'FAIL'}, output={'PASS' if match else 'FAIL'}"
        for name, blocks, iterations, fact, match in b3_results
    ),
)
check(
    "B3 - original and optimised final outputs",
    not b3_failures,
    "All final result values match" if not b3_failures else "Mismatches: " + ", ".join(b3_failures),
)

# Verify the current CSV B3 final-match column, including the straight-line case.
b3_csv = read_csv("b3_dataflow.csv")
check(
    "B3 - CSV match column",
    len(b3_csv) == 3 and all(row["match"] == "PASS" for row in b3_csv),
    ", ".join(f"{row['program']}={row['match']}" for row in b3_csv),
)

# B4: levels 0,1,2 and original/level final-result parity.
b4_text = "a = 2 + 3\nb = a * 4\nc = b - b\nb = 20\nd = b + 1\nresult = d"
b4_instructions = parse_program(b4_text)
b4_original = execute_ir(b4_instructions, {})
b4_levels = {}
for level in (0, 1, 2):
    optimized = optimize_level(b4_instructions, level)
    b4_levels[level] = execute_ir(optimized, {}).get("result")
b4_rows = read_csv("b4_optimisation_levels.csv")
check(
    "B4 - levels 0,1,2",
    {int(row["level"]) for row in b4_rows} == {0, 1, 2}
    and all(b4_levels[level] == b4_original["result"] for level in (0, 1, 2)),
    ", ".join(f"L{level} result={value}" for level, value in b4_levels.items()),
)

# Actual measurement and graph artifacts.
required_csv = [
    "b1_register_measurements.csv",
    "b2_adversarial.csv",
    "b3_dataflow.csv",
    "b3_scalability.csv",
    "b4_optimisation_levels.csv",
]
check(
    "Measurements - all five CSV files",
    all(os.path.isfile(os.path.join(MEAS, name)) and os.path.getsize(os.path.join(MEAS, name)) > 0 for name in required_csv),
    ", ".join(name for name in required_csv),
)
required_graphs = [
    "control_flow_graph.png",
    "register_allocation_comparison.png",
    "b3_scalability.png",
    "b4_optimisation_levels.png",
]
check(
    "Graphs - all actual measurement graphs",
    all(os.path.isfile(os.path.join(SCREEN, name)) and os.path.getsize(os.path.join(SCREEN, name)) > 0 for name in required_graphs),
    ", ".join(name for name in required_graphs),
)

# Required Word documents and document-section headings.
individuals = {
    "A1_Code_Generator.docx": "A1 - Code Generator Design",
    "A2_Basic_Blocks.docx": "A2 - Basic Blocks, Flow Graphs and Next Use",
    "A3_Register_Allocation.docx": "A3 - Simple Code Generator",
    "A4_DAG_Optimization.docx": "A4 - DAG-Based Optimisation",
    "A5_Data_Flow.docx": "A5 - Global Data-Flow Analysis",
}
documents_ok = True
document_details = []
for filename, heading_text in individuals.items():
    path = os.path.join(PART_A, filename)
    ok = os.path.isfile(path) and os.path.getsize(path) > 0
    if ok:
        texts = [p.text for p in Document(path).paragraphs]
        ok = heading_text in texts
    documents_ok = documents_ok and ok
    document_details.append(f"{filename}={'PASS' if ok else 'FAIL'}")

final_path = os.path.join(ROOT, "Final_Report.docx")
final_ok = os.path.isfile(final_path) and os.path.getsize(final_path) > 0
if final_ok:
    final_text = "\n".join(p.text for p in Document(final_path).paragraphs)
    required_final_sections = [
        "Assignment Purpose", "A1 - Code Generator Design",
        "A2 - Basic Blocks, Flow Graphs and Next Use",
        "A3 - Simple Code Generator", "A4 - DAG-Based Optimisation",
        "A5 - Global Data-Flow Analysis", "B1 - Code Generator Implementation",
        "B2 - Adversarial Input Experiment", "B3 - Data-Flow Analysis",
        "B4 - Optimisation Levels", "Appendix A - Complete Source Code",
        "Appendix B - Test Inputs and Actual Execution Outputs",
        "Appendix C - Screenshots and Graphs", "References",
    ]
    missing_sections = [section for section in required_final_sections if section not in final_text]
else:
    missing_sections = ["Final_Report.docx absent"]
check(
    "Word reports - 5 individual documents",
    documents_ok,
    "; ".join(document_details),
)
check(
    "Final_Report.docx - required sections",
    final_ok and not missing_sections,
    "All required sections present" if not missing_sections else "Missing: " + ", ".join(missing_sections),
)

lines = [
    "# Final Verification Report",
    "",
    "This report records direct, reproducible checks against the project files and generated outputs.",
    "",
    "| Requirement | Status | Evidence |",
    "|---|---|---|",
]
for name, status, detail in results:
    lines.append(f"| {name} | {status} | {detail.replace('|', '/')} |")

failed = [name for name, status, _ in results if status == "FAIL"]
lines.extend([
    "",
    "## Summary",
    "",
    f"- PASS: {len(results) - len(failed)}",
    f"- FAIL: {len(failed)}",
    f"- NOT VERIFIED: 0",
    "",
])
if failed:
    lines.append("Required failures: " + ", ".join(failed))
else:
    lines.append("All checked requirements passed.")

os.makedirs(OUT, exist_ok=True)
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
print(f"Saved: {REPORT}")

