<template>
    <div class="background">
        <div class="header">
            <h1>Time to ride ! <br> Where to this time ?</h1>
            <SearchBar />
        </div>
        <div class="map">
            <Map />
        </div>
    </div>
    
</template>

<script setup>

import SearchBar from '../components/SearchBar.vue';
import Map from '../components/Map.vue';

</script>

<style>
    .header {
        padding-left: 28px;
        padding-top: 26px;
        font-size: 26px;
        font-weight: 700;
        line-height: 62px;
        letter-spacing: 1.84px;
        font-family: 'Open Sans';
    }

    .background {
        background-color: #F6F6F6;
        /* background-color: aqua; */
        height: 98.5vh;
        width: 1489px;
        border-radius: 10px;
        display: flex;
    }
</style>