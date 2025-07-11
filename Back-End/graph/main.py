from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from starlette.middleware.cors import CORSMiddleware
import os
from connexity import is_graph_connected
from kruskal import Graph
from dijkstra import GraphDijkstra

app = FastAPI()

class Stop(BaseModel):
    stop_id: str
    stop_sequence: int
    lon: float
    lat: float
    stop_name: str

class DijkstraResponse(BaseModel):
    distance: float
    path: List[str]


def get_db_connection():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "mon_database.db"))
    if not os.path.exists(db_path):
        raise RuntimeError(f"Database not found at {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        # Ne vérifie plus la présence de la table 'stations' ici, laisse chaque endpoint gérer les erreurs SQL
        return conn
    except sqlite3.DatabaseError as e:
        raise RuntimeError(f"Votre base SQLite est corrompue : {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stops/{line_name}", response_model=List[Stop])
def read_stops(line_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {line_name} ORDER BY stop_sequence")
    stops = cursor.fetchall()
    return [Stop(**dict(stop)) for stop in stops]

@app.get("/stop/{line_name}/{stop_id}", response_model=Stop)
def read_stop(line_name: str, stop_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {line_name} WHERE stop_id = ?", (stop_id,))
    stop = cursor.fetchone()
    if stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return Stop(**dict(stop))

@app.get("/stations/")
def read_stations():
    lines = ["ligne1","ligne2","ligne3","ligne3b", "ligne4", "ligne5", "ligne6", "ligne7", "ligne7b", "ligne8", "ligne9", "ligne10", "ligne11", "ligne12", "ligne13", "ligne14"]
    conn = get_db_connection()
    cursor = conn.cursor()
    stations = []
    for line in lines:
        cursor.execute(f"""
            SELECT nt.*, l.lon, l.lat, l.stop_sequence, l.stop_id as line_stop_id
            FROM stations nt
            JOIN {line} l ON nt.stop_ids LIKE '%' || l.stop_id || '%'
            ORDER BY l.stop_sequence
        """)
        line_stations = cursor.fetchall()
        for i, station in enumerate(line_stations):
            station_dict = dict(station)
            station_dict["line"] = line
            # Add the stop_id of the next station
            if i < len(line_stations) - 1:
                next_station_id = line_stations[i + 1]["line_stop_id"]
                cursor.execute(
                    "SELECT id FROM stations WHERE stop_ids LIKE '%' || ? || '%'",
                    (next_station_id,))
                next_station_new_table_id = cursor.fetchone()
                station_dict["next_stop_id"] = next_station_new_table_id["id"] if next_station_new_table_id else ""
            else:
                station_dict["next_stop_id"] = ""
            # Add the stop_id of the previous station
            if i > 0:
                prev_station_id = line_stations[i - 1]["line_stop_id"]
                cursor.execute(
                    "SELECT id FROM stations WHERE stop_ids LIKE '%' || ? || '%'",
                    (prev_station_id,))
                prev_station_new_table_id = cursor.fetchone()
                station_dict["prev_stop_id"] = prev_station_new_table_id["id"] if prev_station_new_table_id else ""
            else:
                station_dict["prev_stop_id"] = ""
            stations.append(station_dict)
    return stations

@app.get("/listestations/")
def get_listestations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM listestations")
    return [dict(row) for row in cursor.fetchall()]

@app.get("/poids/")
def get_poids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM poids")
    return [dict(row) for row in cursor.fetchall()]

@app.get("/poidsligne/")
def get_poidsligne():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM poidsligne")
    return [dict(row) for row in cursor.fetchall()]

@app.get("/station/{stop_id}")
def get_station(stop_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stations WHERE stop_ids LIKE '%' || ? || '%'", (stop_id,))
    station = cursor.fetchone()
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return dict(station)
    #    raise HTTPException(status_code=400, detail="Invalid source or destination vertex")

    distance, path = g.shortest_path(src, dest)

    return DijkstraResponse(distance=distance, path=path)


@app.get("/stations/")
def read_stations():
    lines = ["ligne1","ligne2","ligne3","ligne3b", "ligne4", "ligne5", "ligne6", "ligne7", "ligne7b", "ligne8", "ligne9", "ligne10", "ligne11", "ligne12", "ligne13", "ligne14"]
    conn = get_db_connection()
    cursor = conn.cursor()
    stations = []
    for line in lines:
        cursor.execute(f"""
            SELECT nt.*, l.lon, l.lat, l.stop_sequence, l.stop_id as line_stop_id
            FROM stations nt
            JOIN {line} l ON nt.stop_ids LIKE '%' || l.stop_id || '%'
            ORDER BY l.stop_sequence
        """)
        line_stations = cursor.fetchall()
        for i, station in enumerate(line_stations):
            station_dict = dict(station)
            station_dict["line"] = line
            # Add the stop_id of the next station
            if i < len(line_stations) - 1:
                next_station_id = line_stations[i + 1]["line_stop_id"]
                cursor.execute(
                    "SELECT id FROM stations WHERE stop_ids LIKE '%' || ? || '%'",
                    (next_station_id,))
                next_station_new_table_id = cursor.fetchone()
                station_dict["next_stop_id"] = next_station_new_table_id["id"] if next_station_new_table_id else ""
            else:
                station_dict["next_stop_id"] = ""
            # Add the stop_id of the previous station
            if i > 0:
                prev_station_id = line_stations[i - 1]["line_stop_id"]
                cursor.execute(
                    "SELECT id FROM stations WHERE stop_ids LIKE '%' || ? || '%'",
                    (prev_station_id,))
                prev_station_new_table_id = cursor.fetchone()
                station_dict["prev_stop_id"] = prev_station_new_table_id["id"] if prev_station_new_table_id else ""
            else:
                station_dict["prev_stop_id"] = ""
            stations.append(station_dict)
    return stations

@app.get("/dijkstra/{src}/{dest}", response_model=DijkstraResponse)
def get_dijkstra(src: int, dest: int):
    try:
        from dijkstra import GraphDijkstra
    except ImportError:
        raise HTTPException(500, "Le module dijkstra.py est introuvable ou invalide.")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM stations")
        nb_vertices = cursor.fetchone()[0]

        g = GraphDijkstra(nb_vertices)

        cursor.execute("SELECT * FROM concatligne")
        liaisons = [list(row) for row in cursor.fetchall()]

        for u, v, w in liaisons:
            g.graph[int(u)][int(v)] = int(w)
            g.graph[int(v)][int(u)] = int(w)  

        if src >= nb_vertices or src < 0 or dest >= nb_vertices or dest < 0:
            raise HTTPException(status_code=400, detail="Invalid source or destination vertex")

        distance, path = g.shortest_path(src, dest)

        if not path or distance == float('inf'):
            raise HTTPException(404, "Aucun chemin trouvé entre ces sommets")


        return DijkstraResponse(
            distance=distance,
            path=[str(p) for p in path],
        )
    except Exception as e:
        raise HTTPException(500, f"Erreur interne lors de l'exécution de Dijkstra : {e}")

@app.get("/connexity/")
def check_connexity():
    """
    Vérifie si le graphe global (concatligne) est connexe.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stations")
    nb_vertices = cursor.fetchone()[0]

    # Création de la matrice d'adjacence
    adj_matrix = [[0] * nb_vertices for _ in range(nb_vertices)]
    cursor.execute("SELECT * FROM concatligne")
    for row in cursor.fetchall():
        u, v, w = int(row[0]), int(row[1]), int(row[2])
        adj_matrix[u][v] = w
        adj_matrix[v][u] = w  # Graphe non orienté

    is_connected = is_graph_connected(adj_matrix)
    return {"connected": is_connected}

# To launch your FastAPI backend, use this command from the Back-End/graph directory:
# uvicorn main:app --reload

# Do NOT use: uvicorn app:app --reload
# The filename is main.py, so the correct module is "main".

# If you get "Could not import module 'app'", it means you ran:
# uvicorn app:app --reload
# instead of:
# uvicorn main:app --reload

# Make sure you are in the directory containing main.py and use the correct command.

# L’erreur "'uvicorn' n’est pas reconnu..." signifie que Uvicorn n’est pas installé ou pas dans le PATH.
# Pour corriger :
# 1. Installe Uvicorn avec pip :
#    pip install uvicorn
# 2. Si tu utilises un environnement virtuel (venv), active-le avant de lancer la commande :
#    Sous Windows :
#      .\venv\Scripts\activate
#    Puis :
#      uvicorn main:app --reload
# 3. Si tu utilises Python sans venv, assure-toi que le dossier Scripts de Python est dans le PATH système.

# Si tu veux lancer Uvicorn sans l’ajouter au PATH, tu peux aussi utiliser :
#    python -m uvicorn main:app --reload

@app.get("/acpm/")
def get_kruskal():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stations")
    nb_vertices = cursor.fetchall()
    nb_vertices = len(nb_vertices)
    g = Graph(nb_vertices)

    cursor.execute("SELECT * FROM concatligne")
    liaisons = [list(row) for row in cursor.fetchall()]

    for u, v, w in liaisons:
        g.add_edge(int(u), int(v), int(w))

    acpm = g.kruskal()

    cursor.execute("SELECT stop_ids,id FROM stations")
    stop_ids = cursor.fetchall()
    stop_ids = {id: stop_id.split(',')[0] for stop_id, id in stop_ids}

    acpm_id = [(stop_ids[u], stop_ids[v]) for u, v in acpm]

    return acpm_id


@app.get("/acpm/points/")
def get_kruskal_points():
    kruskal = get_kruskal()

    points = []

    for u, v in kruskal:
        if u not in points:
            points.append(u)
        if v not in points:
            points.append(v)


    lines = ["ligne1","ligne2","ligne3","ligne3b", "ligne4", "ligne5", "ligne6", "ligne7", "ligne7b", "ligne8", "ligne9", "ligne10", "ligne11", "ligne12", "ligne13", "ligne14"]

    conn = get_db_connection()
    cursor = conn.cursor()

    stops = []

    for line in lines:
        cursor.execute(f"SELECT * FROM {line}")
        stops += cursor.fetchall()

    stops = [Stop(**dict(stop)) for stop in stops]

    points = [stop for stop in stops if stop.stop_id in points]

    return points