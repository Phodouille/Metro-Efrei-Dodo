<template>
    <div class="left-nav-bar" @click="$emit('click')">
            <div class="left-icon-side-bar">
                <span v-html="LeftSideBarIcon"></span>
            </div>
            <div class="left-name-icon">
                <p>{{ LeftNameSideBar }}</p>
            </div>
    </div>
</template>

<script setup>
defineProps({
    LeftNameSideBar: String,
    LeftSideBarIcon: String
})
</script>

<style scoped>
.left-nav-bar {
    display: flex;
    margin-left: 38px;
    align-items: center;
}

.left-name-icon {
    margin-left: 38px;
    font-family: 'Open Sans';
    font-size: 22px;   
    font-weight: 700;
}



</style>

