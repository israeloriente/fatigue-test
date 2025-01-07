export {};

declare global {
  interface Window {
    electron: {
      openArduinoPage: () => void;
      on(event: string, callback: (val) => void): void;
    };
    serial: {
      writeSerial: (value: string) => void;
      getSerialPorts: () => Promise<string[]>;
      openSerialPort: (port: string) => promise<string>;
    }
  }
}
