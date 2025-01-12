import { defineStore } from "pinia";
import { i18n } from "../main";
import type { Log } from "../interfaces/log.interface";

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
    processItsRunning: false,
    currentLanguage: "en",
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
    setProcessItsRunning(value: boolean) {
      this.processItsRunning = value;
    },
    changeLanguage(language: "en" | "pt") {
      this.currentLanguage = language;
    },
    resetAll() {
      this.weight = 0;
      this.countOfTurns = 0;
    },
    addLog(log: Log) {
      const timestamp = new Date().toLocaleTimeString();
      const t = i18n.global.t;
      const msg = log.message.includes(".") ? t(log.message) : log.message;
      this.logs += `[${timestamp}] <span class="${log.type}"> ${msg} </span>\n`;
    },
    cleanLogs() {
      this.logs = "";
    },
  },
});
