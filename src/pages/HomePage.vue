<template>
  <div class="content">
    <div class="menu">
      <SerialPort />
      <InputData />
      <div class="list-group-item d-flex justify-content-between align-items-center">
        <div class="ms-auto d-flex gap-2">
          <button
            v-if="globalStore.processItsRunning"
            type="button"
            class="btn btn-danger btn-sm ms-auto button"
            @click="abort()"
          >
            Abortar
          </button>
          <button
            v-if="!globalStore.processItsRunning"
            type="button"
            class="btn btn-primary btn-sm ms-auto buttonColorBlue button"
            @click="start()"
            :disabled="globalStore.arduinoPort === ''"
          >
            Iniciar
          </button>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <Controls />
        </div>
        <div class="col">
          <Status />
        </div>
      </div>
    </div>
    <Results />
    <div class="chart">
      <WeightVsTurnsChart ref="weightVsTurnsChart" />
    </div>
    <Terminal class="terminal" />
    <Speedometer class="ondometer" :userPref="{}"></Speedometer>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, ref } from "vue";
import Speedometer from "../components/Speedometer.vue";
import Terminal from "../components/Terminal.vue";
import Controls from "../components/Controls.vue";
import Status from "../components/Status.vue";
import WeightVsTurnsChart from "../components/WeightVsTurnsChart.vue";
import SerialPort from "../components/SerialPort.vue";
import { useGlobalStore } from "../stores/useGlobalStore";
import InputData from "../components/InputData.vue";
import Results from "../components/Results.vue";

const globalStore = useGlobalStore();
const weightVsTurnsChart = ref<typeof WeightVsTurnsChart | null>(null);
let serialDataHandler: ((data: any) => void) | null = null;
let serialErrorHandler: ((data: any) => void) | null = null;
let serialLogHandler: ((data: any) => void) | null = null;

onMounted(() => {
  globalStore.setProcessItsRunning(globalStore.motorWeightTurnOn || globalStore.motorLapTurnOn);
  setupSerialHandlers();
});

const start = async () => {
  window.serial.writeSerial("project.start");
  globalStore.setProcessItsRunning(true);
  globalStore.setLoadingStatusWeight(true);
  setTimeout(() => {
    if (!globalStore.motorWeightTurnOn) globalStore.setProcessItsRunning(false);
    globalStore.setLoadingStatusWeight(false);
  }, 2000);
};

const abort = async () => {
  window.serial.writeSerial("project.stop");
  weightVsTurnsChart.value?.resetChart();
  globalStore.setProcessItsRunning(false);
  globalStore.resetAll();
  globalStore.setLoadingStatus(true);
  setTimeout(() => {
    if (globalStore.motorWeightTurnOn) globalStore.setProcessItsRunning(true);
    globalStore.setLoadingStatus(false);
  }, 2000);
};

const setupSerialHandlers = () => {
  serialDataHandler = (data: any) => {
    globalStore.setWeight(data.weight);
    globalStore.setCountOfTurns(data.countOfTurns);
    globalStore.setMotorLapTurnOn(data.motorLapTurnOn);
    globalStore.setMotorWeightTurnOn(data.motorWeightTurnOn);
    globalStore.setScaleStatus(data.scaleStatus);
  };
  serialLogHandler = (data: any) => {
    globalStore.addLog(data);
  };
  serialErrorHandler = (data: any) => {
    globalStore.addLog({ type: "error", message: JSON.stringify(data) });
  };
  window.serial.onSerialData(serialDataHandler);
  window.serial.onSerialLog(serialLogHandler);
  window.serial.onSerialError(serialErrorHandler);
};

onUnmounted(() => {
  if (serialDataHandler) {
    window.electron.removeAllListeners("serial-data");
    serialDataHandler = null;
  }
  if (serialErrorHandler) {
    window.electron.removeAllListeners("serial-error");
    serialErrorHandler = null;
  }
});
</script>

<style lang="scss" scoped>
.content {
  .menu {
    margin: 20px;
    width: 520px;
    height: 450px;
    padding: 10px;
    border-radius: 10px;
    background-color: #f1f1f1;

    .buttonColorBlue {
      background-color: rgb(72, 163, 203);
      border-color: rgb(72, 163, 203);
    }
    .buttonColorBlue:hover {
      background-color: rgb(51, 155, 200);
    }
    .button {
      height: 31px;
      width: 80px;
    }
  }
  .chart {
    position: absolute;
    top: 300px;
    left: 550px;
    width: 430px;
  }
  .terminal {
    left: 10px;
    width: 750px;
    height: 250px;
  }
  .ondometer {
    position: absolute;
    top: 555px;
    left: 790px;
  }
}
</style>
