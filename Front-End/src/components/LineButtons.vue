<template>
  <div class="line-buttons">
    <div class="network-header">
      <h2>Paris Network Subways</h2>
    </div>
    <!-- On boucle sur chaque groupe de 4 lignes -->
    <div
      v-for="(chunk, rowIndex) in chunkedLines"
      :key="rowIndex"
      class="line-row"
    >
      <button
        v-for="line in chunk"
        :key="line.name"
        class="line-btn"
        @click="selectLine(line.name)"
      >
        <component :is="line.component" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

// imports de tes logos
import Line1 from "./logo/line1.vue";
import Line2 from "./logo/line2.vue";
import Line3 from "./logo/line3.vue";
import Line3b from "./logo/line3b.vue";
import Line4 from "./logo/line4.vue";
import Line5 from "./logo/line5.vue";
import Line6 from "./logo/line6.vue";
import Line7 from "./logo/line7.vue";
import Line7b from "./logo/line7b.vue";
import Line8 from "./logo/line8.vue";
import Line9 from "./logo/line9.vue";
import Line10 from "./logo/line10.vue";
import Line11 from "./logo/line11.vue";
import Line12 from "./logo/line12.vue";
import Line13 from "./logo/line13.vue";
import Line14 from "./logo/line14.vue";

const lines = [
  { name: "1", component: Line1 },
  { name: "2", component: Line2 },
  { name: "3", component: Line3 },
  { name: "3b", component: Line3b },
  { name: "4", component: Line4 },
  { name: "5", component: Line5 },
  { name: "6", component: Line6 },
  { name: "7", component: Line7 },
  { name: "7b", component: Line7b },
  { name: "8", component: Line8 },
  { name: "9", component: Line9 },
  { name: "10", component: Line10 },
  { name: "11", component: Line11 },
  { name: "12", component: Line12 },
  { name: "13", component: Line13 },
  { name: "14", component: Line14 },
];

// Découpe en lignes de 4 boutons
const chunkedLines = computed(() => {
  const size = 4;
  const chunks = [];
  for (let i = 0; i < lines.length; i += size) {
    chunks.push(lines.slice(i, i + size));
  }
  return chunks;
});

function selectLine(lineName) {
  // on envoie "ligne1", "ligne2", etc.
  const apiParam = "ligne" + lineName;
  window.dispatchEvent(new CustomEvent("show-line", { detail: apiParam }));
}
</script>

<style scoped>
.line-buttons {
  position: absolute;
  top: 220px;
  right: 40px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-right: 20px;
}

.line-row {
  display: flex;
  gap: 60px;
  display: flex;
}

.line-btn {
  width: 48px;
  height: 48px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.15s;
  font-size: 25px;
  font-weight: 700;
  display: flex;
}
.line-btn:hover {
  transform: scale(1.1);
}

.network-header {
  font-family: "Open Sans";
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
