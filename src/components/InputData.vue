<template>
  <p class="title">{{ $t("home.inputData.title") }}</p>
  <div class="input-group mb-2">
    <span class="input-group-text" id="basic-addon1">{{ $t("home.inputData.inputSut") }}</span>
    <input
      type="text"
      class="form-control"
      v-model="sutCorpo"
      placeholder="150"
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
      placeholder="150"
      aria-describedby="basic-addon1"
      v-on:focusout="saveCargaAplicadaOnStorage"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import GlobalService from "../services/global.service";

const sutCorpo = ref<string>("");
const cargaAplicada = ref<string>("");

const saveSutCorpoOnStorage = (ev: any) => {
  GlobalService.setStorage("config.defaultSutCorpo", ev.target.value);
};

const saveCargaAplicadaOnStorage = (ev: any) => {
  GlobalService.setStorage("config.defaultCargaAplicada", ev.target.value);
};

onMounted(() => {
  const { defaultSutCorpo, defaultCargaAplicada } = GlobalService.getStorage("config") || {};
  sutCorpo.value = defaultSutCorpo || "";
  cargaAplicada.value = defaultCargaAplicada || "";
});
</script>

<style scoped lang="scss"></style>
