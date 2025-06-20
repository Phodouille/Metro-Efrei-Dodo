import os


def parse_metro_file(filename):
    graph = {}
    station_names = {}
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header lines until first 'V ' or 'E '
    data_lines = []
    started = False
    for line in lines:
        if line.startswith('V ') or line.startswith('E '):
            started = True
        if started:
            data_lines.append(line)

    # Parse station names and edges
    for line in data_lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('V '):
            # V num_sommet nom_sommet ...
            parts = line.split(' ', 2)
            if len(parts) < 3:
                continue
            station_id = parts[1].zfill(4)
            name_part = parts[2].split(';')[0].strip()
            station_names[station_id] = name_part
        elif line.startswith('E '):
            parts = line.split()
            if len(parts) != 4:
                continue
            _, station1, station2, weight = parts
            station1 = station1.zfill(4)
            station2 = station2.zfill(4)
            try:
                weight = float(weight)
            except ValueError:
                continue
            graph.setdefault(station1, []).append((station2, weight))
            graph.setdefault(station2, []).append((station1, weight))
    return graph, station_names


def visualize_graph(graph, station_names):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    # Par défaut : IDs
    for station_id, neighbors in graph.items():
        for neighbor_id, weight in neighbors:
            G.add_edge(station_id, neighbor_id, weight=weight)

    plt.figure(figsize=(16, 16))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    nx.draw(G, pos, node_size=20, edge_color='gray', with_labels=True, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.title("Visualisation du métro parisien (IDs des stations et poids)")
    plt.show()


def visualize_graph_by_name(graph, station_names):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    for station_id, neighbors in graph.items():
        for neighbor_id, weight in neighbors:
            G.add_edge(
                station_names.get(station_id, station_id),
                station_names.get(neighbor_id, neighbor_id),
                weight=weight
            )
    plt.figure(figsize=(16, 16))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    nx.draw(G, pos, node_size=20, edge_color='gray', with_labels=True, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.title("Visualisation du métro parisien (noms des stations et poids)")
    plt.show()


# Exemple d'utilisation
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "metro.txt")
    graph, station_names = parse_metro_file(data_path)
    print(f"Nombre de stations: {len(graph)}")
    # Affichage avec IDs 
    for station, neighbors in list(graph.items())[:5]:
        print(f"{station}: {[(n, w) for n, w in neighbors]}")
    visualize_graph(graph, station_names)
    # Affichage avec noms
    visualize_graph_by_name(graph, station_names)