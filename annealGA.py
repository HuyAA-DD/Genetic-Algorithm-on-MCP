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

def edge_score(individual: List[int], G: Graph) -> float:
    '''
    Hàm edge_score :
    số cạnh có trong cá thể / số cạnh của clique ứng với só đỉnh trong cá thể 
    '''
    vertices = [i for i, bit in enumerate(individual) if bit == 1]
    if not vertices:
       return 0
    
    k = len(vertices)

    if k == 1:
        return 1

    clique_edge = k * (k - 1) / 2
    count_edge = 0 # Đếm số cạnh trong cá thể 
    for i in range(k):
        u = vertices[i]
        for j in range(i+1,k):
            v = vertices[j]
            if G.has_edge(u,v):
                count_edge = count_edge + 1

    return count_edge / clique_edge

def fitness_annealed(individual : List[int], epsilon : float, G : Graph) -> float:
    vertices = [i for i, bit in enumerate(individual) if bit == 1]
    k = len(vertices)
    p = edge_score(individual,G)
    return (p**epsilon) * k

def epsilon_T(population: List[List[int]], epsilon: float, G: Graph) -> float:
    """
    Cập nhật epsilon theo hiệu năng hiện tại của quần thể.
    """
    ca = 0.35  # tốc độ anneal
    max_all = 0.0         # max fitness_annealed
    max_clique = 0.0 # kích thước clique tốt nhất (thật sự)

    for individual in population:
        f = fitness_annealed(individual, epsilon, G)
        if f > max_all:
            max_all = f

        # Nếu cá thể là clique (edge_score == 1), cập nhật size
        if edge_score(individual, G) == 1.0:
            k = sum(individual)  # số đỉnh
            if k > max_clique:
                max_clique = k

    if max_all == 0:
        # chưa có gì tốt → giữ nguyên epsilon
        return epsilon

    factor = 1.0 + ca * (max_all - max_clique) / max_all
    return epsilon * factor

def diversity_T(population : List[List[int]], num_vertices : int,population_size : int) -> float:
    if not population:
        return 0
    
    sum_point = 0
    for i in range(num_vertices):
        point = 0
        for individual in population:
            point += individual[i]
        if population_size - point > point:
            point = population_size - point
        sum_point += point

    div = sum_point / (num_vertices * population_size)
    div = 2 * (1 - div)
    return div

def random_individual(n: int) -> List[int]:
    """
    Sinh 1 cá thể ngẫu nhiên trong {0,1}^n.
    Ở đây chọn bit 1 với xác suất 0.5 (giống p=1/2 trong bài báo, có thể chỉnh).
    """
    p = 0.5
    return [1 if random.random() < p else 0 for _ in range(n)]


def roulette_selection(population: List[List[int]],
                       fitness_values: List[float]) -> List[int]:
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
    '''
    Cross-over TC(H):
        Chọn 1 điểm cắt i ∈ {1, ..., n-1}
        z = x[0:i] + y[i:n]
    (Bài báo dùng 1..n+1, nhưng thường bỏ 2 điểm biên để tránh clone y hệt)
    '''
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

def Anneal_GA(G : Graph, population_size : int = None, theta : float = 0.3, verbose : bool = False) -> Tuple[List[int], int]:
    '''
    Docstring for Anneal_GA
    
    :param G: Description
    :type G: Graph
    :param population_size: Description
    :type population_size: int
    :param theta: Description
    :type theta: float
    :param verbose: Description
    :type verbose: bool
    :return: Description
    :rtype: Tuple[List[int], int]
    '''
    n = G.n
    if population_size is None:
        population_size = 20 * n  # như bài báo

    # Khởi tạo quần thể H(0)
    population = [random_individual(n) for _ in range(population_size)] #có thể chỉnh p
    
    best_individual = None
    best_size = 0
    divers = diversity_T(population,n,population_size)
    eps = 1.05
    gen = 0

    while divers >= theta:
        # Tính fitness cho toàn bộ quần thể
        fitness_values = [
            fitness_annealed(ind, eps, G) for ind in population
        ]

        # Cập nhật best
        for ind, f in zip(population, fitness_values):
            if edge_score(ind,G) == 1 and f > best_size:
                best_size = f
                best_individual = ind.copy()

        if verbose and gen % 50 == 0:
            print(f"Generation {gen:4d},population:{population},best clique size = {best_size}")

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

        population = crossed_population

        # cập nhật lại độ đa dạng quần thể 
        divers = diversity_T(population,n,population_size)

        # cập nhật lại hệ số tôi ủ 
        eps = epsilon_T(population,eps,G)

        # cập nhật lại số thế hệ 
        gen += 1

    if best_size == 0:
        best_individual = [0] * n
    return best_individual,best_size


if __name__ == "__main__":
    #random.seed(0)

    G = read_graph_from_stdin()
    n = G.n
    
    best_ind, best_size = Anneal_GA(G, population_size = 20 * n, theta = 0.1, verbose = True)

    print("\nBest clique size found:", best_size)
    print("Clique vertices:", [i + 1 for i, bit in enumerate(best_ind) if bit == 1])