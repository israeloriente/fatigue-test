#include "sensor-carga.h"
#include "utils.h"
#include <Thread.h>
#include <ThreadController.h>

float weight = 0.0;
bool scaleStatus = false;
bool motorWeightTurnOn = false;
bool motorLapTurnOn = false;
int countOfTurns = 0;
int pinMotorLap = 8;

SensorCarga sensorCarga;

ThreadController controller = ThreadController();
Thread sensorThread = Thread();
Thread controllerSerialThread = Thread();
Thread controllerSendJsonResponseThread = Thread();
Thread controllerGetWeightThread = Thread();

void setup()
{
  Serial.begin(9600);
  pinMode(pinMotorLap, OUTPUT);
  digitalWrite(pinMotorLap, HIGH);
  pinMode(10, INPUT);

  scaleStatus = sensorCarga.setup();

  // Configura as threads
  sensorThread.onRun(readSensor);
  sensorThread.setInterval(1);
  controllerSerialThread.onRun(listemSerial);
  controllerSerialThread.setInterval(166);
  controllerSendJsonResponseThread.onRun(sendJsonResponse);
  controllerSendJsonResponseThread.setInterval(166);
  controllerGetWeightThread.onRun(updateWeight);
  controllerGetWeightThread.setInterval(166);

  controller.add(&sensorThread);
  controller.add(&controllerSerialThread);
  controller.add(&controllerSendJsonResponseThread);
  controller.add(&controllerGetWeightThread);

  while (!Serial)
  {
  }

  log("success", "arduino.arduinoConnected");
}

void loop()
{
  controller.run(); // Executa as threads
}

void updateWeight()
{
  weight = sensorCarga.getWeight();
}

void readSensor()
{
  static bool wasHigh = false;

  if (digitalRead(10) == HIGH && !wasHigh)
  {
    wasHigh = true;
  }
  else if (digitalRead(10) == LOW && wasHigh)
  {
    wasHigh = false;
    countOfTurns++;
  }
}

void sendJsonResponse()
{
  // Formatar JSON
  String json = "{ \"weight\": " + String(weight, 1) +
                ", \"motorWeightTurnOn\": " + (motorWeightTurnOn ? "true" : "false") +
                ", \"motorLapTurnOn\": " + (motorLapTurnOn ? "true" : "false") +
                ", \"scaleStatus\": " + (scaleStatus ? "true" : "false") +
                ", \"countOfTurns\": " + String(countOfTurns) + "}";

  Serial.print("$");
  Serial.print(json);
  Serial.println("#");
}

void listemSerial()
{
  if (Serial.available())
  {
    String data = Serial.readString(); // Lê o valor enviado pela serial

    // Processa os comandos recebidos
    if (data == "arduino.setup")
    {
      setup();
    }
    else if (data == "project.start")
    {
      startProject();
    }
    else if (data == "project.stop")
    {
      stopProject();
    }
    else if (data == "motorLap.start")
    {
      turnOnMotorLap();
    }
    else if (data == "motorLap.stop")
    {
      turnOffMotorLap();
    }
    else if (data == "motorWeight.start")
    {
      turnOnMotorWeight();
    }
    else if (data == "motorWeight.stop")
    {
      turnOffMotorWeight();
    }
  }
}

void processCommand(String data)
{
  if (data == "arduino.setup")
    setup();
  else if (data == "project.start")
    startProject();
  else if (data == "project.stop")
    stopProject();
  else if (data == "motorLap.start")
    turnOnMotorLap();
  else if (data == "motorLap.stop")
    turnOffMotorLap();
  else if (data == "motorWeight.start")
    turnOnMotorWeight();
  else if (data == "motorWeight.stop")
    turnOffMotorWeight();
}
