import csv
from io import StringIO

def main(csv_string):
    reader = csv.reader(StringIO(csv_string.strip()))
    edges = list(reader)
    if not edges:
        return []
    
    all_vertices = set()
    for edge in edges:
        if len(edge) >= 2:  
            all_vertices.add(int(edge[0]))
            all_vertices.add(int(edge[1]))
    
    if not all_vertices:
        return []
    
    vertices = sorted(all_vertices)
    n = len(vertices)
    
    vertex_to_index = {vertex: idx for idx, vertex in enumerate(vertices)}
    
    adjacency_matrix = [[0] * n for _ in range(n)]
    
    for edge in edges:
        if len(edge) >= 2:
            from_vertex = int(edge[0])
            to_vertex = int(edge[1])
            
            if from_vertex in vertex_to_index and to_vertex in vertex_to_index:
                i = vertex_to_index[from_vertex]
                j = vertex_to_index[to_vertex]
                adjacency_matrix[i][j] = 1
    
    return adjacency_matrix

if __name__ == "__main__":
    example_csv = """0,1
0,2
1,2
2,0
2,3
3,3"""
    
    result = main(example_csv)
    print("Матрица смежности:")
    for row in result:
        print(row)
