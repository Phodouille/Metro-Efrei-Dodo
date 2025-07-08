<template>
    <div class="metro-m-l">
      <div class="metro-m-logo">
        <span>M</span>
      </div>
      <div class="metro-3b-logo">
        <span>3b</span>
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
  .metro-3b-logo {
    width: 41px;
    height: 41px;
    border-radius: 50%;
    display: flex;
    background-color: #82c8e6;
    justify-content: center;
    align-items: center;
  }
  
  .metro-m-l {
    display: flex;
    width: 85px;
    justify-content: space-between;
  }
  
  span {
    font-family: "Open Sans";
  }
  </style>
  