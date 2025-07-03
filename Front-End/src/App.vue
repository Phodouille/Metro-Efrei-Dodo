<template>
  <div class="container">
    <div class="left-side-bar">
      <div class="MetroGo">
        <MetroGo />
      </div>
      <div class="left-nav-component">
        <span class="left-nav-button"><LeftNavBar LeftNameSideBar="Travel" :LeftSideBarIcon="TravelSvgIcon" @click="() => goTo('/travel')"/></span>
        <span class="left-nav-button"><LeftNavBar LeftNameSideBar="Graph" :LeftSideBarIcon="GraphSvgIcon" @click="() => goTo('/graph')"/></span>
        <span class="left-nav-button"><LeftNavBar LeftNameSideBar="Recents" :LeftSideBarIcon="RecentsSvgIcon" @click="() => goTo('/recents')"/></span>
        <span class="left-nav-button"><LeftNavBar LeftNameSideBar="Saved" :LeftSideBarIcon="SavedSvgIcon" @click="() => goTo('/saved')"/></span>
      </div>  
    </div>
    <div class="center-side">
      <RouterView /> 
    </div>
  </div>

</template>

<script setup>
import { useRouter } from 'vue-router'
import LeftNavBar from './components/LeftNavBar.vue';
import MetroGo from './components/MetroGo.vue';
const router = useRouter()
const goTo = (path) => {
  router.push(path)
}
const TravelSvgIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-train-front-icon lucide-train-front"><path d="M8 3.1V7a4 4 0 0 0 8 0V3.1"/><path d="m9 15-1-1"/><path d="m15 15 1-1"/><path d="M9 19c-2.8 0-5-2.2-5-5v-4a8 8 0 0 1 16 0v4c0 2.8-2.2 5-5 5Z"/><path d="m8 19-2 3"/><path d="m16 19 2 3"/></svg>`
const GraphSvgIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-route-icon lucide-route"><circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/></svg>`
const RecentsSvgIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-history-icon lucide-history"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/></svg>`
const SavedSvgIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bookmark-icon lucide-bookmark"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>`
</script>

<style scoped>
.left-side-bar {
  display: flex;
  flex-direction: column;
  width: 15vw;
  height: 98.5vh;
  /* background-color: purple; */
}

.MetroGo {
  padding-top: 66px;
  padding-left: 37px;
  padding-right: 66px;
  padding-bottom: 64px;
}
 
.left-nav-component {
  display: flex;
  flex-direction: column;
  height: 400px;
  justify-content: space-between;
}

.left-nav-button {
  border-left: 5px solid transparent;
  cursor: pointer;
}

.left-nav-button:hover {
  border-left-color: rgb(0, 0, 0);
}

.container {
  display: flex;
  width: 100%;
}

</style>