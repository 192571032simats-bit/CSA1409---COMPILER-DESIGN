# Compiler Design Assignment 2 (CO2)

This folder is a clean Assignment 2 working set created to match the official CO2 task in `Question_Paper/AT2_SCENARIO_BASED_TASK.txt` and the scenario-based checklist discussed during the assignment review. It contains the implementation evidence and report artifacts generated for Q1-Q7, while keeping an honest verification status for items that remain environment-dependent.

## Project structure

Assignment_2_CO2/
├── Question_Paper/
│   ├── AT2_SCENARIO_BASED_TASK.pdf
│   └── AT2_SCENARIO_BASED_TASK.txt
├── Source_Code/
│   ├── Q1/
│   ├── Q2/
│   ├── Q3/
│   ├── Q4/
│   ├── Q5/
│   ├── Q6/
│   └── Q7/
├── Input_Files/
│   ├── Q1/
│   ├── Q2/
│   ├── Q3/
│   ├── Q4/
│   ├── Q5/
│   ├── Q6/
│   └── Q7/
├── Output_Files/
│   ├── Q1_grammar_analysis.txt
│   ├── Q2_recursive_descent.txt
│   ├── Q2_ll1_parsing.txt
│   ├── Q3_shift_reduce.txt
│   ├── Q3_operator_precedence.txt
│   ├── Q4_lr0_items.txt
│   ├── Q4_slr_table.txt
│   ├── Q4_valid_trace.txt
│   ├── Q4_invalid_trace.txt
│   ├── Q5_error_catalogue.txt
│   ├── Q5_panic_mode.txt
│   ├── Q5_phrase_level.txt
│   ├── Q5_error_productions.txt
│   ├── Q6_bison_conflicts.txt
│   ├── Q6_valid_run.txt
│   ├── Q6_invalid_run.txt
│   ├── Q6_ast_output.txt
│   ├── Q7_original_results.csv
│   ├── Q7_redesigned_results.csv
│   └── Q7_redesign_summary.txt
├── Diagrams/
│   ├── Q1_parse_trees/
│   ├── Q2_parsing_flowchart/
│   ├── Q3_shift_reduce/
│   ├── Q4_lr0_dfa/
│   └── Q7_redesign_architecture/
├── Execution_Evidence/
│   └── run_all_log.txt
├── Documentation/
│   └── assignment_notes.md
├── Performance_Analysis/
│   └── analysis_summary.md
├── Parsing_Tables/
│   └── Q1_ll1_table_summary.txt
├── Test_Cases/
│   └── verification_commands.md
├── Word_Report/
│   ├── Assignment_2_CO2_Final_Report.docx
│   └── Assignment_2_CO2_Final_Report.md
├── PDF_Report/
│   └── Assignment_2_CO2_Final_Report.pdf
├── README.md
├── REQUIREMENT_TRACEABILITY_MATRIX.md
├── FINAL_COMPLETION_AUDIT.md
├── run_all.py
├── generate_final_document.py
└── Documentation/

## Coverage by question

- Q1: CFG, terminals, non-terminals, productions, ambiguity, grammar repair, parse tree vs AST
- Q2: left recursion elimination, left factoring, FIRST/FOLLOW sets, recursive descent, LL(1) parsing trace
- Q3: shift-reduce parsing, handles, operator precedence relation table, expression parsing examples
- Q4: augmented grammar, LR(0) item sets, closure/GOTO, SLR table, valid/invalid traces
- Q5: error catalogues, panic mode, phrase-level recovery, error productions, cascading messages
- Q6: YACC/Bison and LEX specifications, conflict reports, grammar rewrite vs precedence declarations
- Q7: evidence-based diagnosis, measurable objectives, original-vs-redesigned comparison

## Execution

Run the project validation suite:

```powershell
cd "C:\Users\ADMIN\Documents\CSA1409---COMPILER-DESIGN\Assignment_2_CO2"
python .\run_all.py
```

Run individual components:

```powershell
python .\Source_Code\Q1\cfg_analysis.py
python .\Source_Code\Q2\recursive_descent_ll1.py
python .\Source_Code\Q3\shift_reduce_precedence.py
python .\Source_Code\Q4\lr_slr_demo.py
python .\Source_Code\Q5\error_recovery_demo.py
python .\Source_Code\Q6\yacc_demo.py
python .\Source_Code\Q7\redesign_analysis.py
```

## Verification status

The project contains actual generated evidence for Q1-Q7. However, the YACC/Bison verification remains partially environment-dependent because the installed GnuWin32 toolchain in this machine generates a path-related failure during the direct Flex/Bison compile step. The project therefore records the grammar/conflict analysis and generated outputs honestly, while noting that the compiler-level verification for Q6 still needs a clean Bison/Flex environment.

## Evidence location

Actual outputs are stored in `Output_Files/`, the consolidated validation log in `Execution_Evidence/run_all_log.txt`, and the final Word/PDF evidence in `Word_Report/` and `PDF_Report/`.
