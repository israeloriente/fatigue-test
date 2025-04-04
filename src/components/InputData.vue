<template>
  <p class="title">{{ $t("home.inputData.title") }}</p>
  <div class="input-group mb-2">
    <span class="input-group-text" id="basic-addon1">{{ $t("home.inputData.inputSut") }}</span>
    <input
      type="text"
      class="form-control"
      v-model="sutCorpo"
      placeholder="280"
      aria-describedby="basic-addon1"
      v-on:focusout="saveSutCorpoOnStorage"
    />
  </div>
  <div class="input-group mb-2">
    <span class="input-group-text" id="basic-addon1">{{ $t("home.inputData.inputLoad") }}</span>
    <input
      type="text"
      class="form-control"
      v-model="cargaAplicada"
      placeholder="10"
      aria-describedby="basic-addon1"
      v-on:focusout="saveCargaAplicadaOnStorage"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import GlobalService from "../services/global.service";
import { useGlobalStore } from "../stores/useGlobalStore";

const globalStore = useGlobalStore();

const sutCorpo = ref<string>("");
const cargaAplicada = ref<string>("");

const saveSutCorpoOnStorage = (ev: any) => {
  GlobalService.setStorage("config.defaultSutCorpo", ev.target.value);
};

const saveCargaAplicadaOnStorage = (ev: any) => {
  if (ev.target.value === "") return;
  const value = parseFloat(ev.target.value);
  if (value > 40) {
    GlobalService.simpleAlert("simpleAlert.maxWeight");
    return;
  }
  window.socket.writeSocket({ maxWeight: value });
  setTimeout(() => {
    if (globalStore.maxWeight !== value) {
      GlobalService.simpleAlert("simpleAlert.raspberryNotConnected");
    } else GlobalService.setStorage("config.defaultCargaAplicada", ev.target.value);
  }, 1000);
};

onMounted(() => {
  const { defaultSutCorpo, defaultCargaAplicada } = GlobalService.getStorage("config") || {};
  sutCorpo.value = defaultSutCorpo || "";
  cargaAplicada.value = defaultCargaAplicada || "";
});
</script>

<style scoped lang="scss"></style>
