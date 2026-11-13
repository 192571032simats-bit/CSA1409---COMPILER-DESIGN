from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q6_Advanced_Attributes.advanced_attributes import generate_q6_outputs


def test_q6_outputs():
    data = generate_q6_outputs()
    assert 'code' in data
    assert len(data['code']) >= 1
