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
