"""Run the full Assignment 2 scenario-based parser validation suite."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    ROOT / 'Source_Code' / 'Q1' / 'll1_conflict_demo.py',
    ROOT / 'Source_Code' / 'Q2' / 'parse_tree_demo.py',
    ROOT / 'Source_Code' / 'Q3' / 'error_handling_demo.py',
    ROOT / 'Source_Code' / 'Q4' / 'dangling_else_demo.py',
    ROOT / 'Source_Code' / 'Q5' / 'operator_precedence_demo.py',
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

print('All Assignment 2 validation scripts completed successfully.')
