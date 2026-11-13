"""Q3: Syntax error detection and recovery for missing operand."""

from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q3_error_handling.txt'


def build_output():
    lines = []
    lines.append('Q3: Invalid Expression Handling and Error Recovery')
    lines.append('=' * 68)
    lines.append('Input tokens: id + * id')
    lines.append('Lexical analysis succeeds: id, +, *, id are all valid tokens.')
    lines.append('But the token arrangement is invalid, so a syntax error occurs.')
    lines.append('')
    lines.append('Grammar:')
    lines.append('E -> E + T | T')
    lines.append('T -> T * F | F')
    lines.append('F -> (E) | id')
    lines.append('')
    lines.append('Predictive parsing observation:')
    lines.append('After matching `id +`, the parser expects an operand before `*`.')
    lines.append('The grammar allows `T -> F` and `F -> id`, but `*` cannot begin an operand.')
    lines.append('Therefore, at the lookahead `*`, the parsing table has no entry and an error is raised.')
    lines.append('')
    lines.append('Error report:')
    lines.append('Syntax error at "*": operand expected after "+"')
    lines.append('')
    lines.append('Recovery techniques:')
    lines.append('1. Panic mode: discard tokens until a synchronizing token is reached.')
    lines.append('2. Phrase-level recovery: insert the missing operand id before *.')
    lines.append('3. Error productions: E -> E + error')
    lines.append('')
    lines.append('Recovery result:')
    lines.append('Panic mode: skip "*" and continue parsing with valid expression `id + id`.')
    lines.append('Phrase level: insert `id` before `*` to recover the valid form `id + id * id`.')
    lines.append('')
    lines.append('Conclusion: a good parser reports the exact error, recovers quickly, and avoids cascading false errors.')
    return '\n'.join(lines)


if __name__ == '__main__':
    output_text = build_output()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output_text, encoding='utf-8')
    print(output_text)
