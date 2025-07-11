import os
import mysql.connector
import pickle

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
        if line.startswith('V '):
            # V num_sommet nom_sommet ;line_number ;...
            parts = line.split(' ', 2)
            station_id = parts[1].zfill(4)
            # Split the rest by ';'
            rest = parts[2].split(';')
            name_part = rest[0].strip()
            line_number = rest[1].strip() 
            station_names[station_id] = name_part
            station_lines[station_id] = line_number
        elif line.startswith('E '):
            parts = line.split()
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

# See a non-directed graph with only the station ID
def visualize_graph(graph):
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


def insert_into_mysql(graph, station_names, station_lines, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Créer les tables si elles n'existent pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            id VARCHAR(8) PRIMARY KEY,
            name VARCHAR(255),
            line VARCHAR(16)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            id INT AUTO_INCREMENT PRIMARY KEY,
            station1 VARCHAR(8),
            station2 VARCHAR(8),
            line1 VARCHAR(16),
            line2 VARCHAR(16),
            weight FLOAT,
            FOREIGN KEY (station1) REFERENCES stations(id),
            FOREIGN KEY (station2) REFERENCES stations(id)
        )
    """)

    # Insérer les stations
    for station_id, name in station_names.items():
        line = station_lines.get(station_id)
        cursor.execute("""
            INSERT IGNORE INTO stations (id, name, line) VALUES (%s, %s, %s)
        """, (station_id, name, line))

    # Insérer les arêtes (edges)
    inserted = set()
    for station_id, neighbors in graph.items():
        for neighbor_id, line_number, weight in neighbors:
            key = tuple(sorted([station_id, neighbor_id]))
            if key in inserted:
                continue
            line1 = station_lines.get(station_id)
            line2 = station_lines.get(neighbor_id)
            cursor.execute("""
                INSERT INTO edges (station1, station2, line1, line2, weight)
                VALUES (%s, %s, %s, %s, %s)
            """, (station_id, neighbor_id, line1, line2, weight))
            inserted.add(key)

    conn.commit()
    cursor.close()
    conn.close()

def load_graph_from_mysql(db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Charger les stations
    cursor.execute("SELECT id, name, line FROM stations")
    station_names = {}
    station_lines = {}
    for row in cursor.fetchall():
        station_names[row['id']] = row['name']
        station_lines[row['id']] = row['line']

    # Charger les arêtes sans doublons
    cursor.execute("SELECT station1, station2, line1, line2, weight FROM edges")
    graph = {}
    for row in cursor.fetchall():
        s1 = row['station1']
        s2 = row['station2']
        l1 = row['line1']
        l2 = row['line2']
        w = row['weight']
        # Utilisation d'un set pour garantir l'unicité
        graph.setdefault(s1, set()).add((s2, l2, w))
        graph.setdefault(s2, set()).add((s1, l1, w))

    # Convertir les sets en listes pour compatibilité avec le reste du code
    graph = {k: list(v) for k, v in graph.items()}

    cursor.close()
    conn.close()
    return graph, station_names, station_lines

def save_graph_to_pickle(graph, station_names, station_lines, pickle_path):
    with open(pickle_path, 'wb') as f:
        pickle.dump((graph, station_names, station_lines), f)

def load_graph_from_pickle(pickle_path):
    with open(pickle_path, 'rb') as f:
        return pickle.load(f)

# Exemple d'utilisation
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "metro.txt")
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'metroefreidodo'
    }
    # Place le pickle dans le dossier data
    pickle_path = os.path.join(base_dir, "..", "data", "metro_graph.pkl")

    # Choisir la source des données
    USE_DB = False  # Passe à False pour utiliser le fichier

    # Utilisation du pickle si disponible, sinon création et sauvegarde
    if os.path.exists(pickle_path):
        graph, station_names, station_lines = load_graph_from_pickle(pickle_path)
    else:
        if USE_DB:
            graph, station_names, station_lines = load_graph_from_mysql(db_config)
        else:
            graph, station_names, station_lines = parse_metro_file(data_path)
        save_graph_to_pickle(graph, station_names, station_lines, pickle_path)

    print(f"Nombre de stations: {len(graph)}")
    for station, neighbors in list(graph.items())[:]:
        unique_neighbors = set((n, l, w) for n, l, w in neighbors)
        print(f"Line: {station_lines.get(station)} : {station}: {list(unique_neighbors)}")

    visualize_graph(graph)
    visualize_graph_by_name(graph, station_names)

    # Si tu veux insérer à nouveau dans la base, décommente la ligne suivante :
    # insert_into_mysql(graph, station_names, station_lines, db_config)