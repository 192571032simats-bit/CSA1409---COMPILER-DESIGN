# Compiler Design Assignment 2 (CO2)

This project is a clean restart of the original Assignment 2 work based on the official `AT2 SCENARIO BASED TASK` assessment paper. It focuses on the five scenario-based parser-design questions covering LL(1) conflicts, parse tree construction, syntax error recovery, dangling else resolution, and operator precedence.

## Project structure

- `Question_Paper/` – original assessment paper and extracted text
- `Source_Code/` – Python implementations for each scenario-based question
- `Input_Files/` – sample input examples
- `Output_Files/` – execution evidence and logs
- `Test_Cases/` – verification commands and expected outputs
- `Execution_Evidence/` – runtime logs and notes
- `Parsing_Tables/` – LL(1) / LR-style table examples
- `Performance_Analysis/` – not required for this paper; retained only if needed
- `Documentation/` – traceability and audit files
- `Word_Report/` – generated final Word document
- `PDF_Report/` – generated PDF report

## How to run

From the repository root:

```powershell
cd "C:\Users\ADMIN\Documents\CSA1409---COMPILER-DESIGN\Assignment_2_CO2"
python Source_Code\Q1\ll1_conflict_demo.py
python Source_Code\Q2\parse_tree_demo.py
python Source_Code\Q3\error_handling_demo.py
python Source_Code\Q4\dangling_else_demo.py
python Source_Code\Q5\operator_precedence_demo.py
```

All outputs are saved under `Output_Files/` and `Execution_Evidence/`.

## Assignment coverage

This project directly addresses the original scenario-based task in the CO2 assessment:

1. LL(1) parsing table conflict and FIRST/FOLLOW analysis
2. Parse tree associativity and grouping errors
3. Syntax error detection and recovery
4. Dangling else resolution strategy
5. Operator precedence conflict and correct grammar redesign

## Verification

The implementation files have been executed and the outputs recorded in `Output_Files/`.
