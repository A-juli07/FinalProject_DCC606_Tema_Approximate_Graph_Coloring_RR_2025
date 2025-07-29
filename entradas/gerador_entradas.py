import networkx as nx
import sys

def generate_graphs():
    sizes = [50, 100, 200, 500, 1000, 2000]
    densities = [0.1, 0.3, 0.5]
    
    for n in sizes:
        for d in densities:
            G = nx.gnp_random_graph(n, d)
            filename = f"entradas/bench_{n}_{int(d*100)}.txt"
            with open(filename, 'w') as f:
                f.write(f"{n} {G.number_of_edges()}\n")
                for edge in G.edges():
                    f.write(f"{edge[0]} {edge[1]}\n")

if __name__ == "__main__":
    generate_graphs()