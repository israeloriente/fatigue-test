volatile int contador = 0; // Variável para armazenar a contagem das voltas

void setup() {
  pinMode(7, INPUT_PULLUP); // Configurar o pino 2 como entrada com resistor pull-up interno
  attachInterrupt(digitalPinToInterrupt(7), contarVolta, FALLING); // Configurar interrupção para borda de descida (NPN fecha para GND)
  Serial.begin(9600); // Iniciar comunicação serial para monitoramento
}

void loop() {
  // Exibir o número de voltas detectadas a cada segundo
  Serial.print("Voltas detectadas: ");
  Serial.println(contador);
  delay(1000); // Atualizar a cada 1 segundo
}

// Função chamada pela interrupção
void contarVolta() {
  contador++; // Incrementar o contador quando o sensor detecta uma volta
}
