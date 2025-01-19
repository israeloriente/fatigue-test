#ifndef MOTOR_PASSO_H
#define MOTOR_PASSO_H

const int ena = 2; // habilita o motor
const int dir = 3; // determina a direção
const int pul = 4; // executa um passo
int contador = 0;
const int intervalo = 1000; // intervalo entre as mudanças de estado do pulso
boolean pulso = LOW;        // estado do pulso

class MotorPasso
{
public:
  MotorPasso() {}

  void setup()
  {
    pinMode(ena, OUTPUT);
    pinMode(dir, OUTPUT);
    pinMode(pul, OUTPUT);
    digitalWrite(ena, LOW);
    digitalWrite(dir, LOW);
    digitalWrite(pul, HIGH);
  }

  void repeat()
  {
    pulso = !pulso;
    digitalWrite(pul, pulso);
    delayMicroseconds(intervalo);
  }

  void changeDirection()
  {
    digitalWrite(dir, !digitalRead(dir));
  }
};

#endif
