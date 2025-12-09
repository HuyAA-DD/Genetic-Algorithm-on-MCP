from typing import List, Set, Tuple
import random
import math


class Graph:
    def __init__(self, n: int):
        self.n = n
        # Ma trận kề kiểu bool cho dễ kiểm tra cạnh
        self.adj = [[False] * (n+1) for _ in range(n+1)]

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

# -------- evaluation: f(C) = số cạnh trong C --------
def edge_count(G: Graph, C: Set[int]) -> int:
    """f(C) = số cạnh bên trong tập C."""
    C_list = list(C)
    k = len(C_list)
    cnt = 0
    for i in range(k):
        u = C_list[i]
        for j in range(i + 1, k):
            v = C_list[j]
            if G.has_edge(u, v):
                cnt += 1
    return cnt


# -------- local search k-fixed + tabu (maximize f) --------
def tabu_k_fixed_clique(
    G: Graph,
    k: int,
    max_iter: int = 10000,
    tabu_tenure_min: int = 5, #tabu_time min 
    tabu_tenure_max: int = 10, #tabu_tim max
    seed: int = 0, #hệ số kiểm soát sự ngẫu nhiên 
) -> Tuple[Set[int], int]:
    """
    Local search dựa trên k-fixed strategy + tabu list.
    Không gian nghiệm: mọi tập k đỉnh.
    Hàm mục tiêu: f(C) = số cạnh trong C (càng nhiều càng tốt).

    Trả về:
        best_set: tập k đỉnh tốt nhất tìm được
        best_value: f(best_set)
    """
    random.seed(seed)
    n = G.n
    vertices = list(range(n))

    if k > n:
        return set(), -math.inf

    # số cạnh tối đa trong một k-clique
    max_edges = k * (k - 1) // 2

    # --- 1. Khởi tạo nghiệm: chọn ngẫu nhiên k đỉnh ---
    current: Set[int] = set(random.sample(vertices, k))
    current_value = edge_count(G, current)

    best: Set[int] = set(current)
    best_value = current_value

    # tabu_until[i] = iteration trước khi vertex i còn tabu
    tabu_until = [0] * n
    iteration = 0

    while iteration < max_iter and best_value < max_edges:
        iteration += 1

        best_move = None            # (u, v): u∈current, v∉current
        best_move_value = -math.inf

        current_list = list(current)
        outside_list = [v for v in vertices if v not in current]

        if not current_list or not outside_list:
            break  # không còn swap nào

        for u in current_list:
            for v in outside_list:
                move_is_tabu = (
                    iteration < tabu_until[u] or iteration < tabu_until[v]
                )

                # giả lập swap: bỏ u, thêm v
                new_set = set(current)
                new_set.remove(u)
                new_set.add(v)
                new_value = edge_count(G, new_set)

                # Aspiration: nếu move tabu nhưng không cải thiện global best → bỏ qua
                if move_is_tabu and new_value <= best_value:
                    continue

                # Chọn move cho giá trị f lớn nhất
                if new_value > best_move_value:
                    best_move_value = new_value
                    best_move = (u, v)

        if best_move is None:
            # không có move hợp lệ
            break

        # Áp dụng move tốt nhất
        u, v = best_move
        current.remove(u)
        current.add(v)
        current_value = best_move_value

        # Cập nhật tabu tenure cho u và v
        tenure = random.randint(tabu_tenure_min, tabu_tenure_max)
        tabu_until[u] = iteration + tenure
        tabu_until[v] = iteration + tenure

        # Cập nhật global best
        if current_value > best_value:
            best_value = current_value
            best = set(current)

    return best, best_value


# -------- bao ngoài: tăng dần k --------
def max_clique_k_fixed_tabu(
    G: Graph,
    max_iter_per_k: int = 5000,
    seed: int = 0,
) -> Set[int]:
    """
    Tăng dần k, mỗi k chạy local search k-fixed + tabu.
    Khi không tìm được cấu hình k đỉnh với đủ k(k-1)/2 cạnh,
    ta dừng và trả về clique tốt nhất ở k-1.
    """
    random.seed(seed)
    n = G.n
    best_clique: Set[int] = set()

    for k in range(2, n + 1):
        Ck, val = tabu_k_fixed_clique(
            G,
            k,
            max_iter=max_iter_per_k,
            seed=random.randint(0, 10**9),
        )
        max_edges = k * (k - 1) // 2
        if val == max_edges:
            # tìm được k-clique
            best_clique = Ck
        else:
            # không đạt clique cho k này → dừng tại k-1
            break

    return best_clique


# -------- ví dụ dùng thử --------
if __name__ == "__main__":
    # Đồ thị ví dụ 6 đỉnh
    G = read_graph_from_stdin()

    clique = max_clique_k_fixed_tabu(G, max_iter_per_k=3000, seed=42)
    print("Maximum clique found:", clique, "size =", len(clique))
