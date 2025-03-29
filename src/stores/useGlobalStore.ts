import { defineStore } from "pinia";
import { i18n } from "../main";
import type { Log } from "../interfaces/log.interface";

export const useGlobalStore = defineStore("global", {
  state: () => ({
    wifiSelected: { ip: "", mac: "", hostname: "" },
    countOfTurns: 0,
    motorLapTurnOn: false,
    motorWeightTurnOn: false,
    directionRotation: false,
    scaleStatus: false,
    weight: 0,
    logs: "",
    loadingStatus: {
      weight: false,
      lap: false,
    },
    projectIsRunning: false,
    currentLanguage: "en",
  }),

  getters: {
    // doubledCount: (state) => state.weight * 2,
  },
  actions: {
    setCountOfTurns(value: number) {
      this.countOfTurns = value;
    },
    setWeight(value: number) {
      this.weight = Math.abs(value);
    },
    setMotorLapTurnOn(value: boolean) {
      this.motorLapTurnOn = value;
    },
    setMotorWeightTurnOn(value: boolean) {
      this.motorWeightTurnOn = value;
    },
    setWifiSelected(value: { ip: string; mac: string; hostname: string }) {
      this.wifiSelected = value;
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
    setProjectIsRunning(value: boolean) {
      this.projectIsRunning = value;
    },
    setDirectionRotation(value: boolean) {
      this.directionRotation = value;
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
