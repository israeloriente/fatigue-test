export {};

declare global {
  interface Window {
    electron: {
      removeAllListeners: (event: string) => void;
    };
    socket: {
      // writeSerial: (value: string) => void;
      // getSerialPorts: () => Promise<string[]>;
      // openSerialPort: (port: string) => promise<string>;
      // onSerialData: (callback: (data: string) => void) => void;
      // onSerialLog: (callback: (data: string) => void) => void;
      // onSerialError: (callback: (error: string) => void) => void;
      // closeSerialPort: () => void;

      // new
      scanNetwork: () => Promise<{ ip: string; mac: string; hostname: string }[]>;
      openSocketConnection: (ip: string) => Promise<void>;
      closeSocketConnection: () => void;
      onSocketData: (callback: (data: string) => void) => void;
      writeSocket: (data: any) => void;
    };
  }
}
