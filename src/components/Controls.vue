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
      <Toggle
        :disabled="arduinoPortIsEmpty"
        :value="globalStore.directionRotation"
        @changed="directionRotationChanged"
        ref="directionRotation"
      />
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
const directionRotation = ref<typeof Toggle | null>(null);

// Função chamada quando o valor muda
const motorGiroChanged = (value: boolean) => {
  if (value) {
    window.socket.writeSocket({ motorLapTurnOn: true });
    globalStore.setLoadingStatusTurns(true);
    setTimeout(() => {
      if (!globalStore.motorLapTurnOn) {
        motorLapTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.raspberryNotConnected");
      }
      globalStore.setLoadingStatusTurns(false);
    }, 1000);
  } else {
    window.socket.writeSocket({ motorLapTurnOn: false });
    globalStore.setLoadingStatusTurns(true);
    setTimeout(() => {
      if (globalStore.motorLapTurnOn) {
        motorLapTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.raspberryNotConnected");
      }
      globalStore.setLoadingStatusTurns(false);
    }, 1000);
  }
};

const motorWeightChanged = (value: boolean) => {
  if (value) {
    window.socket.writeSocket({ motorWeightTurnOn: true });
    globalStore.setLoadingStatusWeight(true);
    setTimeout(() => {
      if (!globalStore.motorWeightTurnOn) {
        motorWeightTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.raspberryNotConnected");
      }
      globalStore.setLoadingStatusWeight(false);
    }, 1000);
  } else {
    window.socket.writeSocket({ motorWeightTurnOn: false });
    globalStore.setLoadingStatusWeight(true);
    setTimeout(() => {
      if (globalStore.motorWeightTurnOn) {
        motorWeightTurnOn.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.raspberryNotConnected");
      }
      globalStore.setLoadingStatusWeight(false);
    }, 1000);
  }
};

const directionRotationChanged = (value: boolean) => {
  if (value) {
    window.socket.writeSocket({ directionRotation: true });
    globalStore.setLoadingStatusDirection(true);
    setTimeout(() => {
      if (!globalStore.directionRotation) {
        directionRotation.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.raspberryNotConnected");
      }
      globalStore.setLoadingStatusDirection(false);
    }, 1000);
  } else {
    window.socket.writeSocket({ directionRotation: false });
    globalStore.setLoadingStatusDirection(true);
    setTimeout(() => {
      if (globalStore.directionRotation) {
        directionRotation.value?.changeLocalValue();
        GlobalService.simpleAlert("simpleAlert.raspberryNotConnected");
      }
      globalStore.setLoadingStatusDirection(false);
    }, 1000);
  }
};

const arduinoPortIsEmpty = computed(() => {
  return globalStore.wifiSelected.ip === "";
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
