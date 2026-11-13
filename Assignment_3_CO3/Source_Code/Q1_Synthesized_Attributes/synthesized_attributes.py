from __future__ import annotations

from pathlib import Path

from Source_Code.common.lexer import tokenize
from Source_Code.common.tree import Node
from Source_Code.common.utilities import write_csv, write_lines


def parse_factor(tokens, pos):
    tok = tokens[pos]
    if tok.kind == 'NUMBER':
        node = Node('F', value=tok.value, production='F -> digit')
        return node, pos + 1
    if tok.kind == '(':
        expr_node, pos = parse_expression(tokens, pos + 1)
        if pos >= len(tokens) or tokens[pos].kind != ')':
            raise ValueError('Missing closing parenthesis')
        node = Node('F', production='F -> ( E )')
        node.add_child(expr_node)
        return node, pos + 1
    raise ValueError(f'Unexpected token: {tok}')


def parse_term(tokens, pos):
    left, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos].kind in {'*', '/'}:
        op = tokens[pos].kind
        right, pos = parse_factor(tokens, pos + 1)
        node = Node('T', production='T -> T * F | T / F')
        node.add_child(left)
        node.add_child(Node(op, value=op))
        node.add_child(right)
        left = node
    return left, pos


def parse_expression(tokens, pos):
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos].kind in {'+', '-'}:
        op = tokens[pos].kind
        right, pos = parse_term(tokens, pos + 1)
        node = Node('E', production='E -> E + T | E - T')
        node.add_child(left)
        node.add_child(Node(op, value=op))
        node.add_child(right)
        left = node
    return left, pos


def evaluate_node(node):
    if node.label == 'F':
        if node.children:
            node.value = evaluate_node(node.children[0])
            return node.value
        return node.value
    if node.label == 'T':
        if len(node.children) == 3:
            left = evaluate_node(node.children[0])
            op = node.children[1].value
            right = evaluate_node(node.children[2])
            if op == '*':
                node.value = left * right
            elif op == '/':
                if right == 0:
                    raise ZeroDivisionError('Division by zero')
                node.value = left / right
            return node.value
        raise ValueError('Malformed T node')
    if node.label == 'E':
        if len(node.children) == 3:
            left = evaluate_node(node.children[0])
            op = node.children[1].value
            right = evaluate_node(node.children[2])
            if op == '+':
                node.value = left + right
            elif op == '-':
                node.value = left - right
            return node.value
        raise ValueError('Malformed E node')
    if node.label in {'+', '-', '*', '/'}:
        return node.value
    return node.value


def evaluate_expression(expr: str):
    try:
        tokens = tokenize(expr)
        if not tokens:
            return None
        tree, pos = parse_expression(tokens, 0)
        if pos != len(tokens):
            return None
        evaluate_node(tree)
        return tree.value
    except Exception:
        return None


def build_q1_experiments():
    expressions = [
        '3', '2 + 3', '5 - 2', '3 * 4', '8 / 2', '3 * (4 + 5) - 6 / 2',
        '2 + 3 * 4', '10 / (2 + 3)', '(1 + 2) * (3 + 4)', '7 - 4 + 2', '3 + 4 * 5 - 6 / 2'
    ]
    rows = []
    for expr in expressions:
        try:
            tokens = tokenize(expr)
            tree, pos = parse_expression(tokens, 0)
            counts = {'node_count': 0}

            def walk(node):
                counts['node_count'] += 1
                for child in node.children:
                    walk(child)

            walk(tree)
            value = evaluate_expression(expr)
            rows.append({
                'expression': expr,
                'length': len(expr),
                'node_count': counts['node_count'],
                'attribute_evaluations': counts['node_count'],
                'result': value,
                'valid': value is not None,
            })
        except Exception:
            rows.append({
                'expression': expr,
                'length': len(expr),
                'node_count': 0,
                'attribute_evaluations': 0,
                'result': None,
                'valid': False,
            })
    return rows


def build_height_results():
    rows = []
    left_exprs = ['1+2', '1+2+3', '1+2+3+4', '1+2+3+4+5']
    right_exprs = ['1+(2+(3+(4+5)))', '1+(2+(3+4))', '1+(2+3)', '1+2']
    for exprs, form in [(left_exprs, 'left'), (right_exprs, 'right')]:
        for expr in exprs:
            tokens = tokenize(expr)
            tree, pos = parse_expression(tokens, 0)

            def height(node):
                if not node.children:
                    return 1
                return 1 + max(height(child) for child in node.children)

            rows.append({'form': form, 'expression': expr, 'height': height(tree)})
    return rows


def generate_q1_outputs():
    out_dir = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q1'
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build_q1_experiments()
    write_csv(out_dir / 'expression_validation.csv', rows)
    write_lines(out_dir / 'summary.txt', [
        'Q1 – Synthesized attributes and annotated parse tree',
        '3 * (4 + 5) - 6 / 2 = 24',
        'The expression is evaluated using bottom-up synthesized values.',
        'The parser preserves precedence and left associativity.'
    ])
    height_rows = build_height_results()
    write_csv(out_dir / 'height_results.csv', height_rows)
    write_lines(out_dir / 'height_summary.txt', [
        'Left-recursive and right-recursive height comparison',
        *[f"{row['form']} | {row['expression']} | height={row['height']}" for row in height_rows]
    ])
    return {'rows': rows, 'height_rows': height_rows, 'status': 'success'}
