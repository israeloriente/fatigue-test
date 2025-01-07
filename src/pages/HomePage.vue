<template>
  <div>
    <h1>Home Page</h1>
    <select v-model="selectedPort" @change="openPort()">
      <option v-for="port in serialPorts" :key="port" :value="port">
        {{ port }}
      </option>
    </select>

    <input type="number" v-model="initVal" v-on:change="changeSpeed()" />

    <br /><br />
    <Speedometer ref="speedometer" :userPref="{}"></Speedometer>

    <h1>Dados da Porta Serial</h1>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Number of Cycles</th>
            <th>Stress Strain</th>
            <th>Life</th>
            <th>Motor 1</th>
            <th>Motor 2</th>
            <th>Gyro Sensor</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ receivedData.Number_of_Cycles }}</td>
            <td>{{ receivedData.Stress_Strain }}</td>
            <td>{{ receivedData.Life }}</td>
            <td>{{ receivedData.Motor_Status ? "Running" : "Stoped" }}</td>
            <td>{{ receivedData.Motor2_Status ? "Running" : "Stoped" }}</td>
            <td>{{ receivedData.Gyro_Sensor_Status ? "Running" : "Stoped" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="toggle-container">
      <label class="switch">
        <input type="checkbox" v-model="motor1Toggle" @change="changeToggle('motor1', $event)" />
        <span class="slider"></span>
      </label>
      <p>{{ "Motor 1" }}</p>
    </div>
    <div class="toggle-container">
      <label class="switch">
        <input type="checkbox" v-model="motor2Toggle" @change="changeToggle('motor2', $event)" />
        <span class="slider"></span>
      </label>
      <p>{{ "Motor 2" }}</p>
    </div>
    <div class="toggle-container">
      <label class="switch">
        <input type="checkbox" v-model="gyroSensorToggle" @change="changeToggle('gyroSensor', $event)" />
        <span class="slider"></span>
      </label>
      <p>{{ "Gyro Sensor" }}</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import Speedometer from "../components/Speedometer.vue";

const serialPorts = ref<string[]>([]);
const selectedPort = ref<string>("");
const receivedData = ref<any>("");
const motor1Toggle = ref<boolean>(false);
const motor2Toggle = ref<boolean>(false);
const gyroSensorToggle = ref<boolean>(false);

const initVal = ref(30);
const speedometer = ref<InstanceType<typeof Speedometer>>(null);

onMounted(() => {
  loadSerialPorts();
  // Escutando dados recebidos da porta serial
  window.electron.on("serial-data", (data) => {
    receivedData.value = data;
  });

  // Escutando erros da porta serial
  window.electron.on("serial-error", (error) => {
    receivedData.value += `Erro: ${error}\n`;
  });
});

const changeSpeed = () => {
  speedometer.value.setPosition(initVal.value);
};

// Função para carregar as portas seriais
const loadSerialPorts = async () => {
  try {
    serialPorts.value = await window.serial.getSerialPorts();
  } catch (error) {
    console.error("Erro ao carregar as portas seriais:", error);
  }
};

const changeToggle = async (device: string, event: Event) => {
  const isChecked = (event.target as HTMLInputElement).checked;
  try {
    switch (device) {
      case "motor1":
        if (isChecked) {
          window.serial.writeSerial("1");
        } else {
          window.serial.writeSerial("2");
        }
        break;
      case "motor2":
        if (isChecked) {
          window.serial.writeSerial("3");
        } else {
          window.serial.writeSerial("4");
        }
        break;
      case "gyroSensor":
        if (isChecked) {
          window.serial.writeSerial("5");
        } else {
          window.serial.writeSerial("6");
        }
        break;
    }
  } catch (error) {
    console.error("Erro ao enviar dados para a porta serial:", error);
  }
};

// Função para abrir a porta serial
const openPort = async () => {
  if (!selectedPort.value) {
    alert("Por favor, selecione uma porta serial!");
    return;
  }

  try {
    const result = await window.serial.openSerialPort(selectedPort.value);
    console.log(result);
  } catch (error) {
    console.error("Erro ao abrir a porta serial:", error);
  }
};

const openWindow = () => {
  window.electron.openArduinoPage();
};
</script>

<style lang="scss">
body {
  font-family: Arial, sans-serif;
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;

  input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: 0.4s;
    border-radius: 34px;

    &::before {
      position: absolute;
      content: "";
      height: 26px;
      width: 26px;
      border-radius: 50%;
      left: 4px;
      bottom: 4px;
      background-color: white;
      transition: 0.4s;
    }
  }

  input:checked + .slider {
    background-color: #4caf50;
  }

  input:checked + .slider::before {
    transform: translateX(26px);
  }
}

.table-container {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 800px;
  margin: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #f1f1f1;
}

th {
  background-color: #4caf50;
  color: white;
}

tr:hover {
  background-color: #f1f1f1;
}

td {
  color: #555;
}
</style>
