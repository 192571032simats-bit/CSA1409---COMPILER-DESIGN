from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q5_AST_Generation.ast_generation import generate_q5_outputs


def test_ast_generation():
    result = generate_q5_outputs()
    assert result['node_count'] >= 1
