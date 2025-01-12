<template>
  <p class="title">{{ $t("config.title") }}</p>
  <ul class="list-group">
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ $t("home.controls.motorLap") }}</p>
      <Toggle
        :disabled="arduinoPortIsEmpty"
        :value="globalStore.motorLapTurnOn"
        @changed="motorGiroChanged"
        ref="motorLapTurnOn"
      />
    </li>
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ $t("home.controls.directionRotation") }}</p>
      <Toggle :disabled="arduinoPortIsEmpty" />
    </li>
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ $t("home.controls.motorWeight") }}</p>
      <Toggle
        :disabled="arduinoPortIsEmpty"
        :value="globalStore.motorWeightTurnOn"
        @changed="motorWeightChanged"
        ref="motorWeightTurnOn"
      />
    </li>
  </ul>
</template>

<script setup lang="ts">
import Toggle from "./Toggle.vue";
import { useGlobalStore } from "../stores/useGlobalStore";
import { computed, ref } from "vue";
import GlobalService from "../services/global.service";

const globalStore = useGlobalStore();
const motorLapTurnOn = ref<typeof Toggle | null>(null);
const motorWeightTurnOn = ref<typeof Toggle | null>(null);

// Função chamada quando o valor muda
const motorGiroChanged = (value: boolean) => {
  if (value) {
    window.serial.writeSerial("motorLap.start");
    globalStore.setLoadingStatusTurns(true);
    setTimeout(() => {
      if (!globalStore.motorLapTurnOn) {
        motorLapTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.arduinoNotConnected");
      }
      globalStore.setLoadingStatusTurns(false);
    }, 2000);
  } else {
    window.serial.writeSerial("motorLap.stop");
    globalStore.setLoadingStatusTurns(true);
    setTimeout(() => {
      if (globalStore.motorLapTurnOn) {
        motorLapTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.arduinoNotConnected");
      }
      globalStore.setLoadingStatusTurns(false);
    }, 2000);
  }
};

const motorWeightChanged = (value: boolean) => {
  if (value) {
    window.serial.writeSerial("motorWeight.start");
    globalStore.setLoadingStatusWeight(true);
    setTimeout(() => {
      if (!globalStore.motorWeightTurnOn) {
        motorWeightTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.arduinoNotConnected");
      }
      globalStore.setLoadingStatusWeight(false);
    }, 2000);
  } else {
    window.serial.writeSerial("motorWeight.stop");
    globalStore.setLoadingStatusWeight(true);
    setTimeout(() => {
      if (globalStore.motorWeightTurnOn) {
        motorWeightTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.arduinoNotConnected");
      }
      globalStore.setLoadingStatusWeight(false);
    }, 2000);
  }
};

const arduinoPortIsEmpty = computed(() => {
  return globalStore.arduinoPort === "";
});
</script>

<style scoped lang="scss">
.item {
  padding: 5px;
}

.label {
  margin: 0;
  font-size: 13px;
}
</style>
