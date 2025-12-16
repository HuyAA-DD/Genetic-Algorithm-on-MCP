import random
from typing import List, Tuple, Set
'''
Các thao tác cơ bản cho GA:
+ random_individual
+ select
+ crossover
+ mutate
'''
def random_individual(n: int,p : float = 1/8) -> List[int]:
    '''
    Sinh 1 cá thể ngẫu nhiên trong {0,1}^n.
    Ở đây chọn bit 1 với xác suất 0.5 (giống p=1/2 trong bài báo, có thể chỉnh).
    '''
    return [1 if random.random() < p else 0 for _ in range(n)]

def roulette_selection(population: List[List[int]],
                       fitness_values: List[float]) -> List[int]:
    '''
    Reproduction TR(H):
        Chọn 1 cá thể theo phân phối tỉ lệ với fitness.
    Nếu tất cả fitness = 0 thì chọn ngẫu nhiên đều.
    '''
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