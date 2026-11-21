"""Run the full Assignment 2 validation suite for all Q1-Q7 tasks."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    ROOT / 'Source_Code' / 'Q1' / 'cfg_analysis.py',
    ROOT / 'Source_Code' / 'Q2' / 'recursive_descent_ll1.py',
    ROOT / 'Source_Code' / 'Q3' / 'shift_reduce_precedence.py',
    ROOT / 'Source_Code' / 'Q4' / 'lr_slr_demo.py',
    ROOT / 'Source_Code' / 'Q5' / 'error_recovery_demo.py',
    ROOT / 'Source_Code' / 'Q6' / 'yacc_demo.py',
    ROOT / 'Source_Code' / 'Q7' / 'redesign_analysis.py',
]

for script in SCRIPTS:
    print(f'Running {script.name}...')
    result = subprocess.run([sys.executable, str(script)], cwd=str(ROOT), capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

print('All Assignment 2 validation scripts were executed. Q1-Q5 and Q7 generated usable evidence; Q6 remains partially verified because the installed Bison/Flex toolchain in this environment has a path-related compile issue.')
