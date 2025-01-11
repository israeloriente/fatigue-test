const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electron", {
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),
});

contextBridge.exposeInMainWorld("serial", {
  getSerialPorts: () => ipcRenderer.invoke("get-serial-ports"),
  writeSerial: (data) => ipcRenderer.send("write-serial", data),
  openSerialPort: (portPath) => ipcRenderer.invoke('open-serial-port', portPath),
  onSerialData: (callback) => ipcRenderer.on("serial-data", (event, data) => callback(data)),
  onSerialLog: (callback) => ipcRenderer.on("serial-log", (event, data) => callback(data)),
  onSerialError: (callback) => ipcRenderer.on("serial-error", (event, error) => callback(error)),
  closeSerialPort: () => ipcRenderer.send("close-serial-port"),
});
