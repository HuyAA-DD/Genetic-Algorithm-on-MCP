# Maximum Clique - Branch & Bound 

import sys
from typing import List, Tuple, Set

class Graph:
    def __init__(self, n: int):
        self.n = n
        # Ma trận kề kiểu bool cho dễ kiểm tra cạnh
        self.adj = [[False] * n for _ in range(n)]

    def add_edge(self, u: int, v: int):
        if u == v:
            return
        u = u - 1 #1 base  
        v = v - 1 #1 base 
        self.adj[u][v] = self.adj[v][u] = True

    def has_edge(self, u: int, v: int) -> bool:
        return self.adj[u][v]

# ---------- Đọc đồ thị ----------
def read_graph_from_stdin() -> Graph:
    n, m = map(int, input().split())
    G = Graph(n)

    for _ in range(m):
        x, y = map(int, input().split())
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
            # Nếu là đồ thị vô hướng
            G.add_edge(x,y)

    return G

# ---------- Lấy danh sách kề  ----------
def getadj(G : Graph) -> Tuple[int, List[List[int]]]:
    n = G.n
    adj = [[] for _ in range(n + 1)]

    for x in range(n):
        for y in range(x+1,n):
            if G.has_edge(x,y):
                adj[x].append(y)
                adj[y].append(x)

    # check
    ''''
    for u in range(1, n + 1):
        print(u, ":", adj[u])
    '''
    return n,adj



# ---------- Thuật toán Maximum Clique ----------
def maximum_clique(n, adj):
    # sắp xếp các đỉnh theo thứ tự tăng dần bậc (deg)
    vertices = list(range(1, n + 1))
    vertices.sort(key=lambda v: len(adj[v]))

    best_clique = []  # C*

    def clique(C, P):
        nonlocal best_clique

        # Cắt tỉa: nếu kể cả dùng hết P cũng không vượt được best_clique
        if len(C) + len(P) <= len(best_clique):
            return

        # Cập nhật nghiệm
        if len(C) > len(best_clique):
            best_clique = C.copy()

        # Mở rộng clique
        # Duyệt các đỉnh p trong P theo thứ tự cho trước
        for i, p in enumerate(P):
            # Tạo clique mới C' = C ∪ {p}
            C_new = C + [p]

            # Tạo tập ứng viên mới P' = P \ {p} ∩ N(p)
            # Ở đây mình chỉ lấy các đỉnh đứng SAU p trong P
            # để tránh duyệt lại các nhánh trùng lặp
            tail = P[i + 1:]
            P_new = [v for v in tail if v in adj[p]]

            clique(C_new, P_new)

    # Gọi với C = ∅, P = V theo thứ tự đã sắp xếp
    clique([], vertices)
    return best_clique


# ---------- Chạy chương trình ----------
if __name__ == "__main__":
    G = read_graph_from_stdin()
    n, adj = getadj()
    if n == 0:
        sys.exit(0)

    C_star = maximum_clique(n, adj)
    print(len(C_star))
    print(*C_star)
