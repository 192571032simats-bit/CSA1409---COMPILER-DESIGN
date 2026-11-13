from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source_Code.Q1_Synthesized_Attributes.synthesized_attributes import generate_q1_outputs
from Source_Code.Q2_Inherited_Attributes.inherited_declarations import generate_q2_outputs
from Source_Code.Q3_Dependency_Graphs.dependency_graph_demo import generate_q3_outputs
from Source_Code.Q4_Syntax_Directed_Translation.infix_to_postfix_sdt import generate_q4_outputs
from Source_Code.Q5_AST_Generation.ast_generation import generate_q5_outputs
from Source_Code.Q6_Advanced_Attributes.advanced_attributes import generate_q6_outputs
from Source_Code.Q7_MiniLang_Translator.minilang_translator import generate_q7_outputs
from Documentation.generate_report import generate_report


def main():
    generate_q1_outputs()
    generate_q2_outputs()
    generate_q3_outputs()
    generate_q4_outputs()
    generate_q5_outputs()
    generate_q6_outputs()
    generate_q7_outputs()
    generate_report()
    print('All Assignment 3 outputs generated successfully.')


if __name__ == '__main__':
    main()
