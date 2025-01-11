<template>
  <div class="list-group-item d-flex justify-content-between align-items-center">
    <p class="title">Selecione a porta serial</p>
    <div class="ms-auto d-flex gap-2">
      <p class="mt-3 icon" title="Desconectar Porta Serial" @click="closePort()">❌</p>
      <p class="mt-3 icon" title="Atualizar Lista" @click="loadSerialPorts()">🔁</p>
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
      Conectar
    </button>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useGlobalStore } from "../stores/useGlobalStore";
import GlobalService from "../services/global.service";

const serialPorts = ref<string[]>([]);
const globalStore = useGlobalStore();

onMounted(() => {
  loadSerialPorts();
  globalStore.setArduinoPort(GlobalService.getStorage("config.arduinoPort"));
  if (globalStore.arduinoPort) selectPort();
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
    const result = await window.serial.openSerialPort(globalStore.arduinoPort);
    globalStore.setArduinoPort(globalStore.arduinoPort);
    globalStore.addLog({ type: "success", message: result });
    GlobalService.setStorage("config.arduinoPort", globalStore.arduinoPort);
  } catch (error) {
    console.error("Erro ao abrir a porta serial:", error);
  }
};

const closePort = async () => {
  try {
    window.serial.closeSerialPort();
    globalStore.setArduinoPort("");
    globalStore.setProcessItsRunning(false);
  } catch (error) {
    console.error("Erro ao fechar a porta serial:", error);
  }
};
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
