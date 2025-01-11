<template>
  <div id="content">
    <Toolbar />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import Toolbar from "./components/Toolbar.vue";
import { useI18n } from "vue-i18n";
import GlobalService from "./services/global.service";
import { useGlobalStore } from "./stores/useGlobalStore";

const { locale } = useI18n();
const globalStore = useGlobalStore();

onMounted(() => {
  const currentLanguage: "en" | "pt" = GlobalService.getStorage("config.defaultLanguage") || "en";
  locale.value = currentLanguage;
  globalStore.changeLanguage(currentLanguage);
});
</script>

<style scoped>
/* #content {
  width: 1000px;
  height: 735px;
  border: 1px solid #000;
} */
</style>
