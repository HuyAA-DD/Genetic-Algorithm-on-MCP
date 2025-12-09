import random
from typing import List, Tuple, Set

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
    
def generate_graph_n_k_p(n: int, k: int, p: float) -> Graph:
    """
    Tạo đồ thị theo mô tả n/k/p trong bài báo:
    
    - n: tổng số đỉnh
    - k: kích thước clique được nhúng
    - p: xác suất thêm cạnh giữa các cặp đỉnh không thuộc clique
    
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

if __name__ == "__main__":
    N, K, P = input().split()
    N = int(N)
    K = int(K)
    P = float(P)

    G = generate_graph_n_k_p(N,K,P)

    M = int(0)

    for x in range(N):
        for y in range(x+1,N):
            if G.has_edge(x,y):
                M += 1

    print(str(N) + ' ' + str(M))
    for x in range(N):
        for y in range(x+1,N):
            if G.has_edge(x,y):
                print(str(x+1) + ' ' + str(y+1))
