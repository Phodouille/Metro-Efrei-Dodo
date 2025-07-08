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
const befSetIdSrcDstList = ref([])
const djikstraStations = ref([]);
const filteredDjikstraStations = ref([]);
const customMarkerIcon = L.icon({
  iconUrl: "src/assets/MarkerIcon.svg",
  iconSize: [18, 18], // size of the icon
  iconAnchor: [9, 9], // point of the icon which will correspond to marker's location
  popupAnchor: [0, -5],
});
let pointLineMarkerGroup = null;
let map = null;

const placeDijkstraPoint = () => {
  pointLineMarkerGroup.clearLayers();
  for (let i = 0; i < filteredDjikstraStations.value.length; i++) {
    if (i === 0 || i === filteredDjikstraStations.value.length - 1) {
      const element = filteredDjikstraStations.value[i];
      const marker = L.marker([element.lat, element.lon], {
        icon: customMarkerIcon,
      });
      marker
        .addTo(pointLineMarkerGroup)
        .bindTooltip(`${element.title} ${element.line}`, {
          permanent: true,
          direction: "top",
          offset: [0, -10],
          opacity: 1,
        });
    } else {
      const element = filteredDjikstraStations.value[i];
      const marker = L.marker([element.lat, element.lon], {
        icon: customMarkerIcon,
      }).bindPopup(`${element.title} ${element.line}`);
      marker.addTo(pointLineMarkerGroup);
    }
  }
  drawLinesBetweenDijkstraPoint();
  if (pointLineMarkerGroup.getLayers().length > 0) {
    map.flyToBounds(pointLineMarkerGroup.getBounds(), {
      padding: [50, 50], // Adds margin around the points
      maxZoom: 20, // Prevents zooming in too much
      animate: true,
      duration: 0.5, // Duration of animation in seconds
    });
  }
};

const drawLinesBetweenDijkstraPoint = () => {
  dijkstraPointsCoordinatesList();
};

const dijkstraPointsCoordinatesList = () => {
  const lineColors = {
    ligne1: "rgba(255,190,0,1)",
    ligne2: "rgba(0,85,200,1)",
    ligne3: "rgba(110,110,0,1)",
    ligne3b: "rgba(130,200,230,1)",
    ligne4: "rgba(160,0,110,1)",
    ligne5: "rgba(255,90,0,1)",
    ligne6: "rgba(129,220,115,1)",
    ligne7: "rgba(255,130,180,1)",
    ligne7_2: "rgba(255,130,180,1)",
    ligne7b: "rgba(129,220,115,1)",
    ligne8: "rgba(210,130,190,1)",
    ligne9: "rgba(210,210,0,1)",
    ligne10: "rgba(220,150,0,1)",
    ligne11: "rgba(110,73,30,1)",
    ligne12: "rgba(0,100,60,1)",
    ligne13: "rgba(130,200,230,1)",
    ligne14: "rgba(100,1,130,1)",
  };

  for (let i = 0; i < filteredDjikstraStations.value.length - 1; i++) {
    const current = filteredDjikstraStations.value[i];
    const next = filteredDjikstraStations.value[i + 1];

    const color = lineColors[next.line] || "gray";

    const polyline = L.polyline(
      [
        [current.lat, current.lon],
        [next.lat, next.lon],
      ],
      {
        color,
        weight: 5,
      }
    );
    pointLineMarkerGroup.addLayer(polyline);
  }
};
async function fetchStations() {
  try {
    const response = await axios.get("http://127.0.0.1:8000/stations/");
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
      console.log('Source data map :', sourceDataMap.value)
      console.log('Destination data map:', destinationDataMap.value)
      searchId();
      listIdSrcDst.value = [...setIdSrcDst.value];
      console.log("stations list ", stations.value);
      console.log("list id", listIdSrcDst.value);
      loadDijkstra();
    }
  );
}

async function fetchDijkstraPath() {
  path.value = [];
  store.pathDijkstraDuration = 0
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/dijkstra/${listIdSrcDst.value[0]}/${listIdSrcDst.value[1]}`
    );
    const data = response.data.path;
    const distance = response.data.distance;
    store.pathDijkstraDuration = distance;
    console.log('check the store here', store.pathDijkstraDuration)
    for (let index = 0; index < data.length; index++) {
      const element = data[index];
      path.value.push(element);
    }
  } catch (error) {
    console.error("Failed to fetch Dijkstra path:", error);
  }
}

const searchId = () => {
  befSetIdSrcDstList.value = []
  for (let index = 0; index < stations.value.length; index++) {
    const element = stations.value[index];
    if (
      element.stop_name === sourceDataMap.value 
    ) {
      befSetIdSrcDstList.value[0] = element.id
    } else {
      if (
        element.stop_name === destinationDataMap.value
      ) {
        befSetIdSrcDstList.value[1] = element.id
      }
    }
  }
  setIdSrcDst.value = new Set(befSetIdSrcDstList.value);
};

const extractDijkstraStations = () => {
  djikstraStations.value = [];
  console.log("check here bro path", path.value);
  console.log("check here bro stations", stations.value);
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

const updateDijkstraPathName = () => {
  store.pathDijkstraName = []
  store.pathDijkstraLine = []
  for (let index = 0; index < filteredDjikstraStations.value.length; index++) {
    const element = filteredDjikstraStations.value[index];
    store.pathDijkstraName.push(element.title)
    store.pathDijkstraLine.push(element.line)
  }
}

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
  updateDijkstraPathName();
};

async function loadDijkstra() {
  await fetchDijkstraPath();
  console.log("this is fetch dji path", path.value);
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
  border-radius: 10px;
  margin-left: 36px;
  margin-top: 9px;
  box-shadow: 0px 0px 3px 2px rgba(54, 54, 54, 0.25);
  margin-top: 50px;
}
</style>
