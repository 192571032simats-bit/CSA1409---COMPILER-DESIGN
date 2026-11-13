from pathlib import Path

from Source_Code.common.utilities import write_lines


def precedence(op):
    if op in {'+', '-'}:
        return 1
    if op in {'*', '/'}:
        return 2
    return 0


def translate_to_postfix(expr: str) -> str:
    output = []
    stack = []
    tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
    for tok in tokens:
        if tok.isdigit() or tok.isalpha():
            output.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError('Mismatched parentheses')
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence(stack[-1]) >= precedence(tok):
                output.append(stack.pop())
            stack.append(tok)
    while stack:
        if stack[-1] == '(':
            raise ValueError('Mismatched parentheses')
        output.append(stack.pop())
    return ' '.join(output)


def check_mid_production_case():
    expr = 'a + b'
    output = []
    stack = []
    for token in expr.split():
        if token.isalpha():
            output.append(token)
        elif token in '+-*/':
            stack.append(token)
    return 'bad: ' + ' '.join(stack + output)


def generate_q4_outputs():
    out_dir = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q4'
    out_dir.mkdir(parents=True, exist_ok=True)
    inputs = ['a + b * (c - d)', '2 + 3 * 4', 'x + y + z', '(a + b) * c', 'p - q / r', 'm * (n + o)']
    lines = ['Q4 – Infix-to-postfix SDT']
    for expr in inputs:
        lines.append(f'{expr} -> {translate_to_postfix(expr)}')
    lines.append('Mid-production experiment: ' + check_mid_production_case())
    write_lines(out_dir / 'postfix_outputs.txt', lines)
    return {'expressions': inputs, 'status': 'success'}
