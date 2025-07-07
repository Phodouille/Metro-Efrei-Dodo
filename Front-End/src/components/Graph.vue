<script setup>
import "leaflet/dist/leaflet.js";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { onMounted, ref } from "vue";
import axios from "axios";

let map = null;
let stationsMarkerGroup = null;
let stationsPolylineGroup = null;
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

// Fonction pour afficher les liaisons ACPM/MST (API /acpm)
function showMstLinks() {
  if (!map) return;
  // Nettoyage des anciens polylines MST
  if (mstPolylineGroup) {
    mstPolylineGroup.clearLayers();
  } else {
    mstPolylineGroup = L.featureGroup().addTo(map);
  }
  // Ajout des liaisons selon l'API /acpm
  for (const link of acpmLinks.value) {
    // On suppose que l'API /acpm retourne des objets {from_id, to_id}
    const fromStation = stations.value.find(s => String(s.id) === String(link.from_id));
    const toStation = stations.value.find(s => String(s.id) === String(link.to_id));
    if (fromStation && toStation) {
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
    const response = await axios.get("http://127.0.0.1:8000/acpm");
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
      attribution:
        '<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
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
      if (mstPolylineGroup) mstPolylineGroup.clearLayers();
    }
  });

  // Affichage/masquage du MST (ACPM)
  window.addEventListener("show-mst", (e) => {
    if (e.detail) {
      Promise.all([fetchStations(), fetchAcpmLinks()]).then(showMstLinks);
    } else {
      if (mstPolylineGroup) mstPolylineGroup.clearLayers();
    }
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