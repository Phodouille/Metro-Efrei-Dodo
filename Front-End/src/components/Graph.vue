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

// Fonction pour afficher toutes les stations sur la carte et relier les points selon les vraies liaisons (next_stop_id)
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
  // Nettoyage des anciens marqueurs et polylines ACPM
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

  // DEBUG : Affiche les liens et les stations utilisés
  console.log("acpmLinks.value =", acpmLinks.value);
  console.log("stations.value =", stations.value);

  // On récupère tous les stop_ids utilisés dans les liens ACPM
  const usedIds = new Set();
  for (const link of acpmLinks.value) {
    if (Array.isArray(link) && link.length === 2) {
      usedIds.add(String(link[0]));
      usedIds.add(String(link[1]));
    }
  }
  console.log("usedIds =", Array.from(usedIds));

  // Ajout des marqueurs pour chaque station utilisée dans ACPM
  for (const station of stations.value) {
    // station.stop_ids peut contenir plusieurs ids séparés par des virgules
    const stopIds = String(station.stop_ids || station.id).split(",");
    if (
      stopIds.some(id => usedIds.has(id.trim())) &&
      station.lat !== undefined &&
      station.lon !== undefined
    ) {
      console.log("Ajout marker ACPM:", station.stop_ids, station.stop_name, station.lat, station.lon);
      const marker = L.marker([station.lat, station.lon], { icon: customMarkerIcon });
      marker.bindPopup(`${station.stop_name} (${station.line})`);
      mstMarkerGroup.addLayer(marker);
    }
  }

  // Ajout des liaisons selon l'API /acpm
  for (const link of acpmLinks.value) {
    if (!Array.isArray(link) || link.length !== 2) continue;
    // Trouve la station dont stop_ids contient link[0]
    const fromStation = stations.value.find(s =>
      String(s.stop_ids || s.id).split(",").map(id => id.trim()).includes(String(link[0]))
    );
    const toStation = stations.value.find(s =>
      String(s.stop_ids || s.id).split(",").map(id => id.trim()).includes(String(link[1]))
    );
    if (
      fromStation && toStation &&
      fromStation.lat !== undefined && fromStation.lon !== undefined &&
      toStation.lat !== undefined && toStation.lon !== undefined
    ) {
      console.log("Ajout liaison ACPM:", link[0], "->", link[1]);
      const polyline = L.polyline(
        [
          [fromStation.lat, fromStation.lon],
          [toStation.lat, toStation.lon]
        ],
        {
          color: "#FF4136",
          weight: 4,
          opacity: 0.85,
        }
      );
      mstPolylineGroup.addLayer(polyline);
    } else {
      console.warn("Liaison ignorée (station manquante):", link, fromStation, toStation);
    }
  }
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
  window.addEventListener("show-mst", (e) => {
    // On efface tout le réseau classique
    if (stationsMarkerGroup) stationsMarkerGroup.clearLayers();
    if (stationsPolylineGroup) stationsPolylineGroup.clearLayers();
    // On affiche l'APCM/MST
    Promise.all([fetchStations(), fetchAcpmLinks()]).then(showAcpm);
  });
});
</script>

<template>
  <div id="map"></div>
</template>

<style scoped>
#map {
  width: 47vw;
  height: 90vh;
  border-radius: 50px;
  margin-left: 36px;
  margin-top: 9px;
  box-shadow: 0px 0px 3px 2px rgba(54, 54, 54, 0.25);
  margin-top: 50px;
}
</style>