from graph_parser import load_graph_from_pickle
import os
import networkx as nx

def build_nx_graph(graph):
    G = nx.Graph()
    for station, neighbors in graph.items():
        for neighbor, line, weight in neighbors:
            G.add_edge(station, neighbor, weight=weight)
    return G

def compute_dijkstra_path(graph, start, end):
    """
    Calcule le plus court chemin et son coût entre start et end avec Dijkstra.
    Retourne (chemin, coût) ou (None, None) si pas de chemin.
    """
    G = build_nx_graph(graph)
    try:
        path = nx.dijkstra_path(G, start, end, weight='weight')
        cost = nx.dijkstra_path_length(G, start, end, weight='weight')
        return path, cost
    except nx.NetworkXNoPath:
        return None, None

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_path = os.path.join(base_dir, "..", "data", "metro_graph.pkl")
    graph, station_names, station_lines = load_graph_from_pickle(pickle_path)
    G = build_nx_graph(graph)
    start = '0000'
    end = '0158'
    try:
        path = nx.dijkstra_path(G, start, end, weight='weight')
        cost = nx.dijkstra_path_length(G, start, end, weight='weight')
        print(f"Chemin le plus court de {start} à {end} (coût {cost}):")
        print(" -> ".join(path))
    except nx.NetworkXNoPath:
        print("Aucun chemin trouvé.")
        print(" -> ".join(path))
    except nx.NetworkXNoPath:
        print("Aucun chemin trouvé.")
    
