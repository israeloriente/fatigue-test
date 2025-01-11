<template>
  <div class="list-group-item d-flex justify-content-between align-items-center">
    <p class="title">{{ $t("home.serialPort.title") }}</p>
    <div class="ms-auto d-flex gap-2">
      <p class="mt-3 icon" :title="getTitleIconClose" @click="closePort()">❌</p>
      <p class="mt-3 icon" :title="getTitleIconUpdate" @click="loadSerialPorts()">🔁</p>
    </div>
  </div>
  <select class="form-select mb-2" v-model="globalStore.arduinoPort" @change="selectPort()">
    <option v-for="port in serialPorts" :key="port" :value="port">
      {{ port }}
    </option>
  </select>
  <div class="ms-auto d-flex gap-2">
    <button
      type="button"
      class="btn btn-primary btn-sm ms-auto buttonColorBlue button"
      :disabled="globalStore.arduinoPort === ''"
      @click="selectPort()"
    >
      {{ $t("home.serialPort.button") }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useGlobalStore } from "../stores/useGlobalStore";
import GlobalService from "../services/global.service";
import { useI18n } from "vue-i18n";

const serialPorts = ref<string[]>([]);
const globalStore = useGlobalStore();
const { t } = useI18n();

onMounted(() => {
  loadSerialPorts().then(() => {
    globalStore.setArduinoPort(GlobalService.getStorage("config.arduinoPort"));
    if (serialPorts.value.includes(globalStore.arduinoPort)) selectPort();
  });
});

const loadSerialPorts = async () => {
  try {
    serialPorts.value = await window.serial.getSerialPorts();
  } catch (error) {
    console.error("Erro ao carregar as portas seriais:", error);
  }
};
const selectPort = async () => {
  try {
    window.serial.openSerialPort(globalStore.arduinoPort);
    globalStore.setArduinoPort(globalStore.arduinoPort);
    window.serial.writeSerial("arduino.setup");
    GlobalService.setStorage("config.arduinoPort", globalStore.arduinoPort);
  } catch (error) {
    console.error("Erro ao abrir a porta serial:", error);
  }
};

const closePort = async () => {
  try {
    if (globalStore.arduinoPort !== "") {
      window.serial.closeSerialPort();
      globalStore.setArduinoPort("");
      globalStore.setProcessItsRunning(false);
    }
  } catch (error) {
    console.error("Erro ao fechar a porta serial:", error);
  }
};

const getTitleIconClose = computed(() => {
  return t("home.serialPort.icons.close");
});
const getTitleIconUpdate = computed(() => {
  return t("home.serialPort.icons.update");
});
</script>

<style scoped lang="scss">
.buttonColorBlue {
  background-color: rgb(72, 163, 203);
  border-color: rgb(72, 163, 203);
}
.buttonColorBlue:hover {
  background-color: rgb(51, 155, 200);
}
.icon {
  cursor: pointer;
}
</style>
