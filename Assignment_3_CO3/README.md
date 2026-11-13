# Assignment 3 – Compiler Design (CO3)

This project implements the required syntax-directed translation and attribute grammar work for Compiler Design Unit III and keeps the work isolated in its own folder so earlier assignments remain untouched.

## Structure

- `Source_Code/common/`: common utilities and compiler helpers
- `Source_Code/Q1_Synthesized_Attributes/`: synthesized attributes and expression evaluation
- `Source_Code/Q2_Inherited_Attributes/`: inherited declarations and symbol table analysis
- `Source_Code/Q3_Dependency_Graphs/`: dependency graphs and evaluation ordering
- `Source_Code/Q4_Syntax_Directed_Translation/`: infix-to-postfix SDT implementation
- `Source_Code/Q5_AST_Generation/`: parse tree and AST generation
- `Source_Code/Q6_Advanced_Attributes/`: advanced attributes and 3-address code
- `Source_Code/Q7_MiniLang_Translator/`: MiniLang translator
- `Output_Files/`: generated experiment outputs and reports
- `Tests/`: validation scripts

## Run

```powershell
cd "C:\Users\ADMIN\Documents\CSA1409---COMPILER-DESIGN\Assignment_3_CO3"
python .\run_all.py
pytest -q
```

## Coverage

- Q1: synthesized attributes, annotated parse tree, height experiment
- Q2: inherited declarations, symbol table, duplicate/undeclared checks
- Q3: dependency graphs, Kahn topological sort, cycle detection
- Q4: infix-to-postfix SDT and action order analysis
- Q5: parse tree and AST generation
- Q6: advanced attributes, marker nonterminal, three-address code generation
- Q7: MiniLang translator and generated code
