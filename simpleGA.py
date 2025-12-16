import random
from typing import List, Tuple, Set
from BasicGraph import *
from BinaryGA import*

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

        if verbose and gen % 10 == 0:
            print(f"Generation {gen:4d},best clique size = {best_fitness}")

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

    G = generate_graph_n_p_k(10,0.5)
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
