<template>
  <div id="content">
    <Toolbar />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import Toolbar from "./components/Toolbar.vue";
</script>

<style scoped>
/* #content {
  width: 1000px;
  height: 735px;
  border: 1px solid #000;
} */
</style>
