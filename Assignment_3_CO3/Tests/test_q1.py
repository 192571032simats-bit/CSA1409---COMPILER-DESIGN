from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q1_Synthesized_Attributes.synthesized_attributes import evaluate_expression, build_q1_experiments


def test_basic_expression_values():
    assert evaluate_expression('3 * (4 + 5) - 6 / 2') == 24
    assert evaluate_expression('2 + 3 * 4') == 14


def test_invalid_and_div_zero():
    assert evaluate_expression('3 +') is None
    assert evaluate_expression('8 / 0') is None


def test_experimental_summary():
    rows = build_q1_experiments()
    assert len(rows) >= 10
