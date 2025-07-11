<template>
  <div class="metro-m-l">
    <div class="metro-m-logo">
      <span>M</span>
    </div>
    <div class="metro-1-logo">
      <span>1</span>
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
.metro-1-logo {
  width: 41px;
  height: 41px;
  border-radius: 50%;
  display: flex;
  background-color: rgba(255,190,0,255);
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
    font-family: 'Open Sans';
}
</style>
