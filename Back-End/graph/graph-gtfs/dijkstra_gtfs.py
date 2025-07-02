import os
import pickle
import networkx as nx

def load_graph_pickle(pickle_path):
    with open(pickle_path, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gtfs_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "data", "gtfs"))
    pickle_path = os.path.join(gtfs_dir, "metro_gtfs_graph.pkl")

    if not os.path.exists(pickle_path):
        print("Le fichier pickle du graphe n'existe pas.")
        exit(1)

    G = load_graph_pickle(pickle_path)

    # Aller de Villejuif Louis Aragon à Chatelet (ligne 7)
    # Remplacez les valeurs ci-dessous par les stop_id exacts de ces stations dans votre GTFS
    start = "IDFM:21907"    
    end = "IDFM:21940"     

    # Vérification : affichez les stop_id présents dans le graphe pour comprendre le format attendu
    if start not in G or end not in G:
        print("Les stop_id de départ ou d'arrivée n'existent pas dans le graphe.")
        print("Exemples de stop_id disponibles dans le graphe :")
        for i, sid in enumerate(list(G.nodes)[:20]):
            print(f"  {sid}")
        print(f"Nombre total de stop_id dans le graphe : {len(G.nodes)}")
        # Affichez aussi les stop_id contenant 'Villejuif' ou 'Chatelet' pour aider à trouver le bon identifiant
        print("\nStop_id contenant 'Villejuif' :")
        for sid in G.nodes:
            if "Villejuif" in sid.lower():
                print(f"  {sid}")
        print("\nStop_id contenant 'Chatelet' :")
        for sid in G.nodes:
            if "Châtelet" in sid.lower():
                print(f"  {sid}")
        exit(1)

    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        cost = nx.dijkstra_path_length(G, start, end, weight="weight")
        # Charger les noms des stations
        stops_path = os.path.join(gtfs_dir, "stops.txt")
        stop_names = {}
        if os.path.exists(stops_path):
            import csv
            with open(stops_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    stop_names[row["stop_id"]] = row["stop_name"]
        print(f"Chemin le plus court de {start} à {end} (coût total : {cost} secondes) :")
        last_name = None
        for sid in path:
            name = stop_names.get(sid, "")
            if name != last_name:
                print(f"{sid} - {name}")
                last_name = name
    except nx.NetworkXNoPath:
        print("Aucun chemin trouvé entre les deux stations.")
