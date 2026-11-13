from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q2_Inherited_Attributes.inherited_declarations import analyze_declaration_tests


def test_declaration_analysis():
    rows = analyze_declaration_tests()
    assert len(rows) >= 3
    assert any(row['status'] == 'valid' for row in rows)
