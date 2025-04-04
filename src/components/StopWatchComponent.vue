<template>
  <div>{{ timerDisplay }}</div>
</template>

<script setup lang="ts">
import { onUnmounted, ref } from "vue";
import moment from "moment";

const timerDisplay = ref("00:00:00");
const duration = ref<moment.Moment>(moment("00:00:00", "HH:mm:ss"));
const currentTime = ref<moment.Moment>(moment("00:00:00", "HH:mm:ss"));
const startDate = ref<any>();
const endDate = ref<any>();
const timer = ref<any>(null);

onUnmounted(() => {
  stopCount();
});

const init = (start: Date, end: Date, isRunning: boolean): void => {
  startDate.value = start;
  endDate.value = end;
  if (start) {
    const startDuration = moment(start);
    const endTime = end == undefined ? moment() : moment(end);
    const diffMilliseconds = endTime.diff(startDuration);
    const diffTime = moment.utc(diffMilliseconds);
    const formattedDiff = diffTime.format("HH:mm:ss");
    if (isRunning) {
      timeCount(formattedDiff);
    } else {
      duration.value = moment(start);
      currentTime.value = moment(end);
      timerDisplay.value = moment.utc(currentTime.value.diff(startDuration)).format("HH:mm:ss");
    }
  }
};
const timeCount = (startInput: string): void => {
  if (timerDisplay.value !== "00:00:00") {
    duration.value = moment(timerDisplay.value, "HH:mm:ss");
  } else {
    duration.value = moment(startInput, "HH:mm:ss");
  }
  timer.value = setInterval(() => countUp(), 1000);
  timerDisplay.value = duration.value.format("HH:mm:ss");
};
const countUp = (): void => {
  const endDateLocal = endDate.value == undefined ? moment() : moment(endDate.value);
  const startDateLocal = moment(startDate.value);
  timerDisplay.value = moment.utc(endDateLocal.diff(startDateLocal)).format("HH:mm:ss");
};
const stopCount = (): void => {
  if (timer.value) {
    clearInterval(timer.value);
    timer.value = null;
  }
};

defineExpose({ init, stopCount, timerDisplay });
</script>

<style scoped lang="scss">
.content {
  width: 100%;
  height: 15vh;
  margin: 5%;
  .title {
    font-size: 3rem;
    font-weight: bold;
    color: #1e1d1d;
  }
}
</style>
