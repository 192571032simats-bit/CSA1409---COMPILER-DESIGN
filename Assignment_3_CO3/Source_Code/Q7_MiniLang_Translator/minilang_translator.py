from pathlib import Path

from Source_Code.common.symbol_table import SymbolTable
from Source_Code.common.utilities import write_lines


def tokenize_program(program: str):
    replacements = {';': ' ; ', '=': ' = ', '+': ' + ', '-': ' - ', '*': ' * ', '/': ' / ', '(': ' ( ', ')': ' ) '}
    for old, new in replacements.items():
        program = program.replace(old, new)
    return [tok.strip() for tok in program.split() if tok.strip()]


def translate_program(program: str):
    symbol_table = SymbolTable()
    code = []
    tokens = tokenize_program(program)
    i = 0

    while i < len(tokens):
        tok = tokens[i]
        if tok in {'int', 'float'}:
            dtype = tok
            i += 1
            name = tokens[i]
            i += 1
            if i < len(tokens) and tokens[i] == ';':
                i += 1
            symbol_table.add(name, dtype)
            code.append(f'{name} : {dtype}')
        elif tok == 'print':
            i += 1
            name = tokens[i]
            i += 1
            if i < len(tokens) and tokens[i] == ';':
                i += 1
            code.append(f'print {name}')
        elif tok.isalpha() or tok.startswith('_'):
            name = tok
            i += 1
            if i < len(tokens) and tokens[i] == '=':
                i += 1
                expr = []
                while i < len(tokens) and tokens[i] != ';':
                    expr.append(tokens[i])
                    i += 1
                if i < len(tokens) and tokens[i] == ';':
                    i += 1
                code.append(f'{name} = {" ".join(expr)}')
        else:
            raise ValueError(f'Unexpected token: {tok}')
    return {'symbol_table': symbol_table.snapshot(), 'generated_code': code}


def generate_q7_outputs():
    out_dir = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q7'
    out_dir.mkdir(parents=True, exist_ok=True)
    program = 'int a; float b; a = 3 + 4; b = 2.5; print a;'
    result = translate_program(program)
    lines = ['Q7 – MiniLang translator', 'Symbol table: ' + str(result['symbol_table'])]
    lines.extend('  ' + line for line in result['generated_code'])
    write_lines(out_dir / 'minilang_output.txt', lines)
    return result
