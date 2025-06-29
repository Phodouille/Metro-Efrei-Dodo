import os
import networkx as nx
import matplotlib.pyplot as plt
from graph_parser import load_graph_from_pickle

def build_nx_graph(graph):
    G = nx.Graph()
    for station, neighbors in graph.items():
        for neighbor, line, weight in neighbors:
            G.add_edge(station, neighbor, weight=weight)
    return G

def visualize_mst(G_mst, station_names):
    pos = nx.spring_layout(G_mst, k=0.25, iterations=100)
    plt.figure(figsize=(30, 30))
    nx.draw(G_mst, pos, with_labels=True, node_size=30, font_size=8)
    edge_labels = nx.get_edge_attributes(G_mst, 'weight')
    nx.draw_networkx_edge_labels(G_mst, pos, edge_labels=edge_labels, font_size=6)
    plt.title("Arbre couvrant minimal du réseau métro parisien (Kruskal)")
    plt.margins(0.05)
    plt.show()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_path = os.path.join(base_dir, "..", "data", "metro_graph.pkl")
    
    graph, station_names, station_lines = load_graph_from_pickle(pickle_path)
    G = build_nx_graph(graph)

    # Appliquer Kruskal avec NetworkX
    mst = nx.minimum_spanning_tree(G, weight='weight')

    print("Arbre couvrant minimal (ACPM - Kruskal) :")
    for u, v, data in mst.edges(data=True):
        print(f"{station_names[u]} ↔ {station_names[v]} : {int(data['weight'])} s")

    print(f"\nNombre total d’arêtes dans l’arbre : {len(mst.edges())}")
    visualize_mst(mst, station_names)


