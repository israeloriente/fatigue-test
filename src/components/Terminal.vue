<template>
  <div class="terminal">
    <div class="fakeMenu">
      <div class="fakeButtons fakeClose" @click="clearLogs()"></div>
      <div class="fakeButtons fakeMinimize"></div>
      <div class="fakeButtons fakeZoom"></div>
    </div>
    <div class="fakeScreen">
      <textarea v-model="logs" ref="logTerminal" readonly name="" id=""></textarea>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from "vue";
import { useGlobalStore } from "../stores/useGlobalStore";

const logs = ref<string>("");
const logTerminal = ref<HTMLTextAreaElement | null>(null);
const globalStore = useGlobalStore();

const clearLogs = () => {
  globalStore.cleanLogs();
};

watch(
  () => globalStore.logs,
  (newLogs) => {
    logs.value = newLogs;
    nextTick(() => {
      const terminal = logTerminal.value;
      if (terminal) terminal.scrollTop = terminal.scrollHeight;
    });
  }
);
</script>

<style scoped lang="scss">
.terminal {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 1%;
}

.fakeButtons {
  height: 10px;
  width: 10px;
  border-radius: 50%;
  border: 1px solid #000;
  position: relative;
  top: 0px;
  left: 6px;
  background-color: #ff3b47;
  border-color: #9d252b;
  display: inline-block;
}

.fakeMinimize {
  left: 11px;
  background-color: #ffc100;
  border-color: #9d802c;
}

.fakeZoom {
  left: 16px;
  background-color: #00d742;
  border-color: #049931;
}

.fakeMenu {
  width: 100%;
  box-sizing: border-box;
  height: 25px;
  background-color: #bbb;
  margin: 0 auto;
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
}

.fakeScreen {
  background-color: #151515;
  box-sizing: border-box;
  width: 100%;
  height: 80%;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;

  textarea {
    background-color: transparent;
    height: 100%;
    width: 100%;
    color: #e3e3e3;
    font-size: 10px;
  }
}

.line1 {
  color: #9cd9f0;
  -webkit-animation: type 0.5s 1s steps(20, end) forwards;
  -moz-animation: type 0.5s 1s steps(20, end) forwards;
  -o-animation: type 0.5s 1s steps(20, end) forwards;
  animation: type 0.5s 1s steps(20, end) forwards;
}

.cursor1 {
  -webkit-animation: blink 1s 2s 2 forwards;
  -moz-animation: blink 1s 2s 2 forwards;
  -o-animation: blink 1s 2s 2 forwards;
  animation: blink 1s 2s 2 forwards;
}

.line2 {
  color: #cdee69;
  -webkit-animation: type 0.5s 4.25s steps(20, end) forwards;
  -moz-animation: type 0.5s 4.25s steps(20, end) forwards;
  -o-animation: type 0.5s 4.25s steps(20, end) forwards;
  animation: type 0.5s 4.25s steps(20, end) forwards;
}

.cursor2 {
  -webkit-animation: blink 1s 5.25s 2 forwards;
  -moz-animation: blink 1s 5.25s 2 forwards;
  -o-animation: blink 1s 5.25s 2 forwards;
  animation: blink 1s 5.25s 2 forwards;
}

.line3 {
  color: #e09690;
  -webkit-animation: type 0.5s 7.5s steps(20, end) forwards;
  -moz-animation: type 0.5s 7.5s steps(20, end) forwards;
  -o-animation: type 0.5s 7.5s steps(20, end) forwards;
  animation: type 0.5s 7.5s steps(20, end) forwards;
}

.cursor3 {
  -webkit-animation: blink 1s 8.5s 2 forwards;
  -moz-animation: blink 1s 8.5s 2 forwards;
  -o-animation: blink 1s 8.5s 2 forwards;
  animation: blink 1s 8.5s 2 forwards;
}

.line4 {
  color: #fff;
  -webkit-animation: type 0.5s 10.75s steps(20, end) forwards;
  -moz-animation: type 0.5s 10.75s steps(20, end) forwards;
  -o-animation: type 0.5s 10.75s steps(20, end) forwards;
  animation: type 0.5s 10.75s steps(20, end) forwards;
}

.cursor4 {
  -webkit-animation: blink 1s 11.5s infinite;
  -moz-animation: blink 1s 8.5s infinite;
  -o-animation: blink 1s 8.5s infinite;
  animation: blink 1s 8.5s infinite;
}

@-webkit-keyframes blink {
  0% {
    opacity: 0;
  }
  40% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-moz-keyframes blink {
  0% {
    opacity: 0;
  }
  40% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-o-keyframes blink {
  0% {
    opacity: 0;
  }
  40% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@keyframes blink {
  0% {
    opacity: 0;
  }
  40% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-webkit-keyframes type {
  to {
    width: 17em;
  }
}

@-moz-keyframes type {
  to {
    width: 17em;
  }
}

@-o-keyframes type {
  to {
    width: 17em;
  }
}

@keyframes type {
  to {
    width: 17em;
  }
}
</style>
