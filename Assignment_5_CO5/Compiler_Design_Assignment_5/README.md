# Compiler Design Assignment 5 - CO5

## Project overview
This project implements code generation, basic-block and CFG construction, register allocation, DAG optimisation, global data-flow analysis, optimisation levels, measurements and an academic Word report for Unit V.

## Folder structure
The required `Part_A`, `Part_B/Source_Code`, `Part_B/Test_Inputs`, `Part_B/Execution_Outputs`, `Part_B/Measurements` and `Part_B/Screenshots` folders are included.

## Python installation
```bat
py --version
py -m pip install -r requirements.txt
```

## Run all implementations
From this project directory:
```bat
py Part_B\Source_Code\program.py
py Part_B\Source_Code\measure.py
py Part_B\Source_Code\a5_trace.py
py Part_B\Source_Code\b3_tests.py
py Part_B\Source_Code\draw_cg_figs.py
py generate_report.py
```

## Run tests and measurements
`b3_tests.py` compares manual facts, generated facts and original/optimised execution. `measure.py` runs B1-B4 tests and writes CSV files. `draw_cg_figs.py` creates graphs from the actual CSV results.

## Outputs
- Execution evidence: `Part_B/Execution_Outputs`
- CSV measurements: `Part_B/Measurements`
- Graphs: `Part_B/Screenshots`
- Individual reports: `Part_A`
- Combined report: `Final_Report.docx`
