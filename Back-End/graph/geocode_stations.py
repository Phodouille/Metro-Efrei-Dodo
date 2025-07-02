from time import sleep
import json
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pickle

# Charge le graphe et les noms
with open('metro_graph.pkl', 'rb') as f:
    graph, station_names, station_lines = pickle.load(f)

# Initialisation du géocodeur avec rate limiting
geolocator = Nominatim(user_agent="metrogo_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

coords = {}
for sid, name in station_names.items():
    if name in coords:
        continue
    query = f"{name}, Paris, France"
    location = geocode(query)
    if location:
        coords[name] = [location.latitude, location.longitude]
        print(f"{name}: {coords[name]}")
    else:
        print(f"⚠️ Pas trouvé : {name}")
    sleep(1)  # respect du limit

# Sauvegarde du fichier JSON
with open('stations_coords.json', 'w', encoding='utf-8') as f:
    json.dump(coords, f, ensure_ascii=False, indent=2)
