# Maximum Clique - Branch & Bound 

import sys

# ---------- Đọc đồ thị ----------
def read_graph_from_stdin():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        x, y = map(int, input().split())
        # vô hướng
        adj[x].append(y)
        adj[y].append(x)

    # check
    ''''
    for u in range(1, n + 1):
        print(u, ":", adj[u])
    '''
    return n,m,adj

def read_graph_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        # Dòng 1: n đỉnh, m cạnh
        n, m = map(int, f.readline().split())

        # Khởi tạo danh sách kề (1-based)
        adj = [[] for _ in range(n + 1)]

        # M dòng tiếp: mỗi dòng là 1 cạnh x y
        for _ in range(m):
            x, y = map(int, f.readline().split())
            # Nếu là đồ thị vô hướng
            adj[x].append(y)
            adj[y].append(x)

            # Nếu là đồ thị có hướng thì chỉ dùng:
            # adj[x].append(y)

    return n, m, adj

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
    n, m, adj = read_graph_from_stdin()
    if n == 0:
        sys.exit(0)

    C_star = maximum_clique(n, adj)
    print(len(C_star))
    print(*C_star)
