from pathlib import Path

from Source_Code.common.dependency_graph import DependencyGraph
from Source_Code.common.utilities import write_lines


def build_expression_dependency_graph():
    g = DependencyGraph()
    for node in ['E.val', 'T.val', 'F1.val', 'F2.val', 'OP1', 'OP2']:
        g.add_node(node)
    g.add_edge('F1.val', 'T.val')
    g.add_edge('F2.val', 'T.val')
    g.add_edge('T.val', 'E.val')
    return g


def build_declaration_dependency_graph():
    g = DependencyGraph()
    for node in ['T.type', 'L.in', 'id1', 'id2', 'D.type']:
        g.add_node(node)
    g.add_edge('T.type', 'L.in')
    g.add_edge('L.in', 'id1')
    g.add_edge('L.in', 'id2')
    g.add_edge('id1', 'D.type')
    g.add_edge('id2', 'D.type')
    return g


def generate_q3_outputs():
    out_dir = Path(__file__).resolve().parents[2] / 'Output_Files' / 'Q3'
    out_dir.mkdir(parents=True, exist_ok=True)
    expr_graph = build_expression_dependency_graph()
    decl_graph = build_declaration_dependency_graph()
    try:
        expression_order = expr_graph.topological_order()
        declaration_order = decl_graph.topological_order()
        lines = [
            'Q3 – Dependency graph and topological evaluation',
            'Expression graph order: ' + ', '.join(expression_order),
            'Declaration graph order: ' + ', '.join(declaration_order),
            'The order obeys dependency constraints and is valid for topological evaluation.'
        ]
        write_lines(out_dir / 'dependency_summary.txt', lines)
        return {'status': 'success', 'expression_order': expression_order, 'declaration_order': declaration_order}
    except ValueError as exc:
        write_lines(out_dir / 'dependency_summary.txt', ['Q3 – Dependency graph and topological evaluation', str(exc)])
        return {'status': 'cycle_detected', 'message': str(exc)}
