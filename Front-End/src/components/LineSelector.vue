<script setup>
import "leaflet/dist/leaflet.js";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { onMounted } from "vue";

let map = null;

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
