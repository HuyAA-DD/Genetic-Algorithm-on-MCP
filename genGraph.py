from BasicGraph import *
from typing import *

def Graph_to_file(n : int = 64) -> None:
   for prob in range(1,11,2):
      for i in range(10):
         num_vert_path = f"n_{n}"
         prob_path = f"p_0{prob}"
         id_path = "graph0" + str(i) + ".txt"
         
         relative_path = f"RandGenGraph/{num_vert_path}/{prob_path}/{id_path}"
         #print(relative_path)
         f  = open(relative_path,"w")
         p = float(prob) / 10
         G  = generate_graph_n_p_k(n,p)
         printGraph(G,f)
         f.close()


if __name__ == "__main__":
   print("Are you sure want to generate new graph set ?")
   choice = input(f"To confirm, press [Y]: ")
   if choice == "Y":
      print("Confirmed")
      Graph_to_file()
   else: 
      print("Canceled")
   

