import sys
from typing import List, Tuple
from BasicGraph import *


# ---------- Thuật toán Maximum Clique ----------
def maximum_clique(n: int, adj: List[List[int]]) -> Tuple[List[int],int]:
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
    return best_clique, len(best_clique)


# ---------- Chạy chương trình ----------
if __name__ == "__main__":
    G = generate_graph_n_p_k(10,0.5)
    n, adj = getadj(G)
    if n == 0:
        sys.exit(0)

    exact_ind, exact_fit = maximum_clique(n, adj)
    # In số đỉnh và các đỉnh (chuyển lại 1-based nếu cần)
    print(exact_fit)
    print(*[v + 1 for v in exact_ind])