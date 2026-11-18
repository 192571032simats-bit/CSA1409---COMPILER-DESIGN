# ASSIGNMENT 4 A

## Topic

Compiler Design Unit IV, CO4: Intermediate Code Generation - intermediate languages, declarations, assignment statements, boolean expressions, case statements, backpatching, and language-independent translation schemes for intermediate-code generation.

## Students

- E. Ragul - 192571032
- S. Sunderesan - 192411245

## Contents

- `Report/` - Expected Word and PDF reports.
- `Source_Code/` - Expected Python implementation modules.
- `Test_Inputs/` - Test input files.
- `Test_Outputs/` - Generated test output files.
- `Measurements/` - Performance or implementation measurements.
- `Diagrams/` - Assignment diagrams.

## Run available code

From `Source_Code/`:

```bat
python mini_compiler.py ..\Test_Inputs\declarations.txt
python -m unittest discover
```

The modules provide symbol-table declarations, typed expression generation, backpatching, switch dispatch, procedure calls, mini-compiler integration, and interpretation. A sample input and generated output are included under `Test_Inputs/` and `Test_Outputs/`.
