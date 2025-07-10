<template>
  <div id="map"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'

let map = null
let stopsLayer = null

// Couleurs par ligne
const lineColors = {
  "1":  "rgba(255,190,0,1)",
  "2":  "rgba(0,85,200,1)",
  "3":  "rgba(110,110,0,1)",
  "3b": "rgba(130,200,230,1)",
  "4":  "rgba(160,0,110,1)",
  "5":  "rgba(255,90,0,1)",
  "6":  "rgba(129,220,115,1)",
  "7":  "rgba(255,130,180,1)",
  "7b": "rgba(129,220,115,1)",
  "8":  "rgba(210,130,190,1)",
  "9":  "rgba(210,210,0,1)",
  "10": "rgba(220,150,0,1)",
  "11": "rgba(110,73,30,1)",
  "12": "rgba(0,100,60,1)",
  "13": "rgba(130,200,230,1)",
  "14": "rgba(100,1,130,1)",
}

async function renderLine(lineParam) {
  // Vide l’ancienne couche
  stopsLayer.clearLayers()

  // On récupère la clé numérique pour lineColors
  const key   = lineParam.replace(/^ligne/, '')        // "ligne1" → "1"
  const color = lineColors[key] || '#000'

  // Fetch des arrêts
  let stops = []
  try {
    const res = await axios.get(`http://127.0.0.1:8000/stops/${lineParam}`)
    stops = res.data
  } catch (err) {
    console.error("Erreur fetch stops:", err)
    return
  }
  if (!stops.length) return

  // Tri par stop_sequence si dispo
  stops.sort((a, b) => (a.stop_sequence || 0) - (b.stop_sequence || 0))

  // On construit la liste de coords
  const coords = stops.map(s => [s.lat, s.lon])

  // On place un marker pour chaque arrêt
  stops.forEach(s => {
    L.circleMarker([s.lat, s.lon], {
      radius:      6,
      fillColor:   color,
      color:       '#000',
      weight:      1,
      fillOpacity: 0.8
    })
    .bindPopup(s.stop_name)
    .addTo(stopsLayer)
  })

  // On trace la polyligne dans la couleur de la ligne
  L.polyline(coords, {
    color,
    weight:  4,
    opacity: 0.9
  }).addTo(stopsLayer)

  // On ajuste le zoom pour tout voir
  map.fitBounds(stopsLayer.getBounds(), { padding: [30, 30] })
}


onMounted(() => {
  map = L.map('map').setView([48.86285, 2.34484], 12.5)
  L.tileLayer(
    "https://tile.jawg.io/5eafae32-aa5a-47da-a62c-ad2c1ab57fc3/{z}/{x}/{y}{r}.png?access-token=7CazPEKT76Mh5MSYbVWhLsP50NvaNbsBSbtEu3buIa0KijexNhx58EbJzu5dZ8Ox",
    {
      attribution:
        '&copy; <a href="https://jawg.io">Jawg</a> &copy; OpenStreetMap contributors',
      minZoom: 0,
      maxZoom: 22,
    }
  ).addTo(map)

  stopsLayer = L.layerGroup().addTo(map)

  window.addEventListener('show-line', e => {
    const lineParam = e.detail  // e.g. "ligne1", "ligne3b", etc.
    if (!lineParam) {
      stopsLayer.clearLayers()
    } else {
      renderLine(lineParam)
    }
  })
})
</script>

<style scoped>
#map {
  width: 47vw;
  height: 90vh;
  border-radius: 10px;
  margin-left: 36px;
  margin-top: 50px;
  box-shadow: 0 0 3px 2px rgba(54,54,54,0.25);
}

</style>
