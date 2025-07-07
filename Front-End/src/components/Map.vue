<script setup>
import "leaflet/dist/leaflet.js";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { onMounted } from "vue";
import axios from "axios";
import { ref } from "vue";
import { watch } from "vue";
import { useNewStore } from "../stores/path.js";

const sourceDataMap = ref("");
const destinationDataMap = ref("");
const store = useNewStore();
const setIdSrcDst = ref(new Set());
const listIdSrcDst = ref([]);
const stations = ref([]);
const path = ref([]);
const djikstraStations = ref([]);
const filteredDjikstraStations = ref([]);
const dijkstraPointsCoordinates = ref([]);
const customMarkerIcon = L.icon({
  iconUrl: 'src/assets/MarkerIcon.svg',
  iconSize: [18, 18],       // size of the icon
  iconAnchor: [9, 9],     // point of the icon which will correspond to marker's location
  popupAnchor: [0, -5] 
})
let pointLineMarkerGroup = null;
let map = null;

const placeDijkstraPoint = () => {
  pointLineMarkerGroup.clearLayers();
  for (let i = 0; i < filteredDjikstraStations.value.length; i++) {
    const element = filteredDjikstraStations.value[i];
    const marker = L.marker([element.lat, element.lon], {icon: customMarkerIcon});
    marker
      .bindPopup(`${element.title} ${element.line}`)
      .addTo(pointLineMarkerGroup);
    // if (i === 0) {
    //   const element = filterDjikstraStations.value[i]
    //   const marker = L.marker([element.lat, element.lon], {icon: customMarkerIcon})

    // }
  }
  drawLinesBetweenDijkstraPoint();
  if (pointLineMarkerGroup.getLayers().length > 0) {
  map.flyToBounds(pointLineMarkerGroup.getBounds(), {
    padding: [50, 50],     // Adds margin around the points
    maxZoom: 20,           // Prevents zooming in too much
    animate: true,
    duration: 0.5         // Duration of animation in seconds
  });
}
};

const drawLinesBetweenDijkstraPoint = () => {
  dijkstraPointsCoordinatesList();
  const lineMarker = L.polyline(dijkstraPointsCoordinates.value, {
    color: "green",
    weight: 5,
    opacity: 0.8,
  });
  pointLineMarkerGroup.addLayer(lineMarker);
};

const dijkstraPointsCoordinatesList = () => {
  dijkstraPointsCoordinates.value = [];
  for (let index = 0; index < filteredDjikstraStations.value.length; index++) {
    const element = filteredDjikstraStations.value[index];
    dijkstraPointsCoordinates.value[index] = [element.lat, element.lon];
  }
};
async function fetchStations() {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/stations/"
    );
    const data = response.data;
    for (let index = 0; index < data.length; index++) {
      const element = data[index];
      const obj = {
        id: element.id,
        lat: element.lat,
        lon: element.lon,
        stop_name: element.stop_name,
        line: element.line,
        next_stop_id: element.next_stop_id,
        previous_stop_id: element.prev_stop_id,
      };
      stations.value.push(obj);
    }
  } catch (error) {
    console.error("Failed to fetch stations:", error);
  }
}

async function loadStations() {
  await fetchStations();
  watch(
    () => [store.sourceData, store.destinationData],
    ([newSrcData, newDstData]) => {
      sourceDataMap.value = newSrcData;
      destinationDataMap.value = newDstData;
      searchId();
      listIdSrcDst.value = [...setIdSrcDst.value];
      console.log('stations list ', stations.value);
      console.log(listIdSrcDst.value);
      loadDijkstra();
    }
  );
}

async function fetchDijkstraPath() {
  path.value = [];
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/dijkstra/${listIdSrcDst.value[0]}/${listIdSrcDst.value[1]}`
    );
    const data = response.data.path;

    for (let index = 0; index < data.length; index++) {
      const element = data[index];
      path.value.push(element);
    }
  } catch (error) {
    console.error("Failed to fetch Dijkstra path:", error);
  }
}

const searchId = () => {
  setIdSrcDst.value = new Set();
  for (let index = 0; index < stations.value.length; index++) {
    const element = stations.value[index];
    if (
      element.stop_name === sourceDataMap.value ||
      element.stop_name === destinationDataMap.value
    ) {
      setIdSrcDst.value.add(element.id);
    }
  }
};

const extractDijkstraStations = () => {
  djikstraStations.value = [];
  console.log('check here bro path', path.value)
  console.log('check here bro stations', stations.value)
  for (let index1 = 0; index1 < path.value.length; index1++) {
    const element1 = path.value[index1];
    for (let index2 = 0; index2 < stations.value.length; index2++) {
      const element2 = stations.value[index2];
      if (element1 == element2.id) {
        const obj = {
          id: element2.id,
          lat: element2.lat,
          lon: element2.lon,
          stop_name: element2.stop_name,
          line: element2.line,
          next_stop_id: element2.next_stop_id,
          previous_stop_id: element2.prev_stop_id,
        };
        djikstraStations.value.push(obj);
      } else {
        continue;
      }
    }
  }

};

const filterDjikstraStations = () => {
  filteredDjikstraStations.value = [];
  for (let pathIndex = 0; pathIndex < path.value.length; pathIndex++) {
    const element1 = path.value[pathIndex];
    for (
      let dataIndex = 0;
      dataIndex < djikstraStations.value.length;
      dataIndex++
    ) {
      const element2 = djikstraStations.value[dataIndex];
      if (
        (element2.id == element1 &&
          element2.next_stop_id == path.value[pathIndex + 1]) ||
        (element2.id == element1 &&
          element2.previous_stop_id == path.value[pathIndex - 1]) ||
        (element2.id == element1 &&
          element2.previous_stop_id == path.value[pathIndex + 1]) ||
        (element2.id == element1 &&
          element2.next_stop_id == path.value[pathIndex - 1])
      ) {
        const obj = {
          id: element2.id,
          title: element2.stop_name,
          line: element2.line,
          lat: element2.lat,
          lon: element2.lon,
        };
        filteredDjikstraStations.value.push(obj);
        break;
      }
    }
  }
};

async function loadDijkstra() {
  await fetchDijkstraPath();
  console.log('this is fetch dji path', path.value);
  extractDijkstraStations();
  console.log("Check here : ", djikstraStations.value);
  filterDjikstraStations();
  console.log("Golden road : ", filteredDjikstraStations.value);
  placeDijkstraPoint();
}

onMounted(() => {
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
  pointLineMarkerGroup = L.featureGroup().addTo(map);
  loadStations();
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