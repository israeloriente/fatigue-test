<template>
  <p class="title">Controles</p>
  <ul class="list-group">
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ "Motor de passo" }}</p>
      <Toggle
        :disabled="arduinoPortIsEmpty"
        :value="globalStore.motorLapTurnOn"
        @changed="motorGiroChanged"
        ref="motorLapTurnOn"
      />
    </li>
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ "Sentido da rotação (Horário)" }}</p>
      <Toggle :disabled="arduinoPortIsEmpty" />
    </li>
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ "Sensor de carga" }}</p>
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

const globalStore = useGlobalStore();
const motorLapTurnOn = ref<typeof Toggle | null>(null);
const motorWeightTurnOn = ref<typeof Toggle | null>(null);

// Função chamada quando o valor muda
const motorGiroChanged = (value: boolean) => {
  if (value) {
    window.serial.writeSerial("motorLap.start");
    globalStore.setLoadingStatusTurns(true);
    setTimeout(() => {
      if (!globalStore.motorLapTurnOn) motorLapTurnOn.value?.changeLocalValue();
      globalStore.setLoadingStatusTurns(false);
    }, 2000);
  } else {
    window.serial.writeSerial("motorLap.stop");
    globalStore.setLoadingStatusTurns(true);
    setTimeout(() => {
      if (globalStore.motorLapTurnOn) motorLapTurnOn.value?.changeLocalValue();
      globalStore.setLoadingStatusTurns(false);
    }, 2000);
  }
};

const motorWeightChanged = (value: boolean) => {
  if (value) {
    window.serial.writeSerial("motorWeight.start");
    globalStore.setLoadingStatusWeight(true);
    setTimeout(() => {
      if (!globalStore.motorWeightTurnOn) motorWeightTurnOn.value?.changeLocalValue();
      globalStore.setLoadingStatusWeight(false);
    }, 2000);
  } else {
    window.serial.writeSerial("motorWeight.stop");
    globalStore.setLoadingStatusWeight(true);
    setTimeout(() => {
      if (globalStore.motorWeightTurnOn) motorWeightTurnOn.value?.changeLocalValue();
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
