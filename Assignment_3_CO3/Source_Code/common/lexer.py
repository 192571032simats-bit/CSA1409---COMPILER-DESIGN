from typing import List


class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"Token({self.kind!r}, {self.value!r})"


def tokenize(expr: str) -> List[Token]:
    tokens = []
    expr = expr.strip()
    if not expr:
        return tokens
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit():
            num = ''
            while i < len(expr) and expr[i].isdigit():
                num += expr[i]
                i += 1
            tokens.append(Token('NUMBER', int(num)))
            continue
        if ch.isalpha() or ch == '_':
            name = ''
            while i < len(expr) and (expr[i].isalnum() or expr[i] == '_'):
                name += expr[i]
                i += 1
            tokens.append(Token('ID', name))
            continue
        if ch in '+-*/()=;,':
            tokens.append(Token(ch, ch))
            i += 1
            continue
        raise ValueError(f'Unexpected symbol: {ch}')
    return tokens
