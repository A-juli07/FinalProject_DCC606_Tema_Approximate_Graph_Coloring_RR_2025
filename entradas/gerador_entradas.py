import networkx as nx
import os

def salvar_grafo(G, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        f.write(f"{G.number_of_nodes()} {G.number_of_edges()}\n")
        for u, v in G.edges():
            f.write(f"{u} {v}\n")

def carregar_dimacs(path):
    G = nx.Graph()
    with open(path, 'r') as file:
        for line in file:
            if line.startswith('e'):
                _, u, v = line.strip().split()
                G.add_edge(int(u)-1, int(v)-1)
    return G

def generate_graphs():
    sizes = [50, 100, 200, 500, 1000, 2000]
    densities = [0.1, 0.3, 0.5]

    os.makedirs("entradas", exist_ok=True)

    # --- Grafos Aleatórios ---
    for n in sizes:
        for d in densities:
            G = nx.gnp_random_graph(n, d)
            filename = f"entradas/bench_{n}_{int(d*100)}.txt"
            salvar_grafo(G, filename)

    # --- Grafos DIMACS ---
    arquivos_dimacs = {
        "miles1500.col": "miles1500.txt",
        "myciel7.col": "myciel7.txt",
        "queen16_16.col": "queen16_16.txt"
    }

    for arquivo_col, nome_saida in arquivos_dimacs.items():
        path = os.path.join("..", "entradas", arquivo_col)
        if os.path.exists(path):
            print(f"Convertendo {arquivo_col}...")
            G = carregar_dimacs(path)
            salvar_grafo(G, os.path.join("entradas", nome_saida))
        else:
            print(f"[Aviso] Arquivo {arquivo_col} não encontrado. Ignorando.")

if __name__ == "__main__":
    generate_graphs()
