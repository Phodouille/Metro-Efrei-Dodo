import json
import pickle
import os
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from time import sleep

# Charger le graphe
with open("../data/metro_graph.pkl", "rb") as f:
    graph, station_names, station_lines = pickle.load(f)

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="metrogo_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

coords = {}

for sid, name in station_names.items():
    if name in coords:
        continue
    try:
        query = f"{name}, Paris, France"
        location = geocode(query)
        if location:
            coords[name] = [location.latitude, location.longitude]
            print(f"{name}: OK")
        else:
            print(f"{name}: Not found")
        sleep(1)
    except Exception as e:
        print(f"{name}: Error {e}")

# Sauvegarder
with open("../data/stations_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords, f, ensure_ascii=False, indent=2)
