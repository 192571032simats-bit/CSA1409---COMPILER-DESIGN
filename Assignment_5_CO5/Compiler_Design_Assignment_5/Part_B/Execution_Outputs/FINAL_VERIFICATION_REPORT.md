# Final Verification Report

This report records direct, reproducible checks against the project files and generated outputs.

| Requirement | Status | Evidence |
|---|---|---|
| B1 - 5 tests x k=2/3/4/8 x both strategies | PASS | 40 combinations in CSV; no original/target final-value mismatch |
| B1 - register counts k=2,3,4,8 | PASS | Observed k values: 2, 3, 4, 8 |
| B1 - register-selection strategies | PASS | Observed strategies: farther, first_free |
| B2 - exactly seven IR instructions per block | PASS | block_a=7, block_b=7, block_b_reordered=7 |
| B3 - straight-line/if-else/loop programs and data-flow facts | PASS | straight_line: blocks=1, iterations=3, facts=PASS, output=PASS; if_else: blocks=4, iterations=4, facts=PASS, output=PASS; loop: blocks=4, iterations=6, facts=PASS, output=PASS |
| B3 - original and optimised final outputs | PASS | All final result values match |
| B3 - CSV match column | PASS | straight=PASS, if_else=PASS, loop=PASS |
| B4 - levels 0,1,2 | PASS | L0 result=21, L1 result=21, L2 result=21 |
| Measurements - all five CSV files | PASS | b1_register_measurements.csv, b2_adversarial.csv, b3_dataflow.csv, b3_scalability.csv, b4_optimisation_levels.csv |
| Graphs - all actual measurement graphs | PASS | control_flow_graph.png, register_allocation_comparison.png, b3_scalability.png, b4_optimisation_levels.png |
| Word reports - 5 individual documents | PASS | A1_Code_Generator.docx=PASS; A2_Basic_Blocks.docx=PASS; A3_Register_Allocation.docx=PASS; A4_DAG_Optimization.docx=PASS; A5_Data_Flow.docx=PASS |
| Final_Report.docx - required sections | PASS | All required sections present |

## Summary

- PASS: 12
- FAIL: 0
- NOT VERIFIED: 0

All checked requirements passed.