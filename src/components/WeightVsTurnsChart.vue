<template>
  <canvas :id="id"></canvas>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import Chart from "chart.js/auto";
import { useGlobalStore } from "../stores/useGlobalStore";
import { useI18n } from "vue-i18n";

const globalStore = useGlobalStore();
const { t } = useI18n();

const id = "weightVsTurnsChart-" + Math.random().toString(36).substr(2, 9);

// Instância do gráfico
let chartInstance: Chart;

// Criando o gráfico no onMounted
onMounted(() => {
  const ctx = document.getElementById(id) as HTMLCanvasElement | null;
  if (ctx) {
    chartInstance = new Chart(ctx, {
      type: "line", // Tipo de gráfico (linha)
      data: {
        labels: [], // Contagem de voltas (exemplo)
        datasets: [
          {
            label: getLabelName.value,
            data: [], // Peso (kg) (exemplo)
            borderColor: "rgb(72, 163, 203)",
            backgroundColor: "rgb(72, 163, 203, 0.2)",
            fill: true,
            tension: 0.1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: getscalesX.value,
            },
          },
          y: {
            title: {
              display: true,
              text: getscalesY.value,
            },
          },
        },
      },
    });
  }
});

const resetChart = () => {
  chartInstance.data.datasets[0].data = [];
  chartInstance.data.labels = [];
  chartInstance.update();
};

const getLabelName = computed(() => {
  return t("home.chart.label");
});
const getscalesX = computed(() => {
  return t("home.chart.scalesX");
});
const getscalesY = computed(() => {
  return t("home.chart.scalesY");
});

watch(
  () => globalStore.tensaoFalha,
  (newValue) => {
    chartInstance.data.datasets[0].data.push(newValue);
    if (chartInstance.data.labels) chartInstance.data.labels.push(globalStore.countOfTurns);
    chartInstance.update();
  }
);

defineExpose({ resetChart });
</script>

<style scoped lang="scss"></style>
