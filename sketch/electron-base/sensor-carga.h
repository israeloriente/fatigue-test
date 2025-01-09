#ifndef SENSOR_CARGA_H
#define SENSOR_CARGA_H

#include "HX711.h" // Inclui a biblioteca HX711 para comunicação com o sensor de carga

class SensorCarga
{
private:
  // Pinos fixos para o HX711
  const int pinDout = 5; // Pino DT (DOUT)
  const int pinSck = 6;  // Pino SCK (CLK)

  HX711 scale;                             // Instância do HX711
  const float fatorCalibracao = -71085.50; // Fator de calibração conhecido
  float weight;                            // Variável para armazenar o peso

public:
  // Construtor: inicializa a variável weight
  SensorCarga() : weight(0) {}

  // Inicializa a balança
  bool setup()
  {
    scale.begin(pinDout, pinSck); // Configura os pinos do HX711
    if (!scale.is_ready())
    {
      return false; // Retorna falso se a balança não estiver pronta
    }
    scale.set_scale(fatorCalibracao); // Define o fator de calibração
    scale.reset();                    // Zera a balança
    return true;                      // Retorna verdadeiro se tudo estiver pronto
  }

  bool test()
  {
    return true;
  }

  // Zera a balança
  void reset()
  {
    scale.tare(); // Remove qualquer peso residual
  }

  // Obtém o peso (com média de várias amostras)
  float getWeight(int amostras = 10)
  {
    weight = scale.get_units(amostras); // Lê o peso com base nas amostras
    return weight;                      // Retorna o valor lido
  }
};

#endif // Fim da proteção contra inclusão múltipla
