from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q7_MiniLang_Translator.minilang_translator import generate_q7_outputs


def test_q7_outputs():
    result = generate_q7_outputs()
    assert result['generated_code']
