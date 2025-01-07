const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electron", {
  openArduinoPage: () => ipcRenderer.send("open-arduino-page"),
  on: (channel, callback) => ipcRenderer.on(channel, (event, data) => callback(data)),
});

contextBridge.exposeInMainWorld("serial", {
  writeSerial: (value) => ipcRenderer.send("write-serial", value),
  getSerialPorts: () => ipcRenderer.invoke("get-serial-ports"),
  openSerialPort: (portPath) => ipcRenderer.invoke('open-serial-port', portPath),
});
