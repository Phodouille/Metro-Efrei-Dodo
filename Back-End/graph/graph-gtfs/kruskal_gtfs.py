import os
import pickle
import networkx as nx

def load_graph_pickle(pickle_path):
    with open(pickle_path, "rb") as f:
        return pickle.load(f)

def load_stop_coords(gtfs_dir):
    import csv
    stops_path = os.path.join(gtfs_dir, "stops.txt")
    coords = {}
    if os.path.exists(stops_path):
        with open(stops_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                coords[row["stop_id"]] = (float(row["stop_lon"]), float(row["stop_lat"]))
    return coords

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gtfs_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "data", "gtfs"))
    pickle_path = os.path.join(gtfs_dir, "metro_gtfs_graph.pkl")

    if not os.path.exists(pickle_path):
        print("Le fichier pickle du graphe n'existe pas.")
        exit(1)

    G = load_graph_pickle(pickle_path)

    # Kruskal sur le graphe pondéré (poids = "weight")
    mst = nx.minimum_spanning_tree(G, weight="weight", algorithm="kruskal")

    print(f"Nombre de sommets dans le MST : {mst.number_of_nodes()}")
    print(f"Nombre d'arêtes dans le MST : {mst.number_of_edges()}")
    print("Quelques arêtes du MST (stop_id1, stop_id2, poids) :")
    for u, v, d in list(mst.edges(data=True))[:5]:
        print(f"{u} -- {v} (poids={d['weight']})")

    # Affiche le nombre d'arêtes retirées et le pourcentage
    nb_edges_removed = G.number_of_edges() - mst.number_of_edges()
    pct_removed = 100 * nb_edges_removed / G.number_of_edges() if G.number_of_edges() else 0
    print(f"Nombre d'arêtes retirées : {nb_edges_removed} ({pct_removed:.2f}%)")

    # Affichage avec matplotlib
    import matplotlib.pyplot as plt

    coords = load_stop_coords(gtfs_dir)
    pos = {n: coords[n] for n in G.nodes if n in coords}
    if pos:
        plt.figure(figsize=(12, 12))
        # Graphe complet en rouge clair
        nx.draw(G, pos, node_size=2, edge_color='red', width=0.2, with_labels=False)
        # MST en bleu par-dessus
        nx.draw(mst, pos, node_size=5, edge_color='blue', width=1, with_labels=False)
        plt.title("Comparaison : Réseau complet (gris) vs MST Kruskal (bleu)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()
    else:
        print("Coordonnées non trouvées pour l'affichage.")
