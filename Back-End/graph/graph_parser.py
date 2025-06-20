import os

def parse_metro_file(filename):
    graph = {}
    station_names = {}
    station_lines = {}
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header lines until first 'V ' or 'E '
    data_lines = []
    for line in range (len(lines)):
        if line > 14:
            if lines[line].startswith('V ') or lines[line].startswith('E '):
                data_lines.append(lines[line])
            else:
                continue
        else:
            continue

    # Parse station names, lines, and edges
    for line in data_lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('V '):
            # V num_sommet nom_sommet ;line_number ;...
            parts = line.split(' ', 2)
            if len(parts) < 3:
                continue
            station_id = parts[1].zfill(4)
            # Split the rest by ';'
            rest = parts[2].split(';')
            name_part = rest[0].strip()
            line_number = rest[1].strip() if len(rest) > 1 else None
            station_names[station_id] = name_part
            station_lines[station_id] = line_number
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
            # Add line number before weight in the tuple
            line1 = station_lines.get(station1)
            line2 = station_lines.get(station2)
            graph.setdefault(station1, []).append((station2, line2, weight))
            graph.setdefault(station2, []).append((station1, line1, weight))
    return graph, station_names, station_lines


def visualize_graph(graph, station_names):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    # Par défaut : IDs
    for station_id, neighbors in graph.items():
        for neighbor_id, line_number, weight in neighbors:
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
        for neighbor_id, line_number, weight in neighbors:
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
    graph, station_names, station_lines = parse_metro_file(data_path)
    print(f"Nombre de stations: {len(graph)}")
    # Affichage avec IDs 
    for station, neighbors in list(graph.items())[:5]:
        print(f"Line: {station_lines.get(station)} : {station}: {[(n, l, w) for n, l, w in neighbors]}")
    visualize_graph(graph, station_names)
    # Affichage avec noms
    visualize_graph_by_name(graph, station_names)