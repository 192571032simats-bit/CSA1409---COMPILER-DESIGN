"""Q2: Ambiguous parse tree generation and associativity."""

from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q2_parse_tree.txt'


def build_output():
    lines = []
    lines.append('Q2: Incorrect Parse Tree Generation and Associativity')
    lines.append('=' * 68)
    lines.append('Input: id + id - id')
    lines.append('')
    lines.append('Ambiguous grammar:')
    lines.append('E -> E + E | E - E | id')
    lines.append('')
    lines.append('Right tree (incorrect):')
    lines.append('E')
    lines.append(' / | \\')
    lines.append('id + E')
    lines.append('    / | \\')
    lines.append('   id - id')
    lines.append('Grouping: id + (id - id)')
    lines.append('Evaluation: 5 + (6 - 7) = 4')
    lines.append('')
    lines.append('Left tree (correct):')
    lines.append('E')
    lines.append(' / | \\')
    lines.append('E - id')
    lines.append(' / | \\')
    lines.append('id + id')
    lines.append('Grouping: (id + id) - id')
    lines.append('Evaluation: (5 + 6) - 7 = 4')
    lines.append('')
    lines.append('Issue: the grammar does not specify associativity. As a result, the same input can produce two different parse trees.')
    lines.append('')
    lines.append('Correct design:')
    lines.append('E -> E + T | E - T | T')
    lines.append('T -> id')
    lines.append('This grammar forces left associativity and gives a single parse tree.')
    lines.append('')
    lines.append('Result: correct tree shape is ((id + id) - id), and evaluation is deterministic and accurate.')
    lines.append('')
    lines.append('Conclusion: grammar structure determines tree shape, and associativity must be fixed explicitly to prevent wrong evaluation.')
    return '\n'.join(lines)


if __name__ == '__main__':
    output_text = build_output()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output_text, encoding='utf-8')
    print(output_text)
