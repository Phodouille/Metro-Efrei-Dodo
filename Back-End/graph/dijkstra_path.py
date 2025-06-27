from graph_parser import load_graph_from_pickle
import os
import networkx as nx

def build_nx_graph(graph):
    G = nx.Graph()
    for station, neighbors in graph.items():
        for neighbor, line, weight in neighbors:
            G.add_edge(station, neighbor, weight=weight)
    return G

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_path = os.path.join(base_dir, "..", "data", "metro_graph.pkl")
    graph, station_names, station_lines = load_graph_from_pickle(pickle_path)
    G = build_nx_graph(graph)
    start = '0244'
    end = '0363'
    try:
        path = nx.dijkstra_path(G, start, end, weight='weight')
        cost = nx.dijkstra_path_length(G, start, end, weight='weight')
        # Ajoute 30s d'attente pour chaque station intermédiaire (hors départ et arrivée)
        wait_time = 30 * (len(path) - 2) if len(path) > 2 else 0
        total_seconds = cost + wait_time
        minutes = int(round(total_seconds / 60))
        print(f"Chemin le plus court de {start} à {end} ({minutes} min):")
        print(" -> ".join(path))
    except nx.NetworkXNoPath:
        print("Aucun chemin trouvé.")
        print(" -> ".join(path))
    except nx.NetworkXNoPath:
        print("Aucun chemin trouvé.")

