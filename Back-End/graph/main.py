from flask import Flask, jsonify, request
import sys
import os
import json
import networkx as nx
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from graph_parser import load_graph_from_pickle

app = Flask(__name__)
CORS(app)  # autorise les requêtes depuis Vue.js en local

# 🔁 Chargement des fichiers
base_dir = os.path.dirname(os.path.abspath(__file__))
pickle_path = os.path.join(base_dir, "..", "data", "metro_graph.pkl")
graph, station_names, station_lines = load_graph_from_pickle(pickle_path)

with open(os.path.join(base_dir, "..", "data", "stations_coords.json"), 'r', encoding='utf-8') as f:
    station_coords = json.load(f)

# Inverser les noms pour retrouver les IDs
name_to_id = {name.lower(): sid for sid, name in station_names.items()}

# NetworkX pour Dijkstra
def build_nx_graph(graph_dict):
    G = nx.Graph()
    for station, neighbors in graph_dict.items():
        for neighbor, line, weight in neighbors:
            G.add_edge(station, neighbor, weight=weight)
    return G

G = build_nx_graph(graph)

@app.route("/api/stations", methods=["GET"])
def get_station_names():
    return jsonify(sorted(list(station_names.values())))

# Fonction principale de calcul
def find_shortest_path(from_station, to_station):
    from_station_id = name_to_id.get(from_station.lower(), from_station)
    to_station_id = name_to_id.get(to_station.lower(), to_station)

    path = nx.shortest_path(G, source=from_station_id, target=to_station_id, weight='weight')

    lines = []
    duration = 0
    for i in range(len(path) - 1):
        neighbors = graph[path[i]]
        for neighbor, line, weight in neighbors:
            if neighbor == path[i + 1]:
                if line not in lines:
                    lines.append(line)
                duration += weight
                break

    path_names = [station_names[str(st)] if str(st) in station_names else st for st in path]
    return path_names, lines, duration

# Route API principale
@app.route('/api/shortest_path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    from_station = data.get("from")
    to_station = data.get("to")

    if not from_station or not to_station:
        return jsonify({"error": "Champs manquants"}), 400

    try:
        path_names, lines, duration = find_shortest_path(from_station, to_station)

        coordinates = []
        for name in path_names:
            if name in station_coords:
                coordinates.append(station_coords[name])

        return jsonify({
            "path": path_names,
            "lines": lines,
            "duration": round(duration / 60, 1),  # minutes
            "coordinates": coordinates
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)