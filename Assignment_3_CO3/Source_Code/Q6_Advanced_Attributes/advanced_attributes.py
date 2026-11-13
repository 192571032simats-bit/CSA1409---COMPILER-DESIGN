from pathlib import Path

from Source_Code.common.utilities import write_lines


def precedence(op):
    if op in {'+', '-'}:
        return 1
    if op in {'*', '/'}:
        return 2
    return 0


def infix_to_postfix(expr: str):
    output = []
    stack = []
    tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
    for token in tokens:
        if token.isdigit() or token.isalpha():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError('Mismatched parentheses')
            stack.pop()
        elif token in {'+', '-', '*', '/'}:
            while stack and stack[-1] != '(' and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)
        else:
            raise ValueError(f'Unexpected token: {token}')
    while stack:
        if stack[-1] == '(':
            raise ValueError('Mismatched parentheses')
        output.append(stack.pop())
    return output


def build_three_address_code(expr: str):
    postfix = infix_to_postfix(expr)
    temp_count = 0
    code = []
    stack = []

    def new_temp():
        nonlocal temp_count
        temp_count += 1
        return f't{temp_count}'

    for token in postfix:
        if token.isdigit() or token.isalpha():
            stack.append(token)
        elif token in {'+', '-', '*', '/'}:
            if len(stack) < 2:
                raise ValueError('Invalid expression')
            right = stack.pop()
            left = stack.pop()
            temp = new_temp()
            code.append(f'{temp} = {left} {token} {right}')
            stack.append(temp)
        else:
            raise ValueError(f'Unexpected token: {token}')
    if len(stack) != 1:
        raise ValueError('Expression reduction failed')
    return code


def generate_q6_outputs():
    out_dir = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q6'
    out_dir.mkdir(parents=True, exist_ok=True)
    exprs = ['3 + 4 * 5', 'a + b * c', 'x - y / z']
    lines = ['Q6 – Advanced attributes and three-address code']
    all_code = []
    for expr in exprs:
        code = build_three_address_code(expr)
        all_code.extend(code)
        lines.append(expr + ':')
        for c in code:
            lines.append('  ' + c)
    write_lines(out_dir / 'three_address_code.txt', lines)
    return {'code': all_code, 'status': 'success'}
