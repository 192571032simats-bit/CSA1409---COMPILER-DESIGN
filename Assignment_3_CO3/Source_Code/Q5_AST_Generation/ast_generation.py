from pathlib import Path

from Source_Code.common.lexer import tokenize
from Source_Code.common.tree import Node
from Source_Code.common.utilities import write_lines


def parse_expr(tokens, pos=0):
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos].kind in {'+', '-'}:
        op = tokens[pos].kind
        right, pos = parse_term(tokens, pos + 1)
        left = Node('bin_op', children=[left, Node(op, value=op), right], value=op)
    return left, pos


def parse_term(tokens, pos=0):
    left, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos].kind in {'*', '/'}:
        op = tokens[pos].kind
        right, pos = parse_factor(tokens, pos + 1)
        left = Node('bin_op', children=[left, Node(op, value=op), right], value=op)
    return left, pos


def parse_factor(tokens, pos=0):
    tok = tokens[pos]
    if tok.kind == 'NUMBER':
        return Node('num', value=tok.value), pos + 1
    if tok.kind == 'ID':
        return Node('id', value=tok.value), pos + 1
    if tok.kind == '(':
        expr, pos = parse_expr(tokens, pos + 1)
        if tokens[pos].kind != ')':
            raise ValueError('Missing )')
        return expr, pos + 1
    raise ValueError(f'Unexpected token {tok}')


def build_ast(expr):
    tokens = tokenize(expr)
    tree, pos = parse_expr(tokens, 0)
    if pos != len(tokens):
        raise ValueError('Unconsumed input')
    return tree


def count_nodes(node):
    total = 1
    for child in node.children:
        total += count_nodes(child)
    return total


def generate_q5_outputs():
    out_dir = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q5'
    out_dir.mkdir(parents=True, exist_ok=True)
    expr = 'a + b * (c - d)'
    tree = build_ast(expr)
    lines = [
        'Q5 – AST generation',
        f'Expression: {expr}',
        f'AST node count: {count_nodes(tree)}',
        f'AST root: {tree.label} {tree.value}'
    ]
    write_lines(out_dir / 'ast_summary.txt', lines)
    return {'expression': expr, 'node_count': count_nodes(tree), 'status': 'success'}
