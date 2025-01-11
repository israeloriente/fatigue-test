class MotorPasso
{
private:
  const int ena = 2;          // Pino para habilitar o motor
  const int dir = 3;          // Pino para direção
  const int pul = 4;          // Pino para pulsos
  const int intervalo = 1500; // Intervalo entre os pulsos em microsegundos
  boolean pulso;              // Estado atual do pulso

public:
  // Construtor: Inicializa as variáveis e configura os pinos
  MotorPasso()
  {
    pulso = LOW;

    pinMode(ena, OUTPUT);
    pinMode(dir, OUTPUT);
    pinMode(pul, OUTPUT);

    digitalWrite(ena, LOW);  // Habilita o motor (LOW invertida)
    digitalWrite(dir, LOW);  // Direção padrão (LOW para CW, HIGH para CCW)
    digitalWrite(pul, HIGH); // Inicializa pulso em HIGH
  }

  // Função para executar um passo
  void step()
  {
    pulso = !pulso;           // Inverte o estado do pulso
    digitalWrite(pul, pulso); // Define o novo estado no pino
    delayMicroseconds(intervalo);
  }

  // Função para parar o motor
  void stop()
  {
    digitalWrite(ena, HIGH); // Desabilita o motor
  }

  void start()
  {
    digitalWrite(ena, LOW);
  }
};
