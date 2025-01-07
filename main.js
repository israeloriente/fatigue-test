import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import { SerialPort } from "serialport";

let mainWindow;
let port;

ipcMain.handle("get-serial-ports", async () => {
  try {
    const ports = await SerialPort.list();
    return ports.map((port) => port.path);
  } catch (error) {
    console.error("Erro ao listar as portas seriais:", error);
    return [];
  }
});

app.on("ready", () => {
  mainWindow = new BrowserWindow({
    width: 800,
    // maxWidth: 800,
    // minWidth: 800,
    // maxHeight: 600,
    // minHeight: 600,
    height: 600,
    webPreferences: {
      preload: path.join(path.resolve(), "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  mainWindow.loadURL("http://localhost:5173");
});

ipcMain.handle("open-serial-port", (event, portPath) => {
  if (port) {
    port.close(); // Fechar a porta anterior se já estiver aberta
  }
  // Criar a nova instância do SerialPort
  port = new SerialPort({ path: portPath, baudRate: 115200 });
  // Tratar eventos do SerialPort, como leitura de dados
  let buffer = "";
  port.on("data", (data) => {
    buffer += data.toString();
    // Verifique se a mensagem está completa
    if (buffer.includes("#")) {
      const message = buffer.split("$")[1].split("#")[0]; // Extrai o conteúdo entre os delimitadores
      try {
        const parsedData = JSON.parse(message);
        mainWindow.webContents.send("serial-data", parsedData);
      } catch (error) {
        console.error("Erro ao processar JSON:", error);
      }
      buffer = "";
    }
  });
  // Tratar erros do SerialPort
  port.on("error", (err) => {
    console.error("Erro na porta serial:", err);
    mainWindow.webContents.send("serial-error", err.message); // Enviar erro para o frontend
  });
  return "Porta serial aberta com sucesso";
});

ipcMain.on("write-serial", (event, value) => {
  port.write(value, (err) => {
    if (err) console.error("Erro ao escrever na porta:", err.message);
  });
});

// ipcMain.on("open-arduino-page", () => {
//   if (!arduinoWindow) {
//     arduinoWindow = new BrowserWindow({
//       width: 400,
//       height: 300,
//       webPreferences: {
//         preload: path.join(__dirname, "preload.js"),
//         contextIsolation: true,
//         nodeIntegration: false,
//       },
//     });

//     arduinoWindow.loadURL("http://localhost:5173/arduino");

//     arduinoWindow.on("closed", () => {
//       arduinoWindow = null;
//     });
//   }
// });

// port1.on("data", (data) => {
//   mainWindow.webContents.send("data", data.toString());
// });
// port2.on("data", (data) => {
//   arduinoWindow.webContents.send("data", data.toString());
// });

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
