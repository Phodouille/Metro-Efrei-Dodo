<template>
    <div class="metro-m-l">
      <div class="metro-m-logo">
        <span>M</span>
      </div>
      <div class="metro-7b-logo">
        <span>7b</span>
      </div>
    </div>
  </template>
  
  <script setup></script>
  
  <style scoped>
  .metro-m-logo {
    width: 37px;
    height: 37px;
    border: solid 2px black;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .metro-7b-logo {
    width: 41px;
    height: 41px;
    border-radius: 50%;
    display: flex;
    background-color: #81dc73;
    justify-content: center;
    align-items: center;
  }
  
  .metro-m-l {
    display: flex;
    width: 85px;
    justify-content: space-between;
    gap: 5px;
  }
  
  span {
    font-family: "Open Sans";
  }
  </style>
  