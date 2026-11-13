from collections import defaultdict, deque


class DependencyGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.indegree = {}

    def add_node(self, node):
        self.graph[node]
        self.indegree.setdefault(node, 0)

    def add_edge(self, source, target):
        self.graph[source].append(target)
        self.indegree.setdefault(source, 0)
        self.indegree[target] = self.indegree.get(target, 0) + 1

    def topological_order(self):
        indegree = dict(self.indegree)
        queue = deque(sorted([n for n, deg in indegree.items() if deg == 0]))
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for nxt in sorted(self.graph.get(node, [])):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        if len(order) != len(indegree):
            cycle_nodes = sorted([n for n in indegree if indegree[n] > 0])
            raise ValueError(f'Cycle detected: {cycle_nodes}')
        return order
