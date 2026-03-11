'''
Vẽ biểu đồ hội tụ của simpleGA 
So sánh kết quả với thuật toán ExactSearch 
'''

from simpleGA import * 
from ExactSearchMCP import *

if __name__ == "__main__":
    
    G = read_graph_from_file("RandGenGraph/n_64/p_05/graph00.txt")
    n = G.n
    
    for phase in range(5):
        simple_ind, simple_fit_gens = genetic_max_clique(
            G,
            population_size=20*n,
            pm=0.02,
            generations=200,
            verbose=True,
        )
        
        '''
        print("\nBest clique size found:", simple_fit_gens[-1])
        print("Clique vertices:", [i + 1 for i, bit in enumerate(simple_ind) if bit == 1])
        print(f"Runtime: {simple_elapsed:.6f} seconds")
        '''

        #vẽ biểu đồ : 
        simple_fit_gens = np.array(simple_fit_gens)
        plt.plot(simple_fit_gens)
    
    plt.show()