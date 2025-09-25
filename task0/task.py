import csv
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python task.py <path_to_csv_file>")
        return []

    csv_file_path = sys.argv[1]

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            edges = list(reader)

        if not edges:
            return []

        all_vertices = set()
        for edge in edges:
            if len(edge) >= 2:
                try:
                    all_vertices.add(int(edge[0]))
                    all_vertices.add(int(edge[1]))
                except ValueError:
                    continue

        if not all_vertices:
            return []

        vertices = sorted(all_vertices)
        n = len(vertices)

        vertex_to_index = {vertex: idx for idx, vertex in enumerate(vertices)}

        adjacency_matrix = [[0] * n for _ in range(n)]

        for edge in edges:
            if len(edge) >= 2:
                try:
                    from_vertex = int(edge[0])
                    to_vertex = int(edge[1])

                    if from_vertex in vertex_to_index and to_vertex in vertex_to_index:
                        i = vertex_to_index[from_vertex]
                        j = vertex_to_index[to_vertex]
                        adjacency_matrix[i][j] = 1
                except ValueError:
                    continue

        return adjacency_matrix

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


if __name__ == "__main__":
    result = main()
    for row in result:
        print(row)