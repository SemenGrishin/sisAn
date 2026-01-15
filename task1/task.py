from typing import List, Tuple
import sys


def parse_edges(s: str):
    edges = []
    for line in s.strip().split('\n'):
        if line:
            parent, child = map(int, line.split(','))
            edges.append((parent, child))
    return edges


def build_tree(edges, root):

    adj = {}
    nodes = set()

    for parent, child in edges:
        adj.setdefault(parent, []).append(child)
        nodes.update([parent, child])

    all_nodes = sorted(nodes)
    for node in all_nodes:
        adj.setdefault(node, [])

    return adj, all_nodes


def get_ancestors(adj, root):
 ancestors = {}

    def dfs(node, path):
        ancestors[node] = set(path)
        for child in adj.get(node, []):
            dfs(child, path + [node])

    dfs(root, [])
    return ancestors


def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:

    edges = parse_edges(s)
    root = int(e)


    adj, all_nodes = build_tree(edges, root)
    node_index = {node: idx for idx, node in enumerate(all_nodes)}
    n = len(all_nodes)


    ancestors = get_ancestors(adj, root)


    def get_descendants(node):
        desc = set()
        stack = [node]
        while stack:
            current = stack.pop()
            for child in adj.get(current, []):
                if child not in desc:
                    desc.add(child)
                    stack.append(child)
        return desc


    R1 = [[False] * n for _ in range(n)]  # родитель -> непосредственный ребенок
    R2 = [[False] * n for _ in range(n)]  # предок -> потомок
    R3 = [[False] * n for _ in range(n)]  # братья/сестры
    R4 = [[False] * n for _ in range(n)]  # вершина -> (себя + потомки)
    R5 = [[False] * n for _ in range(n)]  # вершина -> (себя + предки)


    for parent in all_nodes:
        pi = node_index[parent]

        for child in adj.get(parent, []):
            ci = node_index[child]
            R1[pi][ci] = True
            R2[pi][ci] = True


        descendants = get_descendants(parent)
        for desc in descendants:
            di = node_index[desc]
            R2[pi][di] = True


    parent_of = {}
    for parent in adj:
        for child in adj[parent]:
            parent_of[child] = parent

    for node in all_nodes:
        ni = node_index[node]
        if node in parent_of:
            parent = parent_of[node]
            siblings = [sib for sib in adj.get(parent, []) if sib != node]
            for sib in siblings:
                si = node_index[sib]
                R3[ni][si] = True
                R3[si][ni] = True


    for node in all_nodes:
        ni = node_index[node]
        R4[ni][ni] = True
        descendants = get_descendants(node)
        for desc in descendants:
            di = node_index[desc]
            R4[ni][di] = True


    for node in all_nodes:
        ni = node_index[node]
        R5[ni][ni] = True
        for anc in ancestors.get(node, []):
            ai = node_index[anc]
            R5[ni][ai] = True

    return (R1, R2, R3, R4, R5)



if __name__ == "__main__":

    example_input = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
    root = "1"

    R1, R2, R3, R4, R5 = main(example_input, root)

    print("R1 (родитель -> непосредственный ребенок):")
    for row in R1:
        print([1 if x else 0 for x in row])

    print("\nR2 (предок -> потомок):")
    for row in R2:
        print([1 if x else 0 for x in row])

    print("\nR3 (братья/сестры):")
    for row in R3:
        print([1 if x else 0 for x in row])

    print("\nR4 (вершина -> себя + потомки):")
    for row in R4:
        print([1 if x else 0 for x in row])

    print("\nR5 (вершина -> себя + предки):")
    for row in R5:
        print([1 if x else 0 for x in row])