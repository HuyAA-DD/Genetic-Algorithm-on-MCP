from BasicGraph import *
from typing import *
import os

def ToDotfile(G: Graph, filename : str = None) -> None:
    '''
    Xuất ra file chuyển đồ thị G thành file .dot (Từ đó render ra ảnh bằng graphviz)
    '''
    file : TextIO = None
    if filename is None:
        import sys
        file = sys.stdout
    #Có thể thêm điều kiện check xem file name có phải file .dot không 
    file = open(filename,"w")

    n = G.n

    print("Graph G {",file=file)
    print("layout=sfdp;\noverlap=false;\nnode [shape=circle, width=0.3, fontsize=10];\nedge [color=gray];",file=file)
    for x in range(n):
        for y in range(x+1, n):
            if G.has_edge(x, y):
                print(f"    {x} -- {y}", file=file)
    print("}",file=file)
    file.close()



def Graph_to_file(n : int = 64) -> None:
   for prob in range(1,11,2):
      for i in range(10):
         num_vert_path = f"n_{n}"
         prob_path = f"p_0{prob}"
         id_path = "graph0" + str(i)
         
         txt_path = f"RandGenGraph/{num_vert_path}/{prob_path}/{id_path}" + ".txt"
         dot_path = f"RandGenGraph/{num_vert_path}/{prob_path}/{id_path}" + ".dot"
         png_path = f"RandGenGraph/{num_vert_path}/{prob_path}/{id_path}" + ".png"
         #print(relative_path)
   
         p = float(prob) / 10
         G  = generate_graph_n_p_k(n,p)
         printGraph(G,txt_path)
         ToDotfile(G,dot_path)
         os.system(f"sfdp -Tpng {dot_path} -o {png_path}")


if __name__ == "__main__":
   print("Are you sure want to generate new graph set ?")
   choice = input(f"To confirm, press [Y]: ")
   if choice == "Y":
      print("Confirmed")
      Graph_to_file()
   else: 
      print("Canceled")
   

