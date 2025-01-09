import { defineStore } from "pinia";

export const useGlobalStore = defineStore("global", {
  state: () => ({
    arduinoPort: "",
    countOfTurns: 0,
    motorLapTurnOn: false,
    motorWeightTurnOn: false,
    scaleStatus: false,
    weight: 0,
    logs: "",
    loadingStatus: {
      weight: false,
      lap: false,
    },
  }),

  getters: {
    doubledCount: (state) => state.weight * 2,
  },
  actions: {
    setCountOfTurns(value: number) {
      this.countOfTurns = value;
    },
    setWeight(value: number) {
      this.weight = value;
    },
    setMotorLapTurnOn(value: boolean) {
      this.motorLapTurnOn = value;
    },
    setMotorWeightTurnOn(value: boolean) {
      this.motorWeightTurnOn = value;
    },
    setArduinoPort(value: string) {
      this.arduinoPort = value;
    },
    setLoadingStatus(value: boolean) {
      this.loadingStatus = {
        weight: value,
        lap: value,
      };
    },
    setLoadingStatusWeight(value: boolean) {
      this.loadingStatus.weight = value;
    },
    setLoadingStatusTurns(value: boolean) {
      this.loadingStatus.lap = value;
    },
    setScaleStatus(value: boolean) {
      this.scaleStatus = value;
    },
    resetAll() {
      this.weight = 0;
      this.countOfTurns = 0;
      this.logs = "";
    },
    addLog(message: string) {
      const timestamp = new Date().toLocaleTimeString();
      this.logs += `[${timestamp}] ${message}\n`;
    },
    cleanLogs() {
      this.logs = "";
    },
  },
});
