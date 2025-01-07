#include "HX711.h"

// Pinos do HX711 no Arduino
#define DOUT 5 // Pino DT (DOUT) do HX711
#define SCK 6  // Pino SCK (CLK) do HX711

HX711 balanca;

// Fator de calibração conhecido (ajuste para o valor exato)
float fatorCalibracao = -71085.50; // Valor calibrado previamente (-71085.50 quase funciona)
float peso;                        // Variável para armazenar o peso

void setup()
{
  Serial.begin(9600);
  Serial.println("Iniciando balança...");

  // Configura o HX711
  balanca.begin(DOUT, SCK);

  // Testa se a balança está conectada
  if (!balanca.is_ready())
  {
    Serial.println("Erro: Balança não conectada!");
    while (1)
      ; // Para o código se a balança não estiver conectada
  }
  Serial.println("Balança conectada!");

  // Define o fator de calibração conhecido
  balanca.set_scale(fatorCalibracao);

  // Zera a balança
  Serial.println("Zerando a balança...");
  balanca.tare(); // Remove qualquer peso residual
  Serial.println("Balança zerada e pronta para uso.");
}

void loop()
{
  // Leitura do peso
  peso = balanca.get_units(20); // Obtém a média de 10 amostras
  Serial.print("Peso: ");
  Serial.print(peso, 1); // Exibe com 2 casas decimais
  Serial.println(" kg");

  delay(500); // Atualiza a cada meio segundo
}
