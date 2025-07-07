<template>
  <div class="sidebar">
    <div
      v-for="item in toggles"
      :key="item.label"
      class="sidebar-item"
    >
      <button
        class="sidebar-btn"
        :class="{ active: item.active }"
        @click="onSelect(item)"
      >
        {{ item.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";

const toggles = reactive([
    { label: "Network", active: false },
  { label: "MST", active: false },
  { label: "Connexity", active: false },
  { label: "Traffic", active: false },
]);

function onSelect(selectedItem) {
  toggles.forEach(item => {
    item.active = (item === selectedItem);
  });
  // Événement global pour chaque bouton (un seul actif à la fois)
  window.dispatchEvent(new CustomEvent("show-mst", { detail: false }));
  window.dispatchEvent(new CustomEvent("show-connexity", { detail: false }));
  window.dispatchEvent(new CustomEvent("show-network", { detail: false }));
  window.dispatchEvent(new CustomEvent("show-traffic", { detail: false }));

  if (selectedItem.label === "Connexity") {
    window.dispatchEvent(new CustomEvent("show-connexity", { detail: true }));
  } else if (selectedItem.label === "Network") {
    window.dispatchEvent(new CustomEvent("show-network", { detail: true }));
  } else if (selectedItem.label === "MST") {
    window.dispatchEvent(new CustomEvent("show-mst", { detail: true }));
  } else if (selectedItem.label === "Traffic") {
    window.dispatchEvent(new CustomEvent("show-traffic", { detail: true }));
  }
}
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 18px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 0 8px 2px rgba(54,54,54,0.12);
  padding: 24px 18px;
  position: absolute;
  top: 40px;
  right: 40px;
  z-index: 1000;
  min-width: 170px;
}
.sidebar-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.sidebar-btn {
  width: 100%;
  padding: 10px 0;
  border: none;
  border-radius: 12px;
  background: #f2f2f2;
  font-weight: 600;
  font-size: 1.1em;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.sidebar-btn.active {
  background: #222;
  color: #fff;
}
</style>
