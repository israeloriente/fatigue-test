<template>
  <div class="list-group-item d-flex justify-content-between align-items-center">
    <p class="title">{{ $t("home.wifi.title") }}</p>
    <div class="ms-auto d-flex gap-2">
      <p class="mt-3 icon" :title="getTitleIconClose" @click="closePort()">❌</p>
      <p class="mt-3 icon" :title="getTitleIconUpdate" @click="loadWifiList()">🔁</p>
    </div>
  </div>
  <select class="form-select mb-2" v-model="globalStore.wifiSelected" @change="selectWifi()">
    <option v-for="wifi in wifiList" :key="wifi.ip" :value="wifi">{{ wifi.ip }} ({{ wifi.mac }})</option>
  </select>
  <div class="ms-auto d-flex gap-2">
    <button
      type="button"
      class="btn btn-primary btn-sm ms-auto buttonColorBlue button"
      :disabled="globalStore.wifiSelected?.ip === ''"
      @click="selectWifi()"
    >
      {{ $t("home.wifi.button") }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useGlobalStore } from "../stores/useGlobalStore";
import GlobalService from "../services/global.service";
import { useI18n } from "vue-i18n";

const wifiList = ref<{ ip: string; mac: string; hostname: string }[]>([]);
const globalStore = useGlobalStore();
const { t } = useI18n();

onMounted(() => {
  loadWifiList().then(() => {
    globalStore.setWifiSelected(GlobalService.getStorage("config.wifiSelected"));
    // if (serialPorts.value.includes(globalStore.arduinoPort)) selectWifi();
  });
});

const loadWifiList = async () => {
  try {
    wifiList.value = await window.socket.scanNetwork();
  } catch (error) {
    console.error("Erro ao carregar as portas seriais:", error);
  }
};
const selectWifi = async () => {
  try {
    window.socket.openSocketConnection(globalStore.wifiSelected.ip);
    globalStore.setWifiSelected(globalStore.wifiSelected);
    // window.serial.writeSerial("arduino.setup");
    GlobalService.setStorage("config.wifiSelected", globalStore.wifiSelected);
  } catch (error) {
    console.error("Erro ao abrir a porta serial:", error);
  }
};

const closePort = async () => {
  try {
    if (globalStore.wifiSelected.ip !== "") {
      window.socket.closeSocketConnection();
      globalStore.wifiSelected = { ip: "", mac: "", hostname: "" };
      globalStore.setProcessItsRunning(false);
    }
  } catch (error) {
    console.error("Erro ao fechar a porta serial:", error);
  }
};

const getTitleIconClose = computed(() => {
  return t("home.wifi.icons.close");
});
const getTitleIconUpdate = computed(() => {
  return t("home.wifi.icons.update");
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
