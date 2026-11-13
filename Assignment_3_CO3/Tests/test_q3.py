from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q3_Dependency_Graphs.dependency_graph_demo import generate_q3_outputs


def test_dependency_outputs():
    res = generate_q3_outputs()
    assert res['status'] == 'success'
