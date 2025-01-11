#ifndef UTILS_H
#define UTILS_H

#include <Arduino.h>

void log(String type, String message);
void startProject();
void stopProject();
void turnOnMotorWeight();
void turnOffMotorWeight();
void turnOnMotorLap();
void turnOffMotorLap();

#endif
