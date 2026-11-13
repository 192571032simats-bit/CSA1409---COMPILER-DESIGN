from pathlib import Path

from Source_Code.common.symbol_table import SymbolTable
from Source_Code.common.utilities import write_csv, write_lines


def add_type(symbol_table, name, type_name):
    symbol_table.add(name, type_name)
    return symbol_table.lookup(name)


def parse_declaration_list(names, type_name, symbol_table):
    rows = []
    for name in names:
        try:
            add_type(symbol_table, name, type_name)
            rows.append({'name': name, 'type': type_name, 'status': 'valid'})
        except ValueError as exc:
            rows.append({'name': name, 'type': type_name, 'status': 'duplicate', 'message': str(exc)})
    return rows


def analyze_declaration_tests():
    symbol_table = SymbolTable()
    cases = [
        ('float a, b, c', ['a', 'b', 'c'], 'float'),
        ('int x, y', ['x', 'y'], 'int'),
        ('int a', ['a'], 'int'),
        ('float b', ['b'], 'float'),
    ]
    rows = []
    for declaration, names, type_name in cases:
        entries = parse_declaration_list(names, type_name, symbol_table)
        rows.append({'declaration': declaration, 'status': 'valid', 'entries': entries, 'table': symbol_table.snapshot()})
    return rows


def generate_q2_outputs():
    out_dir = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q2'
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = analyze_declaration_tests()
    write_csv(out_dir / 'declaration_tests.csv', [
        {'declaration': row['declaration'], 'status': row['status'], 'table': str(row['table'])}
        for row in rows
    ])
    write_lines(out_dir / 'declaration_summary.txt', [
        'Q2 – Inherited declaration analysis',
        *[f"{row['declaration']} -> table={row['table']}" for row in rows]
    ])
    return {'rows': rows, 'status': 'success'}
