# Final Completion Audit – Compiler Design Assignment 2 (CO2)

## Scope

This audit checks the rebuilt Assignment 2 project against the official CO2 assessment paper and the requested Assignment 2 checklist. The status below intentionally distinguishes between verified evidence and environment-dependent gaps.

## Requirement-by-requirement audit

| No. | Requirement | Status | Evidence / File | Missing work |
|---|---|---|---|---|
| 1 | Q1 – CFG, terminals, non-terminals, productions, ambiguity and repair | PASS | `Assignment_2_CO2/Output_Files/Q1_grammar_analysis.txt` | None |
| 2 | Q2 – Top-down parsing, FIRST/FOLLOW, recursive descent and LL(1) trace | PASS | `Assignment_2_CO2/Output_Files/Q2_recursive_descent.txt`, `Assignment_2_CO2/Output_Files/Q2_ll1_parsing.txt` | None |
| 3 | Q3 – Bottom-up parsing, handles, precedence table and reduction trace | PASS | `Assignment_2_CO2/Output_Files/Q3_shift_reduce.txt`, `Assignment_2_CO2/Output_Files/Q3_operator_precedence.txt` | None |
| 4 | Q4 – LR(0), closure/GOTO, SLR table and valid/invalid traces | PASS | `Assignment_2_CO2/Output_Files/Q4_lr0_items.txt`, `Assignment_2_CO2/Output_Files/Q4_slr_table.txt`, `Assignment_2_CO2/Output_Files/Q4_valid_trace.txt`, `Assignment_2_CO2/Output_Files/Q4_invalid_trace.txt` | None |
| 5 | Q5 – Error catalogue and recovery strategies | PASS | `Assignment_2_CO2/Output_Files/Q5_error_catalogue.txt`, `Assignment_2_CO2/Output_Files/Q5_panic_mode.txt`, `Assignment_2_CO2/Output_Files/Q5_phrase_level.txt`, `Assignment_2_CO2/Output_Files/Q5_error_productions.txt` | None |
| 6 | Q6 – YACC/Bison and Flex implementation | PARTIAL | `Assignment_2_CO2/Source_Code/Q6/expr_parser.y`, `Assignment_2_CO2/Source_Code/Q6/expr_lexer.l`, `Assignment_2_CO2/Output_Files/Q6_bison_conflicts.txt` | Direct Bison/Flex compile remains blocked by the installed GnuWin32 path-share issue on this machine; the grammar/discussion evidence is present, but full toolchain compilation is not yet confirmed |
| 7 | Q7 – Redesign challenge and evidence-based comparison | PASS | `Assignment_2_CO2/Output_Files/Q7_original_results.csv`, `Assignment_2_CO2/Output_Files/Q7_redesigned_results.csv`, `Assignment_2_CO2/Output_Files/Q7_redesign_summary.txt` | None |
| 8 | Word report and final PDF report | PASS | `Assignment_2_CO2/Word_Report/Assignment_2_CO2_Final_Report.docx`, `Assignment_2_CO2/PDF_Report/Assignment_2_CO2_Final_Report.pdf` | None |
| 9 | Execution evidence logs and output files | PASS | `Assignment_2_CO2/Execution_Evidence/run_all_log.txt`, `Assignment_2_CO2/Output_Files/` | None |
| 10 | GitHub publication and remote verification | PARTIAL | `git remote -v` and `git ls-remote --heads origin` | The remote is configured and reachable, but the specific latest assignment files were not independently confirmed in this session as published; publication remains partially verified |

## Summary counts

- Total requirements checked: 10
- PASS: 8
- PARTIAL: 2
- FAIL: 0
- NOT VERIFIED: 0

## Final status

The project contains substantial and traceable evidence for the full CO2 task. The work is not marked as fully complete because the YACC/Bison compile validation and the remote publication were not fully verified in this environment. The folder therefore reflects the honest current status rather than overstating completion.
