<template>
  <p class="title">Dados de entrada</p>
  <div class="input-group mb-3">
    <span class="input-group-text" id="basic-addon1">Sut do corpo de prova (MPa)</span>
    <input
      type="text"
      class="form-control"
      v-model="sutCorpo"
      placeholder="150"
      aria-label="Username"
      aria-describedby="basic-addon1"
      v-on:focusout="saveSutCorpoOnStorage"
    />
  </div>
  <div class="input-group mb-3">
    <span class="input-group-text" id="basic-addon1">Carga aplicada (MPa)</span>
    <input
      type="text"
      class="form-control"
      v-model="cargaAplicada"
      placeholder="150"
      aria-label="Username"
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
  const { defaultSutCorpo, defaultCargaAplicada } = GlobalService.getStorage("config");
  sutCorpo.value = defaultSutCorpo;
  cargaAplicada.value = defaultCargaAplicada;
});
</script>

<style scoped lang="scss"></style>
