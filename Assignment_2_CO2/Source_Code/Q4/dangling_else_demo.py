"""Q4: Dangling else ambiguity and nearest-then resolution."""

from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q4_dangling_else.txt'


def build_output():
    lines = []
    lines.append('Q4: Dangling Else Problem and Resolution')
    lines.append('=' * 68)
    lines.append('Grammar:')
    lines.append('S -> if E then S | if E then S else S | a')
    lines.append('')
    lines.append('Input: if E1 then if E2 then a else a')
    lines.append('This creates two valid parse trees:')
    lines.append('1) else belongs to the inner if')
    lines.append('2) else belongs to the outer if')
    lines.append('')
    lines.append('The second tree is the ambiguous one, and the grammar is not conflict-free.')
    lines.append('The parser cannot decide which `if` the `else` should attach to with a single lookahead token.')
    lines.append('')
    lines.append('This is the classic dangling else problem.')
    lines.append('')
    lines.append('Nearest-then rule:')
    lines.append('Every else attaches to the nearest unmatched then.')
    lines.append('Under this rule, the else joins the inner if.')
    lines.append('')
    lines.append('Recommended reconstruction:')
    lines.append('S -> M | U')
    lines.append('M -> if E then M else M | a')
    lines.append('U -> if E then S | if E then M else U')
    lines.append('')
    lines.append('This rule set removes ambiguity and ensures a single, deterministic parse tree.')
    lines.append('')
    lines.append('Conclusion: the dangling else is a shift/reduce conflict in LR parsing and must be resolved by grammar redesign or by the nearest-then convention.')
    return '\n'.join(lines)


if __name__ == '__main__':
    output_text = build_output()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output_text, encoding='utf-8')
    print(output_text)
