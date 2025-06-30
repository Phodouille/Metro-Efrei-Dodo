import os
import csv
import networkx as nx
import pickle

def load_metro_route_ids(gtfs_dir):
    metro_route_ids = set()
    with open(os.path.join(gtfs_dir, "routes.txt"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("route_type") == "1":
                metro_route_ids.add(row["route_id"])
    return metro_route_ids

def load_metro_trip_ids(gtfs_dir, metro_route_ids):
    metro_trip_ids = set()
    with open(os.path.join(gtfs_dir, "trips.txt"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["route_id"] in metro_route_ids:
                metro_trip_ids.add(row["trip_id"])
    return metro_trip_ids

def load_stops(gtfs_dir, valid_stop_ids):
    stops = {}
    with open(os.path.join(gtfs_dir, "stops.txt"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop_id = row["stop_id"]
            if stop_id.startswith("IDFM") and stop_id in valid_stop_ids:
                stops[stop_id] = row
    return stops

def load_stop_times(gtfs_dir, metro_trip_ids):
    stop_times = {}
    valid_stop_ids = set()
    with open(os.path.join(gtfs_dir, "stop_times.txt"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip_id = row["trip_id"]
            stop_id = row["stop_id"]
            if trip_id in metro_trip_ids and stop_id.startswith("IDFM"):
                stop_sequence = int(row["stop_sequence"])
                arrival = row["arrival_time"]
                departure = row["departure_time"]
                stop_times.setdefault(trip_id, []).append((stop_sequence, stop_id, arrival, departure))
                valid_stop_ids.add(stop_id)
    # Trie les arrêts par séquence pour chaque trip
    for trip_id in stop_times:
        stop_times[trip_id].sort()
    return stop_times, valid_stop_ids

def load_transfers(gtfs_dir, valid_stop_ids):
    transfers = []
    path = os.path.join(gtfs_dir, "transfers.txt")
    if not os.path.exists(path):
        return transfers
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            from_stop = row["from_stop_id"]
            to_stop = row["to_stop_id"]
            if from_stop in valid_stop_ids and to_stop in valid_stop_ids:
                transfers.append(row)
    return transfers

def time_to_seconds(t):
    # Format: HH:MM:SS (peut dépasser 24h)
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

def build_graph_from_gtfs(gtfs_dir):
    metro_route_ids = load_metro_route_ids(gtfs_dir)
    metro_trip_ids = load_metro_trip_ids(gtfs_dir, metro_route_ids)
    stop_times, valid_stop_ids = load_stop_times(gtfs_dir, metro_trip_ids)
    stops = load_stops(gtfs_dir, valid_stop_ids)
    transfers = load_transfers(gtfs_dir, valid_stop_ids)
    G = nx.DiGraph()

    # Ajoute les arrêts comme nœuds
    for stop_id in stops:
        G.add_node(stop_id)

    # Ajoute les arêtes entre arrêts consécutifs d'un même trip
    for trip_id, stops_seq in stop_times.items():
        for i in range(len(stops_seq) - 1):
            _, stop_a, dep_a, _ = stops_seq[i]
            _, stop_b, arr_b, _ = stops_seq[i+1]
            # Calcule le temps de parcours entre les deux arrêts
            try:
                weight = max(1, time_to_seconds(arr_b) - time_to_seconds(dep_a))
            except Exception:
                weight = 60  # Valeur par défaut si parsing échoue
            G.add_edge(stop_a, stop_b, weight=weight, trip_id=trip_id)

    # Ajoute les transferts
    for t in transfers:
        from_stop = t["from_stop_id"]
        to_stop = t["to_stop_id"]
        min_transfer_time = int(t.get("min_transfer_time", 60))
        G.add_edge(from_stop, to_stop, weight=min_transfer_time, transfer=True)

    return G

def save_graph_pickle(G, pickle_path):
    with open(pickle_path, "wb") as f:
        pickle.dump(G, f)

def load_graph_pickle(pickle_path):
    with open(pickle_path, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gtfs_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "data", "gtfs"))
    pickle_path = os.path.join(gtfs_dir, "metro_gtfs_graph.pkl")

    if os.path.exists(pickle_path):
        print("Chargement du graphe depuis le pickle...")
        G = load_graph_pickle(pickle_path)
    else:
        print("Création du graphe à partir des fichiers GTFS...")
        G = build_graph_from_gtfs(gtfs_dir)
        save_graph_pickle(G, pickle_path)
        print(f"Graphe sauvegardé dans {pickle_path}")

    print(f"Nombre de stations: {G.number_of_nodes()}")
    print(f"Nombre de connexions: {G.number_of_edges()}")
    # Exemple : afficher les voisins d'un arrêt
    stop_id = list(G.nodes)[0]
    print(f"Voisins de {stop_id}: {list(G.neighbors(stop_id))}")
