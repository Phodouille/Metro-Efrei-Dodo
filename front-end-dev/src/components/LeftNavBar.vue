<template>
    <div class="left-nav-bar">
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

<style>
.left-nav-bar {
    display: flex;
}

.left-name-icon {
    margin-left: 50px;    
}



</style>

