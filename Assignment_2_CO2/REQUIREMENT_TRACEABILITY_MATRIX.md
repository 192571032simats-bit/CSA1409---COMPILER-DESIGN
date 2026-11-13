# Requirement Traceability Matrix

## Original source

The implementation is based on the official assessment paper:

- `Question_Paper/AT2_SCENARIO_BASED_TASK.pdf`
- `Question_Paper/AT2_SCENARIO_BASED_TASK.txt`

## Requirement mapping

| Requirement | Original scenario | What must be implemented | Source code | Input / evidence | Output / evidence | Verification | Status |
|---|---|---|---|---|---|---|---|
| Q1 | Parsing table conflict in LL(1) | Explain FIRST/FOLLOW conflict, identify multiple entries in one cell, and show grammar redesign for LL(1) | `Source_Code/Q1/ll1_conflict_demo.py` | `Output_Files/Q1_ll1_conflict.txt` | Deterministic parsing table and repaired grammar | Execute script and review output | PASS |
| Q2 | Incorrect parse tree generation | Show ambiguous parse tree for `id + id - id`, explain associativity issue, and enforce correct grouping | `Source_Code/Q2/parse_tree_demo.py` | `Output_Files/Q2_parse_tree.txt` | Correct left-associative tree and explanation | Execute script and review output | PASS |
| Q3 | Invalid expression handling | Detect missing operand error in `id + * id`, explain diagnostic point, and discuss recovery | `Source_Code/Q3/error_handling_demo.py` | `Output_Files/Q3_error_handling.txt` | Syntax error and recovery strategy | Execute script and review output | PASS |
| Q4 | Ambiguity in conditional statements | Explain dangling else problem and nearest-then resolution | `Source_Code/Q4/dangling_else_demo.py` | `Output_Files/Q4_dangling_else.txt` | Unambiguous grammar and decision rule | Execute script and review output | PASS |
| Q5 | Operator precedence conflict | Explain ambiguity of `id + id * id`, precedence levels, and grammar redesign | `Source_Code/Q5/operator_precedence_demo.py` | `Output_Files/Q5_operator_precedence.txt` | Correct precedence-based grammar and correct evaluation | Execute script and review output | PASS |

## Evidence note

All five requirement traces have been implemented, executed, and recorded in actual project output files. The generated evidence is stored under `Output_Files/`.
