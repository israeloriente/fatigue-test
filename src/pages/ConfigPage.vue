<template>
  <ul class="list-group" style="padding: 3%">
    <li class="item list-group-item d-flex justify-content-between align-items-center">
      <p class="label">{{ $t("config.languageTitle") }}</p>
      <select class="form-select w-25" @change="changeLanguage($event)" :value="globalStore.currentLanguage">
        <option key="pt" value="pt">{{ $t("config.languagePortuguese") }}</option>
        <option key="en" value="en">{{ $t("config.languageEnglish") }}</option>
      </select>
    </li>
    <!-- <li class="item list-group-item d-flex justify-content-between align-items-center">
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
    </li> -->
  </ul>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Toggle from "../components/Toggle.vue";
import GlobalService from "../services/global.service";
import { useGlobalStore } from "../stores/useGlobalStore";
import { useI18n } from "vue-i18n";

const config = ref<any>({});
const { locale } = useI18n();
const globalStore = useGlobalStore();

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

const changeLanguage = (event: any) => {
  locale.value = event.target.value;
  globalStore.changeLanguage(event.target.value);
  GlobalService.setStorage("config.defaultLanguage", event.target.value);
};
</script>

<style scoped>
.label {
  margin: 0;
}
</style>
