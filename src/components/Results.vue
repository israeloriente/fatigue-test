<template>
  <div class="result">
    <p class="title text-center">{{ $t("home.results.title") }}</p>
    <ul class="list-group">
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">{{ $t("home.results.theoreticalLife") }}</span>
        <span>0</span>
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">{{ $t("home.results.testDuration") }}</span>
        <StopWatchComponent ref="stopWatchRef" />
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">{{ $t("home.results.life") }}</span>
        <span>0</span>
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">{{ $t("home.results.error") }}</span>
        <span>0</span>
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">{{ $t("home.results.turnCount") }}</span>
        <span>{{ globalStore.countOfTurns }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useGlobalStore } from "../stores/useGlobalStore";
import StopWatchComponent from "./StopWatchComponent.vue";

const globalStore = useGlobalStore();
const stopWatchRef = ref();

watch(
  () => globalStore.chegouAoPeso,
  (newValue) => {
    console.log("chegouAoPeso", newValue);
    if (newValue && globalStore.projectIsRunning) {
      stopWatchRef.value.init(new Date(), undefined, true);
    }
  },
  { immediate: false }
);
watch(
  () => globalStore.projectIsRunning,
  (newValue) => {
    if (newValue) {
      stopWatchRef.value.timerDisplay = "00:00:00";
    } else stopWatchRef.value.stopCount();
  },
  { immediate: false }
);
</script>

<style scoped lang="scss">
.result {
  position: absolute;
  top: 50.5px;
  left: 555px;
  width: 420px;
  height: 230px;
  padding: 10px;
  border-radius: 10px;
  background-color: #f1f1f1;

  .item {
    padding: 4.5px 7px;
  }
  .label {
    margin: 0;
    font-size: 15px;
  }
}
</style>
