int contador = -1; // Variável para contar os objetos detectados

void setup()
{
  Serial.begin(9600);
  pinMode(10, INPUT); // Configura o pino 10 como entrada
}

void loop()
{
  // Verifica se o sensor detecta metal (sinal HIGH)
  if (digitalRead(10) == HIGH)
  {
    // Aguarda até que o sinal deixe de ser HIGH (objeto já detectado)
    while (digitalRead(10) == HIGH)
    {
    }
  }
  else
  {
    // Incrementa o contador ao detectar um objeto
    contador++;
    Serial.print("Número de voltas: ");
    Serial.println(contador);

    // Aguarda até que o sinal volte para HIGH (objeto saiu)
    while (digitalRead(10) == LOW)
    {
    }
  }
}
