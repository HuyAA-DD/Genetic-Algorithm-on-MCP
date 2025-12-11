import sys
from typing import List, Tuple

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
        # input 1-based -> chuyển về 0-based
        x -= 1
        y -= 1
        G.add_edge(x, y)

    return G


def read_graph_from_file(filename) -> Graph:
    with open(filename, 'r', encoding='utf-8') as f:
        n, m = map(int, f.readline().split())
        G = Graph(n)

        for _ in range(m):
            x, y = map(int, f.readline().split())
            x -= 1
            y -= 1
            G.add_edge(x, y)

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


# ---------- Thuật toán Maximum Clique ----------
def maximum_clique(n: int, adj: List[List[int]]) -> List[int]:
    # các đỉnh: 0..n-1
    vertices = list(range(n))

    # sắp xếp theo bậc tăng dần
    vertices.sort(key=lambda v: len(adj[v]))

    best_clique: List[int] = []  # C*

    def clique(C: List[int], P: List[int]):
        nonlocal best_clique

        # Cắt tỉa: kể cả lấy hết P cũng không vượt được best_clique
        if len(C) + len(P) <= len(best_clique):
            return

        # Cập nhật nghiệm tốt nhất
        if len(C) > len(best_clique):
            best_clique = C.copy()

        # Mở rộng clique
        for i, p in enumerate(P):
            C_new = C + [p]

            tail = P[i + 1:]
            neighbors_p = adj[p]
            # chỉ giữ lại các đỉnh kề với p
            P_new = [v for v in tail if v in neighbors_p]

            clique(C_new, P_new)

    clique([], vertices)
    return best_clique


# ---------- Chạy chương trình ----------
if __name__ == "__main__":
    G = read_graph_from_stdin()
    n, adj = getadj(G)
    if n == 0:
        sys.exit(0)

    C_star = maximum_clique(n, adj)
    # In số đỉnh và các đỉnh (chuyển lại 1-based nếu cần)
    print(len(C_star))
    print(*[v + 1 for v in C_star])