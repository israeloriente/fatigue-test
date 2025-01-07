#include <HX711.h>


//#include "Hx711.h" //Biblioteca do módulo da célula de carga

//Hx711 scale(A1, A0); // Setup de entrada da célula de carga
const int LOADCELL_DOUT_PIN = A1;
const int LOADCELL_SCK_PIN = A0;

HX711 scale;
const int m_ena = 2; //drive motor de passo / Aciona e desliga o motor
const int m_dir = 3; //drive motor de passo /Direção do movimento
const int m_pul = 4; //drive motor de passo / pulsos p rotação
boolean pulso = LOW; // variável para pulsos consecutivos p/ acionamento do motor
const int motor = 8; // Sinal de acionamento do motor principal via relé
volatile unsigned int x = 0;
volatile unsigned int y = 0;
unsigned int c = 0;
int vida = 0;

float t = 0;
float z = 0;
float tset = 0; // tensão ajustada para o ensaio ( a ser definida pelo usuáro)

void contador(); // laço de contagem do número de voltas

void setup()
{
  Serial.begin(9600);
  Serial.println("começar");
  pinMode(m_dir, OUTPUT); //Motor de passo
  pinMode(m_ena, OUTPUT); //Motor de passo
  pinMode(m_pul, OUTPUT); //Motor de passo
  digitalWrite(m_dir, HIGH); //Motor de passo
  digitalWrite(m_ena, LOW); //Motor de passo
  digitalWrite(m_pul, HIGH); //Motor de passo
  pinMode(motor, OUTPUT); // Motor principal
  digitalWrite(motor, HIGH); // Motor principal (Desligado até então)
  pinMode(7, INPUT_PULLUP); // sinal de entrada do sensor indutivo contador de voltas

attachInterrupt(digitalPinToInterrupt(7), contador, RISING);

}
void loop()
{

  while(Serial.available()){ //O programa inicia com o dado da tensão de flexão do teste via porta serial, executa esse loop até o usuário informar o valor da tensão
    delay(10);
    char aux = Serial.parseFloat();
    tset += aux; // Armazena o valor da tensão de flexão na variável tset

  t = ((-scale.read_average(1)+16758666)/4897,4); ///Uma vez definido a tensão de flexão do ensaio, o programa lê a tração aplicada no cabo de aço pela célula de carga.
// tração do cabo em N = (Valor da leitura + ajuste offset)/fator de escala, onde ajuste offset = - 16758666) e fator de escala = 4897,4
  //Serial.println(t);

     while(t < tset){ // Após a leitura da tração do cabo, a máquina entra no loop abaixo até que a tração do cabo atinja a tração desejada.

     for (int i = 0; i < 1000; i++){ //Executa mil ciclos no motor de passo (Cada ciclo corresponte ao movimento de 1,8º)
     pulso = !pulso;
     digitalWrite(m_pul, pulso);
     delayMicroseconds(100);
  }
  t = ((-scale.read_average(1)+16758666)/48974); // Lê novamente o valor da tração e continua no loop até que a tração do cabo atinja o nível desejado
  }
  while(t > tset/2){ // Enquanto a tração do cabo for maior que a tração definida/2, o loop abaixo mantem o motor de passo principal acionado
  digitalWrite(motor, LOW);
  t = ((-scale.read_average(1)+16758666)/48974); // dentro desse loop também ocorre o loop void contador acionado pela função "attachInterrupt(digitalPinToInterrupt(7), contador, RISING)",
  //essa função trabalha da seguinte forma, sempre que o sinal do sensor variar do sinal alto para baixo, significa que o eixo do corpo de prova deu uma volta, então ele executa o loop void contador
  // e soma UM na variável c que ao final do ensaio, corresponde ao número total de voltas que o corpo de prova suportou até a falha sob determinada tensão, definida pela tração aplicada no cabo de aço
}
  digitalWrite(motor, HIGH);//ao final do ensaio, o motor é desligado e o arduino imprime na porta serial a variável C com o total de número de voltas do corpo de prova;
  digitalWrite(m_ena, HIGH);
  Serial.println(c);
  }

  }

void contador(){
  c++;
}
