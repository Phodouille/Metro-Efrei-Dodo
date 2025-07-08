<template>
    <div class="rectangle">
      <div class="metro-line-logo">
        <template v-for="(lineName, index) in displayLinesAsArray" :key="lineName">
          <!-- Render the line component -->
          <component :is="lineComponents[lineName]" />
  
          <!-- Custom SVG arrow between components -->
          <svg
            v-if="index < displayLinesAsArray.length - 1"
            xmlns="http://www.w3.org/2000/svg"
            width="12"
            height="20"
            viewBox="0 0 12 20"
            fill="none"
          >
            <path
              d="M1.11279 19L10.2059 10L1.11279 1"
              stroke="black"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </template>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, computed } from "vue";
  import { useNewStore } from "../stores/path.js";
  
  // Import all line components
  import line1 from "../components/logo/line1.vue";
  import line2 from "../components/logo/line2.vue";
  import line3 from "../components/logo/line3.vue";
  import line3b from "../components/logo/line3b.vue";
  import line4 from "../components/logo/line4.vue";
  import line5 from "../components/logo/line5.vue";
  import line6 from "../components/logo/line6.vue";
  import line7 from "../components/logo/line7.vue";
  import line7b from "../components/logo/line7b.vue";
  import line8 from "../components/logo/line8.vue";
  import line9 from "../components/logo/line9.vue";
  import line10 from "../components/logo/line10.vue";
  import line11 from "../components/logo/line11.vue";
  import line12 from "../components/logo/line12.vue";
  import line14 from "../components/logo/line14.vue";
  
  // Line name → component map
  const lineComponents = {
    ligne1: line1,
    ligne2: line2,
    ligne3: line3,
    ligne3b: line3b,
    ligne4: line4,
    ligne5: line5,
    ligne6: line6,
    ligne7: line7,
    ligne7b: line7b,
    ligne8: line8,
    ligne9: line9,
    ligne10: line10,
    ligne11: line11,
    ligne12: line12,
    ligne14: line14,
  };
  
  const store = useNewStore();
  
  const displayDijkstraPathName = ref([]);
  const displayDijkstraPathLine = ref([]);
  const displaySetDijkstraPathLine = ref(new Set());
  
  // Convert Set to array for rendering
  const displayLinesAsArray = computed(() =>
    Array.from(displaySetDijkstraPathLine.value)
  );
  
  // Watch for store updates
  watch(
    () => [store.pathDijkstraName, store.pathDijkstraLine],
    ([newNames, newLines]) => {
      displayDijkstraPathName.value = newNames;
      displayDijkstraPathLine.value = newLines;
      displaySetDijkstraPathLine.value = new Set(newLines); // reset with new lines
      console.log("Line components to display:", displaySetDijkstraPathLine.value);
    }
  );
  </script>
  
  <style scoped>
  .rectangle {
    margin-top: 20px;
    width: 555px;
    height: 160px;
    border: solid 1px black;
    background-color: white;
    border-radius: 30px;
    padding: 10px;
  }
  
  .metro-line-logo {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: start;
  }
  
  .price,
  .time {
    margin-top: 10px;
  }
  </style>