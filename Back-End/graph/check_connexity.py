from graph_parser import load_graph_from_pickle
import os
import networkx as nx

def build_nx_graph(graph):
    G = nx.Graph()
    for station, neighbors in graph.items():
        for neighbor_tuple in neighbors:
            # Prend toujours le premier et le dernier élément du tuple (id voisin, poids)
            neighbor = neighbor_tuple[0]
            weight = neighbor_tuple[-1]
            G.add_edge(station, neighbor, weight=weight)
    return G

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_path = os.path.join(base_dir, "..", "data", "metro_graph.pkl")
    graph, station_names, station_lines = load_graph_from_pickle(pickle_path)
    G = build_nx_graph(graph)
    if nx.is_connected(G):
        print("Le graphe est connexe")
    else:
        print("Le graphe n'est pas connexe")


