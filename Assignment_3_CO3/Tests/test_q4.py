from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q4_Syntax_Directed_Translation.infix_to_postfix_sdt import translate_to_postfix, check_mid_production_case


def test_postfix_translation():
    assert translate_to_postfix('a + b * (c - d)') == 'a b c d - * +'
    assert translate_to_postfix('2 + 3 * 4') == '2 3 4 * +'


def test_mid_production_case():
    assert check_mid_production_case() == 'bad: + a b'
