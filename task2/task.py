import math
from typing import List, Tuple, Dict, Set


def parse_edges(s: str) -> List[Tuple[int, int]]:

    edges = []
    for line in s.strip().split('\n'):
        if line:
            parts = line.split(',')
            if len(parts) >= 2:
                parent = int(parts[0].strip())
                child = int(parts[1].strip())
                edges.append((parent, child))
    return edges


def build_tree(edges: List[Tuple[int, int]], root: int) -> Tuple[Dict[int, List[int]], List[int]]:

    adj = {}
    nodes = set()

    for parent, child in edges:
        adj.setdefault(parent, []).append(child)
        nodes.update([parent, child])


    nodes.add(root)
    all_nodes = sorted(nodes)


    for node in all_nodes:
        adj.setdefault(node, [])

    return adj, all_nodes


def compute_reachability_matrix(adj: Dict[int, List[int]], nodes: List[int]) -> List[List[bool]]:

    n = len(nodes)
    node_index = {node: idx for idx, node in enumerate(nodes)}
    reachable = [[False] * n for _ in range(n)]


    def dfs(start: int, current: int):
        start_idx = node_index[start]
        current_idx = node_index[current]
        if start != current:
            reachable[start_idx][current_idx] = True

        for child in adj.get(current, []):
            if not reachable[start_idx][node_index[child]]:
                dfs(start, child)

    for node in nodes:
        dfs(node, node)

    return reachable


def compute_entropy_and_complexity(s: str, root_str: str) -> Tuple[float, float]:

    edges = parse_edges(s)
    root = int(root_str)


    adj, all_nodes = build_tree(edges, root)
    n = len(all_nodes)


    reachable = compute_reachability_matrix(adj, all_nodes)


    node_index = {node: idx for idx, node in enumerate(all_nodes)}
    descendant_counts = []

    for i, node in enumerate(all_nodes):
        count = sum(reachable[i])
        descendant_counts.append(count)

    total_descendants = sum(descendant_counts)

    if total_descendants == 0:

        entropy = 0.0
    else:

        entropy = 0.0
        for count in descendant_counts:
            if count > 0:
                p = count / total_descendants
                entropy -= p * math.log2(p)


    if n <= 1:
        normalized = 0.0
    else:

        max_entropy = math.log2(n) if n > 0 else 0

        if max_entropy > 0:
            normalized = entropy / max_entropy
        else:
            normalized = 0.0


    entropy = round(entropy, 1)
    normalized = round(normalized, 1)

    return entropy, normalized


def main(s: str, e: str) -> Tuple[float, float]:

    return compute_entropy_and_complexity(s, e)



if __name__ == "__main__":

    example_csv = "1,2\n1,3\n3,4\n3,5"
    root = "1"

    entropy, complexity = main(example_csv, root)

    print(f"Энтропия структуры: {entropy}")
    print(f"Нормированная структурная сложность: {complexity}")


    example2 = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
    entropy2, complexity2 = main(example2, "1")
    print(f"\nДля большего графа:")
    print(f"Энтропия: {entropy2}")
    print(f"Сложность: {complexity2}")