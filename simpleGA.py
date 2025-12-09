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


def is_clique(individual: List[int], G : Graph) -> bool:
    """
    Kiểm tra xem tập các đỉnh có bit = 1 có tạo thành 1 clique không.
    """
    vertices = [i for i, bit in enumerate(individual) if bit == 1]
    k = len(vertices)
    # Mọi cặp (u, v) trong vertices phải có cạnh
    for i in range(k):
        u = vertices[i]
        for j in range(i + 1, k):
            v = vertices[j]
            if G.adj[u][v] == 0:
                return False
    return True


def fitness_simple(individual: List[int], G : Graph) -> int:
    """
    Hàm fitness simple(x):
        k nếu x là clique size k
        0 nếu không phải clique
    """
    vertices = [i for i, bit in enumerate(individual) if bit == 1]
    if not vertices:
        return 0
    if is_clique(individual, G):
        return len(vertices)
    return 0


def random_individual(n: int) -> List[int]:
    """
    Sinh 1 cá thể ngẫu nhiên trong {0,1}^n.
    Ở đây chọn bit 1 với xác suất 0.5 (giống p=1/2 trong bài báo, có thể chỉnh).
    """
    p = 0.5
    return [1 if random.random() < p else 0 for _ in range(n)]


def roulette_selection(population: List[List[int]],
                       fitness_values: List[int]) -> List[int]:
    """
    Reproduction TR(H):
        Chọn 1 cá thể theo phân phối tỉ lệ với fitness.
    Nếu tất cả fitness = 0 thì chọn ngẫu nhiên đều.
    """
    total_f = sum(fitness_values)
    if total_f == 0:
        # Không có cá thể nào tốt hơn -> chọn random
        return random.choice(population)

    r = random.uniform(0, total_f) # xác suất phân phối đều
    acc = 0.0
    for individual, f in zip(population, fitness_values):
        acc += f
        if acc >= r:
            return individual #roulette selection
        
    # Do sai số float, fallback 
    return population[-1]


def crossover_one_point(parent1: List[int],
                        parent2: List[int]) -> List[int]:
    """
    Cross-over TC(H):
        Chọn 1 điểm cắt i ∈ {1, ..., n-1}
        z = x[0:i] + y[i:n]
    (Bài báo dùng 1..n+1, nhưng thường bỏ 2 điểm biên để tránh clone y hệt)
    """
    n = len(parent1)
    if n <= 1:
        return parent1[:]
    cut = random.randint(1, n - 1)
    return parent1[:cut] + parent2[cut:]


def mutate(individual: List[int], pm: float) -> None:
    """
    Mutation TM(H):
        Với xác suất pm, chọn 1 vị trí i random và flip bit.
    """
    if random.random() < pm:
        n = len(individual)
        i = random.randrange(n)
        individual[i] = 1 - individual[i]


def genetic_max_clique(
    G: Graph,
    population_size: int = None,
    pm: float = 0.01,
    generations: int = 1000,
    verbose: bool = False,
) -> Tuple[List[int], int]:
    """
    Cài đặt Simple Genetic Algorithm cho bài toán MAX-CLIQUE
    theo đúng mô tả mục 2.1 trong bài Carter & Park.

    Parameters
    ----------
    G : Graph
        Danh sách kề của đồ thị (neighbors[i] = tập đỉnh kề với i).
    population_size : int
        Kích thước quần thể H(t). Nếu None, dùng quy tắc N = 20n (như bài báo).
    pm : float
        Xác suất mutation.
    generations : int
        Số thế hệ tối đa.
    verbose : bool
        Nếu True, in log.

    Returns
    -------
    best_individual : List[int]
        Cá thể tốt nhất tìm được (mã nhị phân).
    best_fitness : int
        Kích thước clique lớn nhất tìm được.
    """
    n = G.n
    if population_size is None:
        population_size = 20 * n  # như bài báo

    # Khởi tạo quần thể H(0)
    population = [random_individual(n) for _ in range(population_size)] #có thể chỉnh p

    best_individual = None
    best_fitness = 0

    for gen in range(generations):
        
        # Tính fitness cho toàn bộ quần thể
        fitness_values = [
            fitness_simple(ind, G) for ind in population
        ]

        # Cập nhật best
        for ind, f in zip(population, fitness_values):
            if f > best_fitness:
                best_fitness = f
                best_individual = ind.copy()

        if verbose and gen % 50 == 0:
            print(f"Generation {gen:4d},population:{population},best clique size = {best_fitness}")

        # === T = TM ∘ TC ∘ TR ===

        # 1) Reproduction TR(H): tạo quần thể mới bằng roulette selection
        new_population = []
        for _ in range(population_size):
            selected = roulette_selection(population, fitness_values)
            new_population.append(selected[:])  # copy

        # 2) Cross-over TC(H): N lần chọn 2 bố mẹ và lai 1 điểm
        crossed_population = []
        for _ in range(population_size):
            p1 = random.choice(new_population)
            p2 = random.choice(new_population)
            child = crossover_one_point(p1, p2)
            crossed_population.append(child)

        # 3) Mutation TM(H): với xác suất pm, flip 1 bit
        for ind in crossed_population:
            mutate(ind, pm)

        population = crossed_population

    return best_individual, best_fitness


# Ví dụ dùng thử
if __name__ == "__main__":
    #random.seed(0)

    G = read_graph_from_stdin()
    n = G.n
    
    best_ind, best_fit = genetic_max_clique(
        G,
        population_size=20*n,
        pm=0.02,
        generations=1000,
        verbose=True,
    )

    print("\nBest clique size found:", best_fit)
    print("Clique vertices:", [i + 1 for i, bit in enumerate(best_ind) if bit == 1])
