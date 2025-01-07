const int ena = 2;  //habilita o motor
const int dir = 3;  //determina a direção
const int pul = 4;  //executa um passo
int contador = 0;
const int intervalo = 1500;  //intervalo entre as mudanças de estado do pulso
boolean pulso = LOW;         //estado do pulso

void setup() {
  Serial.begin(9600);
  pinMode(ena, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(pul, OUTPUT);
  digitalWrite(ena, LOW);  //habilita em low invertida
  digitalWrite(dir, LOW);  // low CW / high CCW
  digitalWrite(pul, HIGH);  //borda de descida
}

void loop() {
  pulso = !pulso;            //inverte o estado da variável
  digitalWrite(pul, pulso);  //atribui o novo estado à porta
  delayMicroseconds(intervalo);
  contador++;
  if (contador == 3000) {
    Serial.println("Parou");
    while(1){}
  }
}
