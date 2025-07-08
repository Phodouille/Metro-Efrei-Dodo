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
  { label: "Network",   group: "map",   active: false },
  { label: "MST",       group: "map",   active: false },
  { label: "Connexity", group: "panel", active: false },
  { label: "News",      group: "panel", active: false },
]);

function onSelect(selected) {
  // si on reclique sur le même bouton actif, on le désactive
  const willActivate = !selected.active;

  if (selected.group === "map") {
    // désactive tout le groupe map, puis active si besoin
    toggles
      .filter(t => t.group === "map")
      .forEach(t => t.active = false);
    if (willActivate) selected.active = true;

    window.dispatchEvent(new CustomEvent("show-network", {
      detail: toggles.find(t => t.label === "Network").active
    }));
    window.dispatchEvent(new CustomEvent("show-mst", {
      detail:       toggles.find(t => t.label === "MST").active
    }));

  } else {
    // désactive tout le groupe panel, puis active si besoin
    toggles
      .filter(t => t.group === "panel")
      .forEach(t => t.active = false);
    if (willActivate) selected.active = true;

    window.dispatchEvent(new CustomEvent("show-connexity", {
      detail: toggles.find(t => t.label === "Connexity").active
    }));
    window.dispatchEvent(new CustomEvent("show-news", {
      detail: toggles.find(t => t.label === "News").active
    }));
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
