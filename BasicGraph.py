import random
from typing import List, Tuple, TextIO

'''
Module này implement 1 graph cơ bản và các hàm liên quan 
'''

class Graph:
    def __init__(self, n: int):
        self.n = n
        # Ma trận kề kiểu bool cho dễ kiểm tra cạnh
        self.adj = [[False] * n for _ in range(n)]

    def add_edge(self, u: int, v: int):
        if u == v:
            return
        self.adj[u][v] = self.adj[v][u] = True

    def has_edge(self, u: int, v: int) -> bool:
        return self.adj[u][v]

# ---------- Đọc đồ thị ----------
def read_graph_from_stdin() -> Graph:
    n, m = map(int, input().split())
    G = Graph(n)

    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1 #1 based to 0-based
        y -= 1 #1 based to 0-based
        # vô hướng
        G.add_edge(x,y)

    # check
    return G 

def read_graph_from_file(filename) -> Graph:
    with open(filename, 'r', encoding='utf-8') as f:
        # Dòng 1: n đỉnh, m cạnh
        n, m = map(int, f.readline().split())
        G = Graph(n)

        # M dòng tiếp: mỗi dòng là 1 cạnh x y
        for _ in range(m):
            x, y = map(int, f.readline().split())
            x -= 1 #1-based to 0-based
            y -= 1 #1-based to 0-based
            # Nếu là đồ thị vô hướng
            G.add_edge(x,y)

    return G

def read_graph_from_clq(filename: str) -> Graph:
    """
    Đọc file DIMACS .clq và trả về Graph
    """
    G = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Comment
            if line.startswith('c'):
                continue

            # Dòng khai báo số đỉnh, số cạnh
            if line.startswith('p'):
                parts = line.split()
                # format: p edge n m
                if parts[1] != 'edge':
                    raise ValueError("Unsupported DIMACS format")
                n = int(parts[2])
                G = Graph(n)

            # Dòng cạnh
            elif line.startswith('e'):
                parts = line.split()
                u = int(parts[1]) - 1 #1-based to 0-based  
                v = int(parts[2]) - 1 #1-based to 0-based 
                G.add_edge(u, v)

    if G is None:
        raise ValueError("File does not contain problem line (p edge ...)")

    return G

# ---------- Lấy danh sách kề  ----------
def getadj(G: Graph) -> Tuple[int, List[List[int]]]:
    n = G.n
    # adj[v] chứa danh sách các đỉnh kề với v (0..n-1)
    adj: List[List[int]] = [[] for _ in range(n)]

    for x in range(n):
        for y in range(x + 1, n):
            if G.has_edge(x, y):
                adj[x].append(y)
                adj[y].append(x)

    return n, adj

def printGraph(G: Graph, file: TextIO = None) -> None:
    '''
    In ra đồ thị G (mặc định ra stdout, hoặc ra file nếu truyền vào)
    '''
    if file is None:
        import sys
        file = sys.stdout

    n = G.n
    m = 0

    for x in range(n):
        for y in range(x+1, n):
            if G.has_edge(x, y):
                m += 1

    print(f"{n} {m}", file=file)
    for x in range(n):
        for y in range(x+1, n):
            if G.has_edge(x, y):
                print(f"{x} {y}", file=file)
    
def generate_graph_n_p_k(n: int, p: float, k: int = 0) -> Graph:
    """
    Tạo đồ thị theo mô tả n/k/p trong bài báo:
    
    - n: tổng số đỉnh
    - p: xác suất thêm cạnh giữa các cặp đỉnh không thuộc clique
    - k: kích thước clique được nhúng
    
    Trả về: một Graph có clique kích thước k.
    """
    G = Graph(n)

    # 1) Chọn ngẫu nhiên k đỉnh để tạo clique
    clique_vertices = random.sample(range(n), k)

    # 2) Thêm clique hoàn chỉnh
    for i in range(k):
        for j in range(i+1, k):
            u = clique_vertices[i]
            v = clique_vertices[j]
            G.add_edge(u, v)

    # 3) Thêm cạnh ngẫu nhiên cho phần còn lại với xác suất p
    for u in range(n):
        for v in range(u+1, n):
            # Đã nằm trong clique → cạnh đã được thêm
            if u in clique_vertices and v in clique_vertices:
                continue

            # Thêm cạnh với xác suất p
            if random.random() < p:
                G.add_edge(u, v)

    return G