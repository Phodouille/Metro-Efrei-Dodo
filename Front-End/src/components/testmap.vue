<script setup>
import "leaflet/dist/leaflet.js";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { onMounted } from "vue";
// const marker = [];
// const layer = []
let layer = [];
onMounted(() => {
  const map = L.map("map").setView([48.86285403569893, 2.3448491571643038], 13);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  const subLayer1 = L.marker([48.853, 2.3499]).bindTooltip("📍 Notre-Dame", {
    permanent: true,
    direction: "top",
  }).bindPopup("This is a full popup shown on click");;

  const subLayer2 = L.marker([48.86686002066553, 2.3206535628176]).bindTooltip(
    "🗼 Champs-Élysées",
    { permanent: true, direction: "top" }
  ).bindPopup("This is a full popup shown on click");;

  layer.push(subLayer1, subLayer2);

  layer.forEach((marker) => {
    marker.addTo(map);
  });

  //   layer.addTo(map)
  //   for (let index = 0; index < layer.length; index++) {
  //     const element = layer[index];
  //     element.openPopup()
  //   }
  //   marker.push(L.marker([48.853, 2.3499]))
  //   // First marker in Paris (e.g., Notre-Dame)
  //   //   const marker1 = L.marker([48.853, 2.3499])
  //   //     .addTo(map)
  //   //     .bindPopup("📍 Notre-Dame de Paris")
  //   //     .openPopup()
  //   marker[1] = L.marker([48.8584, 2.2945])
  //   .bindPopup("🗼 Eiffel Tower");

  // Second marker in Paris (e.g., Eiffel Tower)
  //   const marker2 = L.marker([48.8584, 2.2945])
  //     .addTo(map)
  //     .bindPopup("🗼 Eiffel Tower")
  // .openPopup()

  // Force both popups open after map renders
  //   marker1.on("add", () => marker1.openPopup());
  //   marker2.on("add", () => marker2.openPopup());
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
