from graph_parser import parse_metro_file
import os
import networkx as nx

def build_nx_graph(graph):
    G = nx.Graph()
    for station, neighbors in graph.items():
        for neighbor_tuple in neighbors:
            neighbor = neighbor_tuple[0]
            weight = neighbor_tuple[-1]
            G.add_edge(station, neighbor, weight=weight)
    return G

def dijkstra_shortest_path(graph, source, target):
    G = build_nx_graph(graph)
    try:
        path = nx.dijkstra_path(G, source, target, weight='weight')
        length = nx.dijkstra_path_length(G, source, target, weight='weight')
        return path, length
    except nx.NetworkXNoPath:
        return None, float('inf')

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "metro.txt")
    # Adapter à la nouvelle signature de parse_metro_file
    result = parse_metro_file(data_path)
    if len(result) == 3:
        graph, station_names, station_lines = result
    else:
        graph, station_names = result
        station_lines = None
    # Exemple : plus court chemin entre deux stations (par ID)
    source = '0000'  # à adapter
    target = '0012'  # à adapter
    path, length = dijkstra_shortest_path(graph, source, target)
    if path:
        print(f"Plus court chemin de {source} à {target} : {path}")
        print(f"Longueur totale : {length} secondes")
    else:
        print(f"Aucun chemin trouvé entre {source} et {target}")
