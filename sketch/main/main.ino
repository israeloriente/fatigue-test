#include "sensor-carga.h"
#include "motor-passo.h"
#include "utils.h"
#include <Arduino_FreeRTOS.h>

float weight = 0.0;
bool scaleStatus = false;
bool motorWeightTurnOn = false;
bool motorLapTurnOn = false;
int countOfTurns = 0;
int pinMotorLap = 8;

SensorCarga sensorCarga;
MotorPasso motorPasso;

// Prototipação das tarefas
void TaskReadSensor(void *pvParameters);
void TaskListenSerial(void *pvParameters);
void TaskSendJsonResponse(void *pvParameters);
void TaskUpdateWeight(void *pvParameters);
void TaskTurnMotorPasso(void *pvParameters);

void setup()
{
  Serial.begin(9600);
  pinMode(pinMotorLap, OUTPUT);
  digitalWrite(pinMotorLap, HIGH);
  pinMode(10, INPUT);

  scaleStatus = sensorCarga.setup();
  motorPasso.setup();

  // Criação das tarefas
  xTaskCreate(TaskReadSensor, "Read Sensor", 128, NULL, 1, NULL);
  xTaskCreate(TaskListenSerial, "Listen Serial", 256, NULL, 2, NULL);
  xTaskCreate(TaskSendJsonResponse, "Send JSON", 256, NULL, 2, NULL);
  xTaskCreate(TaskUpdateWeight, "Update Weight", 128, NULL, 1, NULL);
  xTaskCreate(TaskTurnMotorPasso, "Motor Passo", 128, NULL, 1, NULL);

  log("success", "arduino.arduinoConnected");
}

void loop()
{
  // O FreeRTOS controla as tarefas, o loop fica vazio
}

// Tarefa para ler o sensor e contar giros
void TaskReadSensor(void *pvParameters)
{
  static bool wasHigh = false;

  while (1)
  {
    if (digitalRead(10) == HIGH && !wasHigh)
    {
      wasHigh = true;
    }
    else if (digitalRead(10) == LOW && wasHigh)
    {
      wasHigh = false;
      countOfTurns++;
    }
    vTaskDelay(1 / portTICK_PERIOD_MS); // Delay de 1ms
  }
}

// Tarefa para atualizar o peso
void TaskUpdateWeight(void *pvParameters)
{
  while (1)
  {
    weight = sensorCarga.getWeight();
    vTaskDelay(125 / portTICK_PERIOD_MS); // Delay de 125ms
  }
}

// Tarefa para escutar comandos via Serial
void TaskListenSerial(void *pvParameters)
{
  while (1)
  {
    if (Serial.available())
    {
      String data = Serial.readString();

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
    vTaskDelay(125 / portTICK_PERIOD_MS); // Delay de 125ms
  }
}

// Tarefa para enviar a resposta JSON
void TaskSendJsonResponse(void *pvParameters)
{
  while (1)
  {
    String json = "{ \"weight\": " + String(weight, 1) +
                  ", \"motorWeightTurnOn\": " + (motorWeightTurnOn ? "true" : "false") +
                  ", \"motorLapTurnOn\": " + (motorLapTurnOn ? "true" : "false") +
                  ", \"scaleStatus\": " + (scaleStatus ? "true" : "false") +
                  ", \"countOfTurns\": " + String(countOfTurns) + "}";

    Serial.print("$");
    Serial.print(json);
    Serial.println("#");

    vTaskDelay(125 / portTICK_PERIOD_MS); // Delay de 125ms
  }
}

// Tarefa para controlar o motor de passo
void TaskTurnMotorPasso(void *pvParameters)
{
  while (1)
  {
    if (motorWeightTurnOn)
    {
      motorPasso.repeat();
    }
    vTaskDelay(125 / portTICK_PERIOD_MS); // Delay de 125ms
  }
}
