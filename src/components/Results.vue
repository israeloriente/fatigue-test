<template>
  <div class="result">
    <p class="title text-center">Resultados</p>
    <ul class="list-group">
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">Vida teórica</span>
        <span>0</span>
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">Duração do ensaio</span>
        <span>0</span>
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">Vida</span>
        <span>0</span>
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">Erro</span>
        <span>0</span>
      </li>
      <li class="item list-group-item d-flex justify-content-between align-items-center">
        <span class="label">Contagem de voltas</span>
        <span>{{ globalStore.countOfTurns }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useGlobalStore } from "../stores/useGlobalStore";

const globalStore = useGlobalStore();

</script>

<style scoped lang="scss">
.result {
  position: absolute;
  top: 50.5px;
  left: 555px;
  width: 420px;
  height: 230px;
  padding: 10px;
  border-radius: 10px;
  background-color: #f1f1f1;

  .item {
    padding: 4.5px 7px;
  }
  .label {
    margin: 0;
    font-size: 15px;
  }
}
</style>
