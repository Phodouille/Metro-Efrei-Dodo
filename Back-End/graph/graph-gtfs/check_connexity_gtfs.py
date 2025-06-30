import os
import pickle
import networkx as nx

def load_graph_pickle(pickle_path):
    with open(pickle_path, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gtfs_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "data", "gtfs"))
    pickle_path = os.path.join(gtfs_dir, "metro_gtfs_graph.pkl")

    if not os.path.exists(pickle_path):
        print("Le fichier pickle du graphe n'existe pas.")
        exit(1)

    G = load_graph_pickle(pickle_path)

    if nx.is_connected(G):
        print("Le graphe métro IDFM est connexe.")
    else:
        print("Le graphe métro IDFM N'EST PAS connexe.")
        components = list(nx.connected_components(G))
        print(f"Nombre de composantes connexes : {len(components)}")
        print(f"Taille de la plus grande composante : {len(max(components, key=len))}")
