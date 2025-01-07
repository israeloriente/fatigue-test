#include "HX711.h"

// Pinos do HX711 no Arduino
#define DOUT 5  // Pino DT (DOUT) do HX711
#define SCK 6   // Pino SCK (CLK) do HX711

HX711 balanca;

float fatorCalibracao = -18510.00; // Ajuste após a calibração
float peso;                     // Variável para armazenar o peso

void setup() {
  Serial.begin(9600);
  Serial.println("Iniciando balança...");

  // Configura o HX711
  balanca.begin(DOUT, SCK);

  // Testa se a balança está conectada
  if (!balanca.is_ready()) {
    Serial.println("Erro: Balança não conectada!");
    while (1);
  }
  Serial.println("Balança conectada!");

  // Zera a balança
  Serial.println("Zerando a balança...");
  balanca.set_scale(); // Configura sem fator de calibração
  balanca.tare();      // Remove qualquer peso inicial
  Serial.println("Balança zerada. Adicione peso para calibrar.");
}

void loop() {
  // Modo de calibração
  if (Serial.available()) {
    char comando = Serial.read();
    if (comando == 'c') {
      Serial.println("Calibrando... Coloque um peso conhecido na balança.");
      delay(5000); // Dê tempo para adicionar o peso

      // Defina o peso real em kg
      float pesoReal = 1.5; // Exemplo: Coloque 2 kg na balança
      balanca.set_scale();  // Remove fator de calibração temporário
      float leitura = balanca.get_units(10); // Obtém leitura média de 10 amostras
      fatorCalibracao = leitura / pesoReal;  // Calcula fator de calibração
      balanca.set_scale(fatorCalibracao);    // Define novo fator
      Serial.print("Fator de calibração ajustado para: ");
      Serial.println(fatorCalibracao);
    }
  }

  // Leitura do peso
  peso = balanca.get_units(10); // Obtém a média de 10 amostras
  Serial.print("Peso: ");
  Serial.print(peso, 3); // Exibe com 2 casas decimais
  Serial.println(" kg");

  delay(500); // Atualiza a cada meio segundo
}
