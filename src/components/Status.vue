<template>
  <p class="title">{{ $t("home.status.title") }}</p>

  <div>
    <span
      class="buttons fakeClose"
      v-bind:class="{
        green: arduinoPortIsConnected,
      }"
    ></span>
    <span> {{ $t("home.status.serialPort") }} </span>
  </div>
  <div>
    <span class="buttons fakeClose" v-bind:class="{ green: globalStore.scaleStatus }"></span>
    <span> {{ $t("home.status.scale") }} </span>
  </div>
  <div>
    <span
      class="buttons fakeClose"
      v-bind:class="{
        green: globalStore.motorLapTurnOn,
        yellow: isLoadingLap,
      }"
    ></span>
    <span> {{ $t("home.status.motorLap") }} </span>
  </div>
  <div>
    <span
      class="buttons fakeClose"
      v-bind:class="{
        green: globalStore.motorWeightTurnOn,
        yellow: isLoadingWeight,
      }"
    ></span>
    <span> {{ $t("home.status.motorWeight") }} </span>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useGlobalStore } from "../stores/useGlobalStore";

const globalStore = useGlobalStore();

onMounted(() => {});

const isLoadingLap = computed(() => {
  return globalStore.loadingStatus.lap;
});
const isLoadingWeight = computed(() => {
  return globalStore.loadingStatus.weight;
});
const arduinoPortIsConnected = computed(() => {
  return globalStore.arduinoPort !== "";
});
</script>

<style scoped lang="scss">
.buttons {
  height: 10px;
  width: 10px;
  border-radius: 50%;
  border: 1px solid #000;
  position: relative;
  background-color: #ff3b47;
  border-color: #9d252b;
  display: inline-block;
}

.green {
  background-color: #00d742;
  border-color: #049931;
}

.yellow {
  background-color: #ffc100;
  border-color: #9d802c;
}
</style>
