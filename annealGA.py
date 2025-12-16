import random
from typing import List, Tuple, Set
from BasicGraph import *
from BinaryGA import *

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

def Anneal_GA(
    G : Graph,
    population_size : int = None,
    theta : float = 0.3,
    max_gen : int = 200,
    verbose : bool = False
) -> Tuple[List[int], int]:
    '''
    Tìm lời giải xấp xỉ cho bài toán Clique lớn nhất (Maximum Clique Problem)
    trên đồ thị G bằng Thuật toán Di truyền lai kết hợp mô phỏng ủ nhiệt.

    Thuật toán tiếp tục cho đến khi độ đa dạng của quần thể giảm xuống
    dưới ngưỡng theta (divers < theta) và gen chạm đến max_gen.

    Args:
        G (Graph): Đối tượng đồ thị đầu vào, có thuộc tính G.n là số đỉnh.
        population_size (int, optional): Kích thước quần thể. Nếu là None,
                                        sẽ được đặt bằng 20 * n (theo bài báo).
                                        Mặc định là None.
        theta (float, optional): Ngưỡng đa dạng (diversity threshold) để dừng thuật toán.
                                 Thuật toán dừng khi đa dạng <= theta. Mặc định là 0.3.
        verbose (bool, optional): Nếu True, sẽ in thông tin cập nhật về thế hệ
                                  và kích thước clique tốt nhất mỗi 50 thế hệ.
                                  Mặc định là False.

    Returns:
        Tuple[List[int], int]: Một tuple chứa:
            - List[int]: Cá thể tốt nhất (best_individual) tìm được, biểu diễn
                         bằng một chuỗi nhị phân [0, 1, ..., 0] có độ dài n.
            - int: Kích thước của clique lớn nhất (best_size) tương ứng.
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

    while divers >= theta or gen < max_gen: 
        # Tính fitness cho toàn bộ quần thể
        fitness_values = [
            fitness_annealed(ind, eps, G) for ind in population
        ]

        # Cập nhật best
        for ind, f in zip(population, fitness_values):
            if edge_score(ind,G) == 1 and f > best_size:
                best_size = f
                best_individual = ind.copy()

        if verbose and gen % 10 == 0:
            print(f"Generation {gen:4d},best clique size = {best_size}")

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

    G = generate_graph_n_p_k(10,0.99,7)
    n = G.n
    
    best_ind, best_size = Anneal_GA(G, population_size = 20 * n, theta = 0.1, max_gen = 1000, verbose = True)

    print("\nBest clique size found:", best_size)
    print("Clique vertices:", [i + 1 for i, bit in enumerate(best_ind) if bit == 1])