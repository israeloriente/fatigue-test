const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electron", {
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),
});

contextBridge.exposeInMainWorld("socket", {
  // getSerialPorts: () => ipcRenderer.invoke("get-serial-ports"),
  scanNetwork: () => ipcRenderer.invoke("scan-network"),
  openSocketConnection: (ip) => ipcRenderer.invoke("open-socket-connection", ip),
  closeSocketConnection: () => ipcRenderer.send("close-socket-connection"),
  onSocketData: (callback) => ipcRenderer.on("socket-data", (event, data) => callback(data)),
  writeSocket: (data) => ipcRenderer.send("write-socket", data),

  // openSerialPort: (portPath) => ipcRenderer.invoke('open-serial-port', portPath),
  // onSerialData: (callback) => ipcRenderer.on("serial-data", (event, data) => callback(data)),
  // onSerialLog: (callback) => ipcRenderer.on("serial-log", (event, data) => callback(data)),
  // onSerialError: (callback) => ipcRenderer.on("serial-error", (event, error) => callback(error)),
  // closeSerialPort: () => ipcRenderer.send("close-serial-port"),
});
