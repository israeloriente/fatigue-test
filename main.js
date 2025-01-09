import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import { SerialPort } from "serialport";

let mainWindow;
let port;

app.on("ready", () => {
  mainWindow = new BrowserWindow({
    width: 1000,
    // maxWidth: 1000,
    // minWidth: 1000,
    // maxHeight: 800,
    // minHeight: 800,
    height: 800,
    webPreferences: {
      preload: path.join(path.resolve(), "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  mainWindow.loadURL("http://localhost:5173");
});

ipcMain.handle("get-serial-ports", async () => {
  try {
    const ports = await SerialPort.list();
    return ports.map((port) => port.path);
  } catch (error) {
    console.error("Erro ao listar as portas seriais:", error);
    return [];
  }
});

ipcMain.on("write-serial", (event, value) => {
  port.write(value);
});

ipcMain.handle("open-serial-port", (event, portPath) => {
  if (port) {
    port.close(); // Fechar a porta anterior se já estiver aberta
  }

  port = new SerialPort({ path: portPath, baudRate: 9600 });
  let buffer = "";
  port.on("data", (data) => {
    buffer += data.toString();
    if (buffer.includes("#")) {
      const message = buffer.split("$")[1].split("#")[0];
      try {
        const parsedData = JSON.parse(message);
        mainWindow.webContents.send("serial-data", parsedData);
      } catch (error) {
        console.error("Erro ao processar JSON:", error);
        mainWindow.webContents.send("serial-error", error);
      }
      buffer = "";
    }
  });
  port.on("error", (err) => {
    console.error("Erro na porta serial:", err);
    mainWindow.webContents.send("serial-error", err.message);
  });
  return "Porta serial selecionada com sucesso";
});

ipcMain.on("close-serial-port", (event, value) => {
  port.close();
});

app.on("window-all-closed", () => {
  app.quit();
});
