"""Q1: LL(1) table conflict and FIRST/FOLLOW resolution."""

from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q1_ll1_conflict.txt'


def first_of_sequence(sequence, productions):
    if not sequence:
        return {'epsilon'}
    first = set()
    for symbol in sequence:
        if symbol.islower() or symbol in {'+', '-', '*', '/', '(', ')', 'id', '$', 'a'}:
            first.add(symbol)
            break
        if symbol not in productions:
            first.add(symbol)
            break
        sub_first = set()
        for prod in productions[symbol]:
            sub_first.update(first_of_sequence(prod, productions))
        first |= sub_first - {'epsilon'}
        if 'epsilon' not in sub_first:
            break
    else:
        first.add('epsilon')
    return first


def build_output():
    lines = []
    lines.append('Q1: LL(1) Parsing Table Conflict and FIRST/FOLLOW Analysis')
    lines.append('=' * 68)
    lines.append('Scenario: A student constructs an LL(1) parsing table with multiple entries in one cell.')
    lines.append('Issue: Overlapping FIRST/FOLLOW sets create a deterministic parsing conflict.')
    lines.append('')
    lines.append('Problematic grammar:')
    lines.append('S -> aS | a')
    lines.append('')
    lines.append('FIRST(aS) = {a}')
    lines.append('FIRST(a)  = {a}')
    lines.append('Therefore, M[S, a] contains two entries:')
    lines.append('M[S, a] = { S -> aS, S -> a }')
    lines.append('This is a FIRST/FIRST conflict, so the grammar is not LL(1).')
    lines.append('')
    lines.append('Reason: the syntax analyzer must choose a production using one lookahead token, but the cell has two valid choices.')
    lines.append('Result: deterministic parsing fails, and the parser cannot build a valid predictive table.')
    lines.append('')
    lines.append('Decision: left factoring the grammar produces a valid LL(1) form.')
    lines.append('Left-factored grammar:')
    lines.append('S -> aS\'')
    lines.append("S' -> S | epsilon")
    lines.append('')
    lines.append('FIRST(S) = {a}')
    lines.append("FIRST(S') = {a, epsilon}")
    lines.append('FOLLOW(S) = {$}')
    lines.append("FOLLOW(S') = {$}")
    lines.append('FIRST(S) intersect FOLLOW(S\') = {a} intersect {$} = empty set')
    lines.append('Hence the grammar satisfies LL(1) conditions.')
    lines.append('')
    lines.append('Parsing table after repair:')
    lines.append('Non-terminal   a      $')
    lines.append('S             S -> aS\'')
    lines.append("S'            S' -> S    S' -> epsilon")
    lines.append('')
    lines.append('Input: aa$')
    lines.append('S => aS\'')
    lines.append("S' => S => aS\'")
    lines.append("S' => epsilon")
    lines.append('ACCEPTED -> deterministic LL(1) parsing succeeds.')
    lines.append('')
    lines.append('Conclusion: overlapping FIRST/FOLLOW sets are the source of the conflict; removing left recursion, left factoring, and ambiguity resolves the issue.')
    return '\n'.join(lines)


if __name__ == '__main__':
    output_text = build_output()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output_text, encoding='utf-8')
    print(output_text)
