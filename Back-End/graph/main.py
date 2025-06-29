from flask import Flask, jsonify, request
import sys
import os
import json
import networkx as nx
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from graph_parser import load_graph_from_pickle
from dijkstra_path import compute_dijkstra_path
from kruskal import kruskal_mst

app = Flask(__name__)
CORS(app)  # autorise les requêtes depuis Vue.js en local

# Chargement des fichiers
graph_dir = os.path.dirname(os.path.abspath(__file__))
pickle_path = os.path.join(graph_dir, "..", "data", "metro_graph.pkl")
coord_path = os.path.join(graph_dir, "..", "data", "stations_coords.json")

graph, station_names, station_lines = load_graph_from_pickle(pickle_path)
with open(coord_path, 'r', encoding='utf-8') as f:
    station_coords = json.load(f)

name_to_id = {name.lower(): sid for sid, name in station_names.items()}

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

def convert_path_to_output(path):
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

    path_names = [station_names.get(str(st), st) for st in path]
    coordinates = [station_coords[name] for name in path_names if name in station_coords]

    return {
        "path": path_names,
        "lines": lines,
        "duration": round(duration / 60, 1),
        "coordinates": coordinates
    }

@app.route('/api/shortest_path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    from_station = data.get("from")
    to_station = data.get("to")

    if not from_station or not to_station:
        return jsonify({"error": "Champs manquants"}), 400

    try:
        from_id = name_to_id.get(from_station.lower(), from_station)
        to_id = name_to_id.get(to_station.lower(), to_station)

        # Utilisation des différents algorithmes
        results = []

        # Dijkstra
        path_dijkstra, _ = compute_dijkstra_path(graph, from_id, to_id)
        if path_dijkstra:
            results.append(convert_path_to_output(path_dijkstra))

        # Kruskal (via MST et BFS pour extraire un chemin)
        mst = kruskal_mst(graph)
        mst_graph = build_nx_graph(mst)
        try:
            path_kruskal = nx.shortest_path(mst_graph, source=from_id, target=to_id)
            results.append(convert_path_to_output(path_kruskal))
        except:
            pass

        # Supprimer les doublons (même chemin)
        unique_results = []
        seen_paths = set()
        for r in results:
            path_str = '->'.join(r['path'])
            if path_str not in seen_paths:
                seen_paths.add(path_str)
                unique_results.append(r)

        return jsonify(unique_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
