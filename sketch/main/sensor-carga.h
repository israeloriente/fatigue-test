#ifndef SENSOR_CARGA_H
#define SENSOR_CARGA_H

#include "HX711.h" // Inclui a biblioteca HX711 para comunicação com o sensor de carga
#define DOUT 5     // Pino DT (DOUT) do HX711
#define SCK 6      // Pino SCK (CLK) do HX711

HX711 scale;                             // Instância do HX711
const float fatorCalibracao = -71085.50; // Fator de calibração conhecido

class SensorCarga
{
public:
  // Construtor: inicializa a variável weight
  SensorCarga() {}

  // Inicializa a balança
  bool setup()
  {
    Serial.begin(9600);
    scale.begin(DOUT, SCK);
    delay(1000);
    if (!scale.is_ready())
    {
      return false;
    }
    scale.set_scale(fatorCalibracao);
    scale.tare();
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
    return scale.get_units(amostras); // Lê o peso com base nas amostras
  }
};

#endif // Fim da proteção contra inclusão múltipla
