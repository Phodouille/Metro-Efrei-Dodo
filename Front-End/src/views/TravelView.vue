<template>
  <div class="background">
    <div class="row">
      <div class="header">
        <h1>
          Time to ride ! <br />
          Where to this time ?
        </h1>
        <SearchBar />
        <CardDetails />
      </div>
      <div class="map">
        <Map />
      </div>
    </div>
  </div>
</template>

<script setup>
import SearchBar from "../components/SearchBar.vue";
import Map from "../components/Map.vue";
import CardDetails from "../components/CardDetails.vue";
</script>

<style>
.header {
  padding-left: 28px;
  padding-top: 26px;
  font-size: 26px;
  font-weight: 700;
  line-height: 62px;
  letter-spacing: 1.84px;
  font-family: "Open Sans";
}

.background {
  background-color: #f6f6f6;
  /* background-color: aqua; */
  display: flex;
  flex-direction: column;
  width: 83vw;
  border-radius: 5px;
  display: flex;
  padding: 8px 8px;
  box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.25);
  padding-bottom: 35px;
}

.row {
    display: flex;
}
</style>
