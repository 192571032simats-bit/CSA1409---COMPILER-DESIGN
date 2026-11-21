# Requirement Traceability Matrix

## Original source

The implementation is based on the official assessment paper:

- `Question_Paper/AT2_SCENARIO_BASED_TASK.pdf`
- `Question_Paper/AT2_SCENARIO_BASED_TASK.txt`

## Requirement mapping

| Requirement | Question focus | What must be implemented | Source code | Evidence file(s) | Verification status |
|---|---|---|---|---|---|
| Q1 | CFG, terminals, productions and ambiguity | Grammar design, leftmost/rightmost derivations, ambiguity, repaired grammar, AST vs parse tree | `Source_Code/Q1/cfg_analysis.py` | `Output_Files/Q1_grammar_analysis.txt` | PASS |
| Q2 | Top-down parsing | Left-recursion elimination, left factoring, FIRST/FOLLOW, recursive descent, LL(1) parsing trace | `Source_Code/Q2/recursive_descent_ll1.py` | `Output_Files/Q2_recursive_descent.txt`, `Output_Files/Q2_ll1_parsing.txt` | PASS |
| Q3 | Bottom-up parsing | Hand reductions, shift-reduce trace, handles, precedence table, operator-precedence examples | `Source_Code/Q3/shift_reduce_precedence.py` | `Output_Files/Q3_shift_reduce.txt`, `Output_Files/Q3_operator_precedence.txt` | PASS |
| Q4 | LR and SLR parsing | Augmented grammar, LR(0) item sets, closure/GOTO, SLR table, valid/invalid traces | `Source_Code/Q4/lr_slr_demo.py` | `Output_Files/Q4_lr0_items.txt`, `Output_Files/Q4_slr_table.txt`, `Output_Files/Q4_valid_trace.txt`, `Output_Files/Q4_invalid_trace.txt` | PASS |
| Q5 | Error handling and recovery | Six error catalogues, panic-mode recovery, phrase-level recovery, error productions | `Source_Code/Q5/error_recovery_demo.py` | `Output_Files/Q5_error_catalogue.txt`, `Output_Files/Q5_panic_mode.txt`, `Output_Files/Q5_phrase_level.txt`, `Output_Files/Q5_error_productions.txt` | PASS |
| Q6 | YACC implementation | YACC/Bison and LEX specs, conflict reports, grammar rewrite vs precedence declarations, recovery experiments | `Source_Code/Q6/yacc_demo.py`, `Source_Code/Q6/expr_parser.y`, `Source_Code/Q6/expr_lexer.l` | `Output_Files/Q6_bison_conflicts.txt`, `Output_Files/Q6_valid_run.txt`, `Output_Files/Q6_invalid_run.txt`, `Output_Files/Q6_ast_output.txt` | PARTIAL |
| Q7 | Day-4 redesign challenge | Evidence-based diagnosis, measurable objective, original-vs-redesigned experiment and trade-offs | `Source_Code/Q7/redesign_analysis.py` | `Output_Files/Q7_original_results.csv`, `Output_Files/Q7_redesigned_results.csv`, `Output_Files/Q7_redesign_summary.txt` | PASS |
| Word report | Final submission document | Full report for all questions, diagrams, evidence, and output summaries | `generate_final_document.py` | `Word_Report/Assignment_2_CO2_Final_Report.docx`, `PDF_Report/Assignment_2_CO2_Final_Report.pdf` | PASS |
| Execution evidence | Validation and actual runs | Full evidence log across the project | `run_all.py` | `Execution_Evidence/run_all_log.txt` | PASS |
| Publication | GitHub repository check | Verify the remote repository contains the files and the latest generated set | `git remote -v` and GitHub remote | Remote configured, but latest push not independently confirmed in this session | PARTIAL |

## Notes

- Q1-Q5 and Q7 are backed by generated output files and executed scripts.
- Q6 includes the required grammar and conflict analysis files, but the direct Bison/Flex compilation remains partially verified because the installed GnuWin32 toolchain on this machine does not resolve its share-path correctly during the final compile step.
- The final report and output files are intentionally honest about these limitations and do not claim a full 100% verified completion without evidence.
