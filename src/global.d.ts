export {};

declare global {
  interface Window {
    electron: {
      removeAllListeners: (event: string) => void;
    };
    serial: {
      writeSerial: (value: string) => void;
      getSerialPorts: () => Promise<string[]>;
      openSerialPort: (port: string) => promise<string>;
      onSerialData: (callback: (data: string) => void) => void;
      onSerialLog: (callback: (data: string) => void) => void;
      onSerialError: (callback: (error: string) => void) => void;
      closeSerialPort: () => void;
    };
  }
}
