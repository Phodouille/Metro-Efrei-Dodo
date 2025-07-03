from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from starlette.middleware.cors import CORSMiddleware
import os

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

@app.get("/dijkstra/{src_stopid}/{dest_stopid}", response_model=DijkstraResponse)
def get_dijkstra(src_stopid: str, dest_stopid: str):
    from dijkstra import GraphDijkstra

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1) Charger tous les stop_ids uniques (attention aux stop_ids multiples séparés par virgule)
    cursor.execute("SELECT id, stop_ids FROM stations")
    id_to_stopid = {}
    stopid_to_ids = {}
    for row in cursor.fetchall():
        # Gère les cas où stop_ids contient plusieurs ids séparés par une virgule
        for sid in str(row["stop_ids"]).split(","):
            sid = sid.strip()
            id_to_stopid[row["id"]] = sid
            stopid_to_ids.setdefault(sid, []).append(row["id"])

    # 2) Construire le graphe sur les ids internes
    all_ids = list(id_to_stopid.keys())
    idx_map = {id_: idx for idx, id_ in enumerate(all_ids)}
    inv_map = {idx: id_ for id_, idx in idx_map.items()}
    V = len(all_ids)
    g = GraphDijkstra(V)

    cursor.execute("SELECT departure_stop_id, arrival_stop_id, duration FROM poidsligne")
    for dep_stopid, arr_stopid, duration in cursor.fetchall():
        for u in stopid_to_ids.get(dep_stopid, []):
            for v in stopid_to_ids.get(arr_stopid, []):
                ui, vi = idx_map[u], idx_map[v]
                g.graph[ui][vi] = float(duration)
                g.graph[vi][ui] = float(duration)

    # 3) Trouver tous les ids internes pour src_stopid et dest_stopid
    src_ids = stopid_to_ids.get(src_stopid, [])
    dest_ids = stopid_to_ids.get(dest_stopid, [])
    if not src_ids or not dest_ids:
        raise HTTPException(400, f"stop_id '{src_stopid}' ou '{dest_stopid}' inconnu")

    # 4) Appliquer Dijkstra sur tous les couples (src_id, dest_id) pour trouver le plus court chemin
    best_path = None
    best_distance = None
    for src in src_ids:
        for dest in dest_ids:
            try:
                distance, path_idx = g.shortest_path(idx_map[src], idx_map[dest])
            except Exception:
                continue
            if path_idx and (best_distance is None or distance < best_distance):
                best_distance = distance
                best_path = path_idx

    if not best_path or best_distance is None or best_distance == float('inf'):
        raise HTTPException(404, "Aucun chemin trouvé entre ces stop_ids")

    # 5) Convertir le chemin d'ids internes en stop_ids physiques (en évitant les doublons consécutifs)
    path_stop_ids = []
    last_stop_id = None
    for idx in best_path:
        stop_id = id_to_stopid[inv_map[idx]]
        if stop_id != last_stop_id:
            path_stop_ids.append(stop_id)
            last_stop_id = stop_id

    return DijkstraResponse(distance=best_distance, path=path_stop_ids)

