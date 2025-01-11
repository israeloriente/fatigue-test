<template>
  <ul class="list-group" style="padding: 3%">
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ `Valor padrão para "sut do corpo de prova"` }}</p>
      <input
        type="text"
        class="form-control w-25"
        placeholder="150"
        aria-describedby="basic-addon1"
        v-on:focusout="saveSutCorpoOnStorage"
        v-model="config.sutCorpo"
      />
    </li>
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ `Valor padrão para "Carga Aplicada"` }}</p>
      <input
        type="text"
        class="form-control w-25"
        placeholder="150"
        aria-describedby="basic-addon1"
        v-on:focusout="saveCargaAplicadaOnStorage"
        v-model="config.cargaAplicada"
      />
    </li>
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ "Sentido da rotação (Horário)" }}</p>
      <Toggle />
    </li>
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ "Sensor de carga" }}</p>
      <Toggle />
    </li>
  </ul>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Toggle from "../components/Toggle.vue";
import GlobalService from "../services/global.service";

const config = ref<any>({});

onMounted(() => {
  const { defaultSutCorpo, defaultCargaAplicada } = GlobalService.getStorage("config");
  config.value.sutCorpo = defaultSutCorpo;
  config.value.cargaAplicada = defaultCargaAplicada;
});

const saveSutCorpoOnStorage = (ev: any) => {
  GlobalService.setStorage("config.defaultSutCorpo", ev.target.value);
};
const saveCargaAplicadaOnStorage = (ev: any) => {
  GlobalService.setStorage("config.defaultCargaAplicada", ev.target.value);
};
</script>

<style scoped>
.label {
  margin: 0;
}
</style>
