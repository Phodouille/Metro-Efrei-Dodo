<template>
  <div
    class="rectangle"
    v-if="displayLinesAsArray.length > 0"
    @click="showDetails = !showDetails"
  >
    <div class="show-details" v-if="showDetails">
      <div v-for="element in displayDijkstraPathName" :key="element" class="li">
        <ul>
          <li>
            {{ element }}
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      <div class="metro-line-logo">
        <template
          v-for="(lineName, index) in displayLinesAsArray"
          :key="lineName"
        >
          <!-- Render the component -->
          <component :is="lineComponents[lineName]" />

          <!-- Arrow between components -->
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
      <div class="footer">
        <div class="svg-price">
          <div class="price-svg">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="35"
              height="35"
              viewBox="0 0 35 35"
              fill="none"
            >
              <path
                d="M6.5625 11.6667L21.9917 4.2875C22.1666 4.20379 22.3564 4.15579 22.5501 4.14633C22.7438 4.13687 22.9374 4.16613 23.1196 4.23239C23.3019 4.29866 23.4691 4.40061 23.6114 4.53227C23.7538 4.66393 23.8685 4.82266 23.9488 4.99917L26.9792 11.6667"
                stroke="black"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M8.75 14.5834V11.6667"
                stroke="black"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M8.75 20.4167V21.875"
                stroke="black"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M8.75 27.7083V30.625"
                stroke="black"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M29.1665 11.6667H5.83317C4.22234 11.6667 2.9165 12.9725 2.9165 14.5834V27.7084C2.9165 29.3192 4.22234 30.625 5.83317 30.625H29.1665C30.7773 30.625 32.0832 29.3192 32.0832 27.7084V14.5834C32.0832 12.9725 30.7773 11.6667 29.1665 11.6667Z"
                stroke="black"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </div>
          <div class="ticket-price">
            <h4>2.50€</h4>
          </div>
        </div>
        <div class="right-side">
          <div class="duration-min">
            <div class="duration">
              {{ displayDijkstraDuration }}
            </div>
            <div class="min">
              <h4>min</h4>
            </div>
          </div>
        </div>
      </div>
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
import line13 from "../components/logo/line13.vue";
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
  ligne13: line13,
  ligne14: line14,
};

const store = useNewStore();

const displayDijkstraPathName = ref([]);
const displayDijkstraPathLine = ref([]);
const displayRemoveDuplicateDijkstraPathLine = ref([]);
const displayDijkstraDuration = ref(0);
const showDetails = ref(false);

// Convert to array for rendering
const displayLinesAsArray = computed(() =>
  Array.from(displayRemoveDuplicateDijkstraPathLine.value)
);

const removeConsecutiveDuplicates = () => {
  displayRemoveDuplicateDijkstraPathLine.value = [];

  const arr = displayDijkstraPathLine.value;
  if (arr.length === 0) return;

  const first = arr[0];
  const rest = arr.slice(1);

  // Check if the first element appears again
  const firstAppearsAgain = rest.includes(first);

  let deduped = [];

  if (firstAppearsAgain) {
    deduped.push(first);
  }

  for (let i = 1; i < arr.length; i++) {
    const current = arr[i];
    const previous = arr[i - 1];
    if (current !== previous) {
      deduped.push(current);
    }
  }

  displayRemoveDuplicateDijkstraPathLine.value = deduped;
};

watch(
  () => [
    store.pathDijkstraName,
    store.pathDijkstraLine,
    store.pathDijkstraDuration,
  ],
  ([newNames, newLines, newDuration]) => {
    displayDijkstraPathName.value = newNames;
    displayDijkstraPathLine.value = newLines;
    console.log("CHECK ABSOULTELY HERE", displayDijkstraPathLine.value);
    removeConsecutiveDuplicates();
    console.log(
      "Remove duplicates",
      displayRemoveDuplicateDijkstraPathLine.value
    );
    displayDijkstraDuration.value = newDuration;
  }
);
</script>

<style scoped>
.rectangle {
  margin-top: 20px;
  width: 540px;
  border: solid 1px black;
  background-color: white;
  border-radius: 30px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  height: auto;
}

.metro-line-logo {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: start;
  flex-wrap: wrap;
}

.price,
.time {
  margin-top: 10px;
}

.svg-price {
  display: flex;
  margin-top: 45px;
  font-size: large;
  align-items: center;
  margin-left: 5px;
}

.price-svg {
  display: flex;
  justify-content: center;
  align-items: center;
}

.ticket-price {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 10px;
  margin-top: 5px;
}

.footer {
  display: flex;
  flex-direction: row;
  height: 95px;
}

.duration {
  display: flex;
  font-size: 55px;
  flex-direction: column;
  justify-content: flex-end;
}

.min {
  display: flex;
  align-items: flex-start;
  margin-top: 11px;
}

.duration-min {
  display: flex;
  margin-left: 19rem;
}

.right-side {
  display: flex;
  justify-content: flex-end;
}

.li {
  font-family: "Open Sans";
  font-size: small;
  font-weight: lighter;
}

ul li {
  margin-bottom: 1px;
  height: 20px;
}

ul {
  list-style-type: disc;
}

.show-details {
  margin-top: -20px;
  padding-bottom: 20px;
}
</style>
