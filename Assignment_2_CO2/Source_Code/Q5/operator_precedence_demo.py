"""Q5: Operator precedence conflict and resolution."""

from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q5_operator_precedence.txt'


def build_output():
    lines = []
    lines.append('Q5: Operator Precedence Conflict and Grammar Redesign')
    lines.append('=' * 68)
    lines.append('Ambiguous grammar:')
    lines.append('E -> E + E | E * E | id')
    lines.append('Input: id + id * id')
    lines.append('')
    lines.append('Two possible groupings exist:')
    lines.append('1. id + (id * id) -> correct because * has higher precedence than +')
    lines.append('2. (id + id) * id -> wrong because + is evaluated before *')
    lines.append('')
    lines.append('Issue: the grammar gives equal precedence to + and *, so a shift/reduce conflict appears.')
    lines.append('The parser cannot decide whether to reduce or shift when it sees `*` after `E + E`.')
    lines.append('')
    lines.append('Correct precedence-based grammar:')
    lines.append('E -> E + T | T')
    lines.append('T -> T * F | F')
    lines.append('F -> id')
    lines.append('')
    lines.append('This enforces:')
    lines.append('1. `*` is evaluated before `+` because `T` appears one level below `E`.')
    lines.append('2. Left associativity is preserved by left-recursive rules.')
    lines.append('3. The parse tree is unique and evaluation is consistent.')
    lines.append('')
    lines.append('Correct evaluation:')
    lines.append('id + (id * id) = 5 + (6 * 7) = 47')
    lines.append('')
    lines.append('Conclusion: precedence and associativity must be encoded in the grammar or by parser declarations so that the same expression yields one parse tree and one evaluation.')
    return '\n'.join(lines)


if __name__ == '__main__':
    output_text = build_output()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output_text, encoding='utf-8')
    print(output_text)
