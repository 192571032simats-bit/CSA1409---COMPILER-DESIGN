from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT1 = ROOT / 'Output_Files' / 'Q2_recursive_descent.txt'
OUT2 = ROOT / 'Output_Files' / 'Q2_ll1_parsing.txt'

content1 = '''Q2: Left recursion, left factoring, FIRST/FOLLOW and recursive descent
=====================================================================

Original grammar fragment:
E -> E + T | T
T -> T * F | F
F -> id | (E)

Step 1: left-recursion elimination (for top-down parsers)
E -> T E'
E' -> + T E' | eps
T -> F T'
T' -> * F T' | eps
F -> id | (E)

Step 2: left factoring
The grammar is already left-factored after elimination.

FIRST sets:
FIRST(E) = {id, (}
FIRST(E') = {+, eps}
FIRST(T) = {id, (}
FIRST(T') = {*, eps}
FIRST(F) = {id, (}

FOLLOW sets:
FOLLOW(E) = {$, )}
FOLLOW(E') = {$, )}
FOLLOW(T) = {+, ), $}
FOLLOW(T') = {+, ), $}
FOLLOW(F) = {*, +, ), $}

Recursive-descent pseudocode:
parse_E():
    parse_T()
    while lookahead == '+':
        match('+')
        parse_T()

parse_T():
    parse_F()
    while lookahead == '*':
        match('*')
        parse_F()

parse_F():
    if lookahead == 'id': match('id')
    elif lookahead == '(':
        match('(')
        parse_E()
        match(')')
    else: error('expected id or (')

Call trace for input: id + id * id
----------------------------------
parse_E -> parse_T -> parse_F -> match id
parse_E sees + -> match +
parse_T -> parse_F -> match id
parse_T sees * -> match *
parse_F -> match id
accept

Invalid input detection:
Input: id + * id
Error occurs when parse_T expects an operand after + and sees *.
Exact detection point: before consuming *, the parser has a valid prefix id + and the next token * cannot start an operand.
'''

content2 = '''Q2: LL(1) table and stack trace
=================================

Grammar after rewrite:
E -> T E'
E' -> + T E' | eps
T -> F T'
T' -> * F T' | eps
F -> id | (E)

LL(1) predictive table (selected entries):
M[E, id] = E -> T E'
M[E, (] = E -> T E'
M[E', +] = E' -> + T E'
M[E', )] = E' -> eps
M[E', $] = E' -> eps
M[T, id] = T -> F T'
M[T, (] = T -> F T'
M[T', *] = T' -> * F T'
M[T', +] = T' -> eps
M[T', )] = T' -> eps
M[T', $] = T' -> eps
M[F, id] = F -> id
M[F, (] = F -> (E)

Stack-based parse for id + id * id$
------------------------------------
Stack                Input                     Action
$E                   id + id * id$            E -> T E'
$E'T                 id + id * id$            T -> F T'
$E'T'F               id + id * id$            F -> id
$E'T'                + id * id$               match id
$E'                  + id * id$               E' -> + T E'
$E'T                 id * id$                 T -> F T'
$E'T'F               id * id$                 F -> id
$E'T'                * id$                    T' -> * F T'
$E'T'F               id$                      F -> id
$E'T'                $                        T' -> eps
$E'                  $                        E' -> eps
$                    $                        ACCEPT
'''
OUT1.parent.mkdir(parents=True, exist_ok=True)
OUT1.write_text(content1, encoding='utf-8')
OUT2.write_text(content2, encoding='utf-8')
print('Q2 outputs generated')
