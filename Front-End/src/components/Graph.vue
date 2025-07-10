<script setup>
import "leaflet/dist/leaflet.js";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { onMounted, ref } from "vue";
import axios from "axios";

let map = null;
let stationsMarkerGroup = null;
let stationsPolylineGroup = null;
let mstMarkerGroup = null;
let mstPolylineGroup = null;
const stations = ref([]);
const acpmLinks = ref([]);

// Icône personnalisée pour les marqueurs
const customMarkerIcon = L.icon({
  iconUrl: "src/assets/MarkerIcon.svg",
  iconSize: [18, 18],
  iconAnchor: [9, 9],
  popupAnchor: [0, -5],
});

// Fonction pour afficher toutes les stations sur la carte et relier les points selon les vraies liaisons de l'ACPM en ajoutant les stations des différentes lignes
function showAllstations() {
  if (!map) return;
  // Nettoyage des anciens marqueurs et polylines
  if (stationsMarkerGroup) {
    stationsMarkerGroup.clearLayers();
  } else {
    stationsMarkerGroup = L.featureGroup().addTo(map);
  }
  if (stationsPolylineGroup) {
    stationsPolylineGroup.clearLayers();
  } else {
    stationsPolylineGroup = L.featureGroup().addTo(map);
  }
  if (mstPolylineGroup) {
    mstPolylineGroup.clearLayers();
  } else {
    mstPolylineGroup = L.featureGroup().addTo(map);
  }

  // Ajout des marqueurs
  for (const station of stations.value) {
    const marker = L.marker([station.lat, station.lon], { icon: customMarkerIcon });
    marker.bindPopup(`${station.stop_name} (${station.line})`);
    stationsMarkerGroup.addLayer(marker);
  }

  // Ajout des liaisons réelles (utilise next_stop_id pour chaque station)
  for (const station of stations.value) {
    if (station.next_stop_id) {
      const nextStation = stations.value.find(s => String(s.id) === String(station.next_stop_id));
      if (nextStation) {
        const polyline = L.polyline(
          [
            [station.lat, station.lon],
            [nextStation.lat, nextStation.lon]
          ],
          {
            color: "#0074D9",
            weight: 3,
            opacity: 0.7,
          }
        );
        stationsPolylineGroup.addLayer(polyline);
      }
    }
  }
}

// Fonction pour afficher uniquement les stations et liaisons selon l'API /acpm
function showAcpm() {
  if (!map) return;

  // 1. (Re)création / nettoyage des groupes
  if (mstMarkerGroup) {
    mstMarkerGroup.clearLayers();
  } else {
    mstMarkerGroup = L.featureGroup().addTo(map);
  }
  if (mstPolylineGroup) {
    mstPolylineGroup.clearLayers();
  } else {
    mstPolylineGroup = L.featureGroup().addTo(map);
  }

  // 2. Map stop_id → station (pour lookup rapide)
  const idToStation = {};
  stations.value.forEach(station => {
    const raw = station.stop_ids ?? station.id;
    const ids = String(raw).split(",").map(s => s.trim());
    ids.forEach(id => { idToStation[id] = station; });
  });

  // 3. Collecter tous les stop_ids et stop_names “utilisés” par /acpm
  const usedIds = new Set();
  acpmLinks.value.forEach(link => {
    if (Array.isArray(link) && link.length === 2) {
      usedIds.add(String(link[0]));
      usedIds.add(String(link[1]));
    }
  });
  const usedNames = new Set();
  usedIds.forEach(id => {
    const st = idToStation[id];
    if (st) usedNames.add(st.stop_name);
  });

  // 4. Afficher **tous** les markers dont le stop_name est utilisé
  stations.value.forEach(station => {
    if (
      usedNames.has(station.stop_name) &&
      station.lat != null && station.lon != null
    ) {
      L.marker([station.lat, station.lon], { icon: customMarkerIcon })
       .bindPopup(`${station.stop_name} (${station.line})`)
       .addTo(mstMarkerGroup);
    }
  });

  // 5. Tracer les liaisons “officielles” ACPM (rouge)
  acpmLinks.value.forEach(link => {
    if (!Array.isArray(link) || link.length !== 2) return;
    const from = idToStation[String(link[0])];
    const to   = idToStation[String(link[1])];
    if (from && to) {
      L.polyline(
        [[from.lat, from.lon], [to.lat,   to.lon]],
        { color: "#FF4136", weight: 4, opacity: 0.85 }
      ).addTo(mstPolylineGroup);
    }
  });


  // 6. Connexions **inter-enregistrements** même stop_name — vert pointillé
  const nameToStations = {};
  stations.value.forEach(station => {
    if (usedNames.has(station.stop_name)) {
      (nameToStations[station.stop_name] ??= []).push(station);
    }
  });

  Object.values(nameToStations).forEach(group => {
    if (group.length > 1) {
      const [ref, ...others] = group;
      others.forEach(st => {
        L.polyline(
          [[ref.lat,  ref.lon], [st.lat, st.lon]],
          {
            color:    "#2ECC40",
            weight:   2,
            opacity:  0.6,
            dashArray:"2,4"
          }
        ).addTo(mstPolylineGroup);
      });
    }
  });
}






// Charge les stations depuis l'API backend
async function fetchStations() {
  try {
    const response = await axios.get("http://127.0.0.1:8000/stations/");
    stations.value = response.data;
  } catch (error) {
    console.error("Erreur lors du chargement des stations :", error);
  }
}

// Charge les liaisons ACPM depuis l'API backend
async function fetchAcpmLinks() {
  try {
    const response = await axios.get("http://127.0.0.1:8000/acpm/");
    acpmLinks.value = response.data;
  } catch (error) {
    console.error("Erreur lors du chargement des liaisons ACPM :", error);
  }
}

onMounted(async () => {
  map = L.map("map").setView([48.86285403569893, 2.3448491571643038], 12.5);
  L.tileLayer(
    "https://tile.jawg.io/5eafae32-aa5a-47da-a62c-ad2c1ab57fc3/{z}/{x}/{y}{r}.png?access-token=7CazPEKT76Mh5MSYbVWhLsP50NvaNbsBSbtEu3buIa0KijexNhx58EbJzu5dZ8Ox",
    {
      attribution:'<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      minZoom: 0,
      maxZoom: 22,
    }
  ).addTo(map);

  // Affichage/masquage du réseau classique
  window.addEventListener("show-network", (e) => {
    if (e.detail) {
      fetchStations().then(showAllstations);
    } else {
      if (stationsMarkerGroup) stationsMarkerGroup.clearLayers();
      if (stationsPolylineGroup) stationsPolylineGroup.clearLayers();
      // On ne touche pas à mstPolylineGroup ici
    }
  });

  // Affichage exclusif de l'APCM/MST (bouton, pas toggle)
  window.addEventListener("show-mst", async (e) => {
  // Si detail=false, on vide juste les couches MST
  if (!e.detail) {
    if (mstMarkerGroup)   mstMarkerGroup.clearLayers();
    if (mstPolylineGroup) mstPolylineGroup.clearLayers();
    return;
  }

  // Si detail=true, on veut afficher MST
  // On efface d'abord le réseau classique
  if (stationsMarkerGroup)   stationsMarkerGroup.clearLayers();
  if (stationsPolylineGroup) stationsPolylineGroup.clearLayers();

  // On charge les données puis on trace
  await Promise.all([fetchStations(), fetchAcpmLinks()]);
  showAcpm();
    });
});
</script>

<template>
  <div id="map"></div>
</template>

<style scoped>
#map {
  width: 80vw;
  height: 90vh;
  /* border-radius: 50px; */
  margin-left: 36px;
  margin-top: 9px;
  /* box-shadow: 0px 0px 3px 2px rgba(54, 54, 54, 0.25); */
  margin-top: 50px;

  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  border-radius: 25px;
  overflow: hidden;
  margin-right: 20px;
}
</style>