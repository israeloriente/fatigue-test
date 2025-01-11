#include "sensor-carga.h"
#include "utils.h"

float weight = 0.0;             // Peso da balança
bool scaleStatus = false;       // Status da balança
bool motorWeightTurnOn = false; // Motor 1 - Sensor de carga
bool motorLapTurnOn = false;    // Motor 2 - Motor de passo
int countOfTurns = 0;           // Quantidade de voltas
SensorCarga sensorCarga;

void setup()
{
  // Iniciar comunicação serial
  Serial.begin(9600);
  // scaleStatus = sensorCarga.setup();
  // Aguarde a comunicação serial estar pronta
  while (!Serial)
  {
    ; // Aguarda a conexão da porta serial
  }
  delay(1000);
  log("success", "Serial monitor conectado");
}

void loop()
{
  // Verifica se há dados disponíveis na porta serial
  if (Serial.available())
  {
    String data = Serial.readString(); // Lê o valor enviado pela serial

    // Processa os comandos recebidos
    if (data == "project.start")
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

  // weight = sensorCarga.getWeight();

  if (countOfTurns < 100 && motorLapTurnOn)
  {
    countOfTurns++;
  }
  else
  {
    countOfTurns = 0; // Zera o número de ciclos ao chegar em 420
  }

  // Incrementando o weight
  if (weight < 50 && motorWeightTurnOn)
  {
    weight += 0.08; // Incrementa de 0.3 em 0.3
    if (weight > 1)
    {
      turnOnMotorLap();
    }
    if (weight > 5)
    {
      turnOffMotorWeight();
    }
  }

  // // Formatar os valores em JSON
  String json = "{ \"weight\": " + String(weight, 1) +
                ", \"motorWeightTurnOn\": " + (motorWeightTurnOn ? "true" : "false") +
                ", \"motorLapTurnOn\": " + (motorLapTurnOn ? "true" : "false") +
                ", \"scaleStatus\": " + (scaleStatus ? "true" : "false") +
                ", \"countOfTurns\": " + String(countOfTurns) + "}";

  Serial.print("$");
  Serial.print(json);
  Serial.println("#");

  // Atraso de 0.4 segundos
  delay(500); // Atraso de 400 milissegundos entre as atualizações
}
