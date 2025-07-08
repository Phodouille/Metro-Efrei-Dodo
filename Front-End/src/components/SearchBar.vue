<template>
  <div class="rectangle">
    <div class="rectangle-content">
      <div class="start-end">
        <p>From</p>
      </div>
      <div class="icon-input-container">
        <div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M20 10.0001C20 14.9931 14.461 20.1931 12.601 21.7991C12.4277 21.9294 12.2168 21.9998 12 21.9998C11.7832 21.9998 11.5723 21.9294 11.399 21.7991C9.539 20.1931 4 14.9931 4 10.0001C4 7.87833 4.84285 5.8435 6.34315 4.34321C7.84344 2.84292 9.87827 2.00006 12 2.00006C14.1217 2.00006 16.1566 2.84292 17.6569 4.34321C19.1571 5.8435 20 7.87833 20 10.0001Z"
              stroke="black"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M12 13.0001C13.6569 13.0001 15 11.6569 15 10.0001C15 8.34321 13.6569 7.00006 12 7.00006C10.3431 7.00006 9 8.34321 9 10.0001C9 11.6569 10.3431 13.0001 12 13.0001Z"
              stroke="black"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>
        <div class="input-zone">
          <input
            type="text"
            class="input"
            v-model="source"
            placeholder="Enter a starting station name"
            @input="showSourceSuggestions = true"
            @blur="showSourceSuggestions = false"
            autocomplete="off"
          />
          <ul
            v-if="showSourceSuggestions && filteredSourceSuggestions.length > 0"
          >
            <li
              v-for="suggestion in filteredSourceSuggestions"
              :key="suggestion"
              @mousedown="source = suggestion"
            >
              {{ suggestion }}
            </li>
          </ul>
        </div>
      </div>
      <div class="bullet-point-container">
        <div class="bullet-point"></div>
        <div class="bullet-point"></div>
        <div class="bullet-point"></div>
      </div>
      <div class="start-end">
        <p>To</p>
      </div>
      <div class="icon-input-container">
        <div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"
              stroke="black"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M12 16L16 12L12 8"
              stroke="black"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M8 12H16"
              stroke="black"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>
        <div class="input-zone">
          <input
            type="text"
            class="input"
            v-model="destination"
            placeholder="Enter a destination station name"
            @input="showDestinationSuggestions = true"
            @blur="showDestinationSuggestions = false"
            autocomplete="off"
          />
          <ul
            v-if="
              showDestinationSuggestions &&
              filteredDestinationSuggestions.length > 0
            "
          >
            <li
              v-for="suggestion in filteredDestinationSuggestions"
              :key="suggestion"
              @mousedown="destination = suggestion"
            >
              {{ suggestion }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="button-center">
      <button class="send-button" v-on:click="sendSourceDestination">
        <p>Go</p>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useNewStore } from "../stores/path.js";
import axios from "axios";

const store = useNewStore();
const source = ref("");
const destination = ref("");
const showSourceSuggestions = ref(false);
const showDestinationSuggestions = ref(false);
const stations = ref([]);

// Suggestion for "From"
const filteredSourceSuggestions = computed(() => {
  if (!source.value || source.value.length < 2) return [];
  return stations.value
    .filter((station) =>
      station.stop_name.toLowerCase().includes(source.value.toLowerCase())
    )
    .slice(0, 5)
    .map((station) => station.stop_name);
});

// Suggestion for "To"
const filteredDestinationSuggestions = computed(() => {
  if (!destination.value || destination.value.length < 2) return [];
  return stations.value
    .filter((station) =>
      station.stop_name.toLowerCase().includes(destination.value.toLowerCase())
    )
    .slice(0, 5)
    .map((station) => station.stop_name);
});

const sendSourceDestination = () => {
  store.sourceData = source.value;
  store.destinationData = destination.value;
  console.log(store.sourceData);
  console.log(store.destinationData);
  source.value = "";
  destination.value = "";
};

onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/stations/");
    stations.value = response.data;
  } catch (error) {
    console.error("Erreur:", error);
  }
});
</script>

<style scoped>
.rectangle {
  background-color: white;
  width: 555px;
  height: 220px;
  border-radius: 25px;
  border: 2px solid #000;
  display: flex;
  flex-direction: row;
}

.start-end {
  font-family: "Open Sans";
  font-weight: 700;
  color: #ddd;
  margin-top: -30px;
}

.rectangle-content {
  margin-left: 14px;
}

.icon-input-container {
  display: flex;
  flex-direction: row;
  margin-top: -53px;
}

.input {
  border-top: none;
  border-left: none;
  border-right: none;
  outline: none;
  border-color: #bfbfbf;
  padding-bottom: 5px;
  width: 310px;
  font-size: 20px;
}

.input-zone {
  margin-left: 10px;
}

.input:focus {
  border-bottom-color: black;
}

.bullet-point {
  width: 6px;
  height: 6.412px;
  background-color: black;
  border-radius: 50%;
}

.bullet-point-container {
  margin-top: -10px;
  margin-left: 9px;
  height: 35px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

ul {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  margin: 0;
  padding: 0;
  font-weight: lighter;
  font-size: 18px;
  list-style-type: none;
}

li {
  padding: 8px;
  cursor: pointer;
}

li:hover {
  background: #f0f0f0;
}

input::placeholder {
  color: rgba(212, 212, 212, 0.927);
}

.send-button {
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 40px;
  margin-bottom: 10px;
  margin-left: 26px;
  width: 147px;
  height: 145px;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.send-button p {
  font-family: "Open Sans";
  font-size: 85px;
}
.button-center {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.send-button:hover {
  background-color: #f6f6f6;
  color: black;
  border: solid black 2px;
  transition: background-color 0.3s ease-in-out;
}
</style>
