{/* <script setup>
import "leaflet/dist/leaflet.js";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { onMounted } from "vue";
import axios from "axios";
import { ref } from "vue";
import { watch } from "vue";
import { computed } from "vue";
import { useNewStore } from "../stores/path.js";
import { point } from "leaflet";

// const test = () => {
//    console.log('check here', stations.value)
//    console.log(path.value)
//    if (stations.value.length > 0) {
//      for (let index = 0; index < stations.value.length; index++) {
//        const element = stations.value[index];
//        console.log(element);
//      }
//    } else {
//      console.warn("Stations data is not yet populated.");
//    }
// }

const sourceDataMap = ref("");
const destinationDataMap = ref("");
const store = useNewStore();
const setIdSrcDst = ref(new Set());
const listIdSrcDst = ref([]);
const stations = ref([]);
const map = ref(null);
const path = ref([]);
const djikstraStations = ref([]);
const filteredDjikstraStations = ref([]);
const lineMarkerGroup = ref(null);
const dijkstraPointsCoordinates = ref([]);
const pointLineMarkerGroup = ref(null);

// console.log(store.sourceData)
// console.log(store.newData)
// store.newData = 'bye bye'
// console.log(store.newData)

// const props = defineProps({
//   sourceInput: String,
//   destinationInput: String,
// });

// const sourceInputDijkstra = ref("");
// const destinationInputDijkstra = ref("");

// let locations = [];

// const points = ref([])
// const lines = ref([])

// let map;

// const stations = ref([]);

// const path = ref([]);

// const tempPoint = ref([])

// let dijkstraPointsCoordinates = {};
// const dijkstraPointsCoordinates = ref([])

// const djikstraStations = ref([]);

// // let filterDjikstraStations = [];
// const filterDjikstraStations = ref([])

// let inputSrcDst = [];

// const resetMap = () => {
//   console.log("Clearing", points.value.length, "points");
//   for (const marker of points.value) {
//     if (map.hasLayer(marker)) {
//       map.removeLayer(marker);
//     }
//   }
//   points.value = [];

//   console.log("Clearing", lines.value.length, "lines");
//   for (const line of lines.value) {
//     if (map.hasLayer(line)) {
//       map.removeLayer(line);
//     }
//   }
//   lines.value = [];
// setTimeout(()=> {
//     for (let index = 0; index < points.value.length; index++) {
//     const element = points.value[index];
//     map.removeLayer(element)
// }
// }, 2000)
// map.removeLayer(points.value[0])
// if (points.value.length === 0) {
//     console.log('list of points is empty')
// }
// else {
//         for (let index = 0; index < points.value.length; index++) {
//             map.removeLayer(points.value[index]);
//         }
//         points.value = []

// for (let index = 0; index < points.value.length; index++) {
//     const element = points.value[index];
//     map.removeLayer(element)
//     console.log('point has been removed')
// }
// map.removeLayer(points.value[1])
// }

// };

const placeDijkstraPoint = () => {
  // if (
  //   map.value &&
  //   pointLineMarkerGroup.value &&
  //   map.value.hasLayer(pointLineMarkerGroup.value)
  // ) {
  //   pointLineMarkerGroup.value.eachLayer((layer) => {
  //     if (layer.unbindPopup) {
  //       layer.unbindPopup();
  //     }
  //   });
  //   pointLineMarkerGroup.value.closePopup();
  //   pointLineMarkerGroup.value.clearLayers(); // Remove all markers/lines
  //   map.value.removeLayer(pointLineMarkerGroup.value); // Remove the group from map
  //   pointLineMarkerGroup.value = null; // Optional: reset it
  //   console.log("Hello");
  // }

  // Create a new clean group and add to the map
  // pointLineMarkerGroup.value = L.layerGroup().addTo(map.value);

  // Add new markers to the group
//   for (let i = 0; i < filteredDjikstraStations.value.length; i++) {
//     const element = filteredDjikstraStations.value[i];
//     const marker = L.marker([element.lat, element.lon]);
//     marker
//       .bindPopup(`${element.title} ${element.line}`)
//       .addTo(pointLineMarkerGroup.value);
//     marker.addTo(pointLineMarkerGroup.value)
//     marker.on('click', () => {
//   const popup = L.popup()
//     .setLatLng(marker.getLatLng())
//     .setContent('Hello')
//     .openOn(map.value);
// });}
    // Create the marker manually
// const marker1 = L.marker([48.858504187279614, 2.294438382089036]).addTo(pointLineMarkerGroup.value);

// Use a standalone popup (not bound to the marker)
// const popup1 = L.popup({ autoClose: true, closeOnClick: false })
//   .setContent('I\'m here');

// Show the popup on click
// marker1.on('click', () => {
//   popup1.setLatLng(marker1.getLatLng());
//   popup1.openOn(map.value);
// });
// map.value.on('popupclose', function (e) {
//   if (e.popup === popup1) {
//     map.value.removeLayer(marker1);      // Remove marker
//     map.value.closePopup();              // Make sure popup is closed
//     // No need to remove popup manually; Leaflet handles it
//   }
// });
// Optional: disable double-click zoom on the map
// L.marker([48.858504187279614, 2.294438382089036])
//   .addTo(pointLineMarkerGroup.value)
//   .bindPopup('I\'m here');
// map.value.on('zoomstart', () => {
//   map.value.closePopup(); // Prevent crash during animated zoom
// });
// const marker = L.marker([48.8585, 2.2944])
//   .addTo(map.value)
// marker.bindPopup('Hi')
  // .openPopup();

// This is enough to remove the popup DOM reference safely
// marker.on("popupclose", () => {
//   marker.unbindPopup(); // ✅ Safe: only detaches reference, no DOM loop
// });

// (Optional) Close all popups on zoom start to prevent crash
// map.value.on("zoomstart", () => {
//   map.value.closePopup(); // ✅ this doesn't loop
// });
// Attach popupclose listener directly to the marker
// marker.on('popupclose', () => {
//   map.value.removeLayer(marker); // Remove marker when popup is closed
// });
// map.value.doubleClickZoom.disable();
//     marker.on('dblclick', (e) => {
//   // Fully cancel the native and Leaflet event behavior
//   if (e.originalEvent) {
//     e.originalEvent.preventDefault();
//     e.originalEvent.stopImmediatePropagation();
//   }

//   e.preventDefault();
//   e.stopImmediatePropagation();

//   // Explicitly close popups and reset zoom animation state
//   if (map.value) {
//     map.value.closePopup();
//     map.value._stop(); // 💣 this forcefully cancels zoom animation
//   }
// });
    // drawLinesBetweenDijkstraPoint()
  // }
};

const drawLinesBetweenDijkstraPoint = () => {
  dijkstraPointsCoordinatesList();
  const lineMarker = L.polyline(dijkstraPointsCoordinates.value, {
    color: "red",
    weight: 5,
    opacity: 0.8,
  });
  pointLineMarkerGroup.value.addLayer(lineMarker);
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
      "https://backend-ot44.onrender.com/stations"
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
  // L.marker([48.858504187279614, 2.294438382089036]).addTo(
  //   pointLineMarkerGroup.value
  // );
  // setTimeout(() => {
  //   pointLineMarkerGroup.value.clearLayers();
  // }, 2000);
  // setTimeout(() => {
  //   L.marker([48.85723395168378, 2.3126868472746396]).addTo(
  //     pointLineMarkerGroup.value
  //   );
  //   L.marker([48.83867680116839, 2.3148376801854966]).addTo(
  //     pointLineMarkerGroup.value
  //   );
  //   console.log(pointLineMarkerGroup.value);
  // }, 5000);

  await fetchStations();
  watch(
    () => [store.sourceData, store.destinationData],
    ([newSrcData, newDstData]) => {
      sourceDataMap.value = newSrcData;
      destinationDataMap.value = newDstData;
      searchId();
      listIdSrcDst.value = [...setIdSrcDst.value];
      console.log(stations.value);
      console.log(listIdSrcDst.value);
      // pointLineMarkerGroup.value.clearLayers();
      loadDijkstra();
    }
  );
}

async function fetchDijkstraPath() {
  path.value = [];
  try {
    const response = await axios.get(
      `https://backend-ot44.onrender.com/dijkstra/${listIdSrcDst.value[0]}/${listIdSrcDst.value[1]}`
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
  for (let index = 0; index < path.value.length; index++) {
    const element1 = path.value[index];
    for (let index = 0; index < stations.value.length; index++) {
      const element2 = stations.value[index];
      if (element1 === element2.id) {
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
        (element2.id === element1 &&
          element2.next_stop_id === path.value[pathIndex + 1]) ||
        (element2.id === element1 &&
          element2.previous_stop_id === path.value[pathIndex - 1]) ||
        (element2.id === element1 &&
          element2.previous_stop_id === path.value[pathIndex + 1]) ||
        (element2.id === element1 &&
          element2.next_stop_id === path.value[pathIndex - 1])
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
  console.log(path.value);
  extractDijkstraStations();
  console.log("Check here : ", djikstraStations.value);
  filterDjikstraStations();
  console.log("Golden road : ", filteredDjikstraStations.value);
  placeDijkstraPoint();
}

// Define a reactive variable called "pointLineMarkerGroup"
// const pointLineMarkerGroup = ref(null)
// Initialize an empty layer group (container) and add it on the map
// pointLineMarkerGroup.value = L.layerGroup().addTo(map)

onMounted(() => {
  // stations.value = []
  // console.log(stations.value)
  //   watch(
  //     () => props.sourceInput,
  //     (input) => {
  //       sourceInputDijkstra.value = input;
  //       console.log(sourceInputDijkstra.value);
  //     }
  //   );

  //   watch(
  //     () => props.destinationInput,
  //     (input) => {
  //       destinationInputDijkstra.value = input;
  //       console.log(destinationInputDijkstra.value);
  //     }
  //   );

  //   console.log(`Check here ${sourceInputDijkstra.value}`);

  // axios
  //   .get("https://backend-ot44.onrender.com/stations")
  //   .then(function (response) {
  //     const data = response.data;
  //     for (let index = 0; index < data.length; index++) {
  //       const element = data[index];
  //       const obj = {
  //         id: element.id,
  //         lat: element.lat,
  //         lon: element.lon,
  //         stop_name: element.stop_name,
  //         line: element.line,
  //         next_stop_id: element.next_stop_id,
  //         previous_stop_id: element.prev_stop_id,
  //       };
  //       stations.push(obj);
  //     }
  //   })
  //     .finally(function () {
  // for (let index = 0; index < path.length; index++) {
  //     const element1 = path[index];
  //     for (let index = 0; index < stations.length; index++) {
  //         const element2 = stations[index];
  //         if (element2.id === element1) {
  //             const obj = {
  //                 id: element2.id,
  //                 lat: element2.lat,
  //                 lon: element2.lon,
  //                 title: element2.stop_name
  //             }
  //             locations.push(obj)
  //         }
  //     }

  // }
  map.value = L.map("map").setView(
    [48.86285403569893, 2.3448491571643038],
    12.5
  );
  L.tileLayer(
    "https://tile.jawg.io/5eafae32-aa5a-47da-a62c-ad2c1ab57fc3/{z}/{x}/{y}{r}.png?access-token=7CazPEKT76Mh5MSYbVWhLsP50NvaNbsBSbtEu3buIa0KijexNhx58EbJzu5dZ8Ox",
    {
      attribution:
        '<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      minZoom: 0,
      maxZoom: 22,
    }
  ).addTo(map.value);
  L.marker([48.8585, 2.2944]).bindPopup('hello').addTo(map.value)
  


//   map.value.on('zoomstart', () => {
//   map.value.closePopup();
// });
  // pointLineMarkerGroup.value = L.layerGroup().addTo(map.value);

  // pointLineMarkerGroup.value = L.layerGroup().addTo(map.value);
  // map.value.doubleClickZoom.disable();
  // pointLineMarkerGroup.value = L.layerGroup().addTo(map.value);
  // loadStations();
  // pointLineMarkerGroup.value ? console.log(true) : console.log(false);

  // for (let index = 0; index < locations.length; index++) {
  //     const element = locations[index];
  //     L.marker([element.lat, element.lon]).bindPopup(element.title).addTo(map);
  // }
  // locations.forEach(point => {
  //     dijkstraPointsCoordinates[point.id] = [point.lat, point.lon]
  // })
  // let latlon = path.map(id => dijkstraPointsCoordinates[id])
  // const polyline = L.polyline(latlon, {
  // color: 'red',
  // weight: 4,
  // opacity: 0.8
  // }).addTo(map);
  // console.log('Check over here :', stations)
  //   for (let index = 0; index < stations.length; index++) {
  //     const element = stations[index];
  //     if (element.stop_name === sourceInputDijkstra.value) {
  //       console.log(element.stop_name);
  //       inputSrcDst.push(element.id);
  //     } else {
  //       continue;
  //     }
  //   }
  // console.log(inputSrcDst)

  //   axios
  //     .get(`https://backend-ot44.onrender.com/dijkstra/194/123`)
  //     .then(function (response) {
  //       const data = response.data.path;
  //       for (const key in data) {
  //         if (Object.prototype.hasOwnProperty.call(data, key)) {
  //           const element = data[key];
  //           path.push(element);
  //         }
  //       }
  //     })

  //   fetchDijkstraPath()
  //     console.log(`here djisktra : ${sourceDataMap.value}`)
  //         .finally(function () {
  //           // console.log(`This is the path : ${path}`)

  //             for (let index = 0; index < filterDjikstraStations.length; index++) {
  //               const element = filterDjikstraStations[index];
  //               L.marker([element.lat, element.lon])
  //                 .bindPopup(element.title + " " + element.line)
  //                 .addTo(map);
  //             }
  //             filterDjikstraStations.forEach((point) => {
  //               dijkstraPointsCoordinates[point.id] = [point.lat, point.lon];
  //             });
  //             let latlon = path.map((id) => dijkstraPointsCoordinates[id]);
  //             // console.log('My latlon', latlon)
  //             const polyline = L.polyline(latlon, {
  //               color: "blue",
  //               weight: 4,
  //               opacity: 0.8,
  //             }).addTo(map);
  //             // for (let index = 0; index < filterDjikstraStations.length; index++) {
  //             //         const element = filterDjikstraStations[index];
  //             //         const obj = {
  //             //             lat: element.lat,
  //             //             lon: element.lon
  //             //         }
  //             //         tempList.push(obj)
  //             //     }
  //             // console.log(filterDjikstraStations)
  //             // console.log(concreteData)
  //           });
  //       });
  //   });

  // const props = defineProps(
  //     {
  //         concorde: String
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
</style> */}
