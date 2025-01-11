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
	log("info", "arduino.loadCellMotorActivated");
}

void stopProject()
{
	motorWeightTurnOn = false;
	motorLapTurnOn = false;
	weight = 0.0;
	countOfTurns = 0;
	log("info", "arduino.processInterrupted");
}

void turnOnMotorWeight()
{
	motorWeightTurnOn = true;
	log("info", "arduino.loadMotorTurnedOn");
}

void turnOffMotorWeight()
{
	if (motorWeightTurnOn == true)
	{
		motorWeightTurnOn = false;
		log("info", "arduino.loadMotorTurnedOff");
	}
}

void turnOnMotorLap()
{
	if (motorLapTurnOn == false)
	{
		motorLapTurnOn = true;
		log("info", "arduino.lapMotorTurnedOn");
	}
}

void turnOffMotorLap()
{
	motorLapTurnOn = false;
	log("info", "arduino.lapMotorTurnedOff");
}
