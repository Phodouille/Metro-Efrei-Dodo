from graph_parser import parse_metro_file
import os
import networkx as nx

def build_nx_graph(graph):
    G = nx.Graph()
    for station, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(station, neighbor, weight=weight)
    return G

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "metro.txt")
    graph, _ = parse_metro_file(data_path)
    G = build_nx_graph(graph)
    if nx.is_connected(G):
        print("Le graphe est connexe")
    else:
        print("Le graphe n'est pas connexe")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "metro.txt")
    graph, _ = parse_metro_file(data_path)
  
