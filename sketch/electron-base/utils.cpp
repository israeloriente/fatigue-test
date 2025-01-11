#include "utils.h"

extern float weight;
extern bool scaleStatus;
extern bool motorWeightTurnOn;
extern bool motorLapTurnOn;
extern int countOfTurns;

void log(String type, String message)
{
	Serial.print("&");
	Serial.print("{ \"type\": \"" + type + "\", \"message\": \"" + message + "\"}");
	Serial.println("%");
}

void startProject()
{
	motorWeightTurnOn = true;
	motorLapTurnOn = false;
	weight = 0.0;
	countOfTurns = 0;
	log("info", "Sensor de carga ativado");
}

void stopProject()
{
	motorWeightTurnOn = false;
	motorLapTurnOn = false;
	weight = 0.0;
	countOfTurns = 0;
	log("info", "Processo Interrompido");
}

void turnOnMotorWeight()
{
	motorWeightTurnOn = true;
	log("info", "Motor de carga ligado");
}

void turnOffMotorWeight()
{
	if (motorWeightTurnOn == true)
	{
		motorWeightTurnOn = false;
		log("info", "Motor de carga desligado");
	}
}

void turnOnMotorLap()
{
	if (motorLapTurnOn == false)
	{
		motorLapTurnOn = true;
		log("info", "Motor de passo ligado");
	}
}

void turnOffMotorLap()
{
	motorLapTurnOn = false;
	log("info", "Motor de passo desligado");
}
