from graph_parser import load_graph_from_mysql
import networkx as nx

def build_nx_graph(graph):
    G = nx.Graph()
    for station, neighbors in graph.items():
        for neighbor, line, weight in neighbors:
            G.add_edge(station, neighbor, weight=weight)
    return G

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',
        'database': 'metroefreidodo'
    }
    graph, station_names, station_lines = load_graph_from_mysql(db_config)
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
    
