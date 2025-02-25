import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import arp from "node-arp";
import net from "net";
import os from "os";
import dns from "dns";

let mainWindow;
let client;
let raspberryIP;
let buffer = "";

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

ipcMain.handle("scan-network", async () => {
  const ipBase = getBaseIp();
  if (!ipBase) {
    console.error("Não foi possível obter o IP base da rede.");
    return [];
  }
  const scanPromises = [];
  const macRegex = /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/;
  for (let i = 1; i < 255; i++) {
    const ip = `${ipBase}.${i}`;
    const promise = new Promise((resolve) => {
      arp.getMAC(ip, (err, mac) => {
        if (!err && mac && macRegex.test(mac)) {
          // Obtém o hostname usando DNS reverse lookup
          dns.reverse(ip, (err, hostnames) => {
            const hostname = !err && hostnames.length > 0 ? hostnames[0] : null;
            resolve({ ip, mac, hostname });
          });
        } else {
          resolve(null);
        }
      });
    });
    scanPromises.push(promise);
  }
  const results = await Promise.all(scanPromises);
  const devices = results.filter((device) => device !== null);
  return devices;
});

// ipcMain.handle("get-serial-ports", async () => {
//   try {
//     const ports = await SerialPort.list();
//     return ports.map((port) => port.path);
//   } catch (error) {
//     mainWindow.webContents.send("serial-error", "global.errorListingSerialPorts");
//     return [];
//   }
// });

ipcMain.on("write-socket", (event, value) => {
  const message = JSON.stringify(value);
  client.write(message + "\n");
});

ipcMain.handle("open-socket-connection", (event, selectedIP) => {
  if (client) client.destroy();
  raspberryIP = selectedIP;
  client = new net.Socket();
  client.connect(8080, raspberryIP, () => {
    console.log("Conectado ao Raspberry Pi");
    mainWindow.webContents.send("socket-status", "Conectado");
  });
  client.on("data", (data) => {
    buffer += data.toString();
    const messages = buffer.split("\n");
    for (let i = 0; i < messages.length - 1; i++) {
      const message = messages[i].trim();
      if (message) {
        try {
          const jsonData = JSON.parse(message);
          console.log("JSON Recebido:", jsonData);
          mainWindow.webContents.send("socket-data", jsonData);
        } catch (err) {
          console.error("Erro ao parsear JSON:", err, "Mensagem:", message);
        }
      }
    }
    buffer = messages[messages.length - 1];
  });
  client.on("error", (err) => {
    console.error("Erro na conexão:", err);
    mainWindow.webContents.send("socket-error", err.message);
  });
  client.on("close", () => {
    console.log("Conexão encerrada.");
    mainWindow.webContents.send("socket-status", "Desconectado");
  });
  return true;
});

// ipcMain.handle("open-serial-port", (event, portPath) => {
//   if (port) {
//     port.close(); // Fechar a porta anterior se já estiver aberta
//   }

//   port = new SerialPort({ path: portPath, baudRate: 9600 });
//   let bufferJson = "";
//   let buffer = "";
//   port.on("data", (data) => {
//     bufferJson += data.toString();
//     if (bufferJson.includes("#")) {
//       try {
//         const message = bufferJson.split("$")[1].split("#")[0];
//         const parsedData = JSON.parse(message);
//         mainWindow.webContents.send("serial-data", parsedData);
//       } catch (error) {}
//       bufferJson = "";
//     }
//   });
//   port.on("data", (data) => {
//     buffer += data.toString();
//     if (buffer.includes("%")) {
//       try {
//         const message = buffer.split("&")[1].split("%")[0];
//         const parsedData = JSON.parse(message);
//         mainWindow.webContents.send("serial-log", parsedData);
//       } catch (error) {}
//       buffer = "";
//     }
//   });
//   port.on("error", (err) => {
//     mainWindow.webContents.send("serial-error", err.message);
//     mainWindow.webContents.send("serial-log", { type: "info", message: "global.restarting" });
//     mainWindow.webContents.send("write-serial", "arduino.setup");
//   });
//   return true;
// });

ipcMain.on("close-socket-connection", () => {
  if (client) {
    client.destroy();
    mainWindow.webContents.send("socket-status", "Desconectado");
  }
});

// ipcMain.on("close-serial-port", (event, value) => {
//   port.close();
// });

function getBaseIp() {
  const interfaces = os.networkInterfaces();
  for (const interfaceName in interfaces) {
    for (const netInfo of interfaces[interfaceName]) {
      if (netInfo.family === "IPv4" && !netInfo.internal) {
        return netInfo.address.split(".").slice(0, 3).join(".");
      }
    }
  }
  return null;
}

app.on("window-all-closed", () => {
  app.quit();
});
