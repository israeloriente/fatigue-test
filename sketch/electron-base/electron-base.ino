// Definindo as variáveis
int number_of_cycles = 0;
float stress_strain = 0.0;
int life = 0;
bool motor_status = false;        // Motor 1 - Inicialmente desligado (false)
bool motor2_status = false;       // Motor 2 - Inicialmente desligado (false)
bool gyro_sensor_status = false;  // Sensor de giro - Inicialmente desligado (false)

void setup() {
  // Iniciar comunicação serial
  Serial.begin(115200);

  // Aguarde a comunicação serial estar pronta
  while (!Serial) {
    ;  // Aguarda a conexão da porta serial
  }
}

void loop() {
  // Verifica se há dados disponíveis na porta serial
  if (Serial.available()) {
    int received_value = Serial.parseInt();  // Lê o valor enviado pela serial

    // Processa os comandos recebidos
    switch (received_value) {
      case 1:
        motor_status = true;  // Liga o motor 1
        break;
      case 2:
        motor_status = false;  // Desliga o motor 1
        break;
      case 3:
        motor2_status = true;  // Liga o motor 2
        break;
      case 4:
        motor2_status = false;  // Desliga o motor 2
        break;
      case 5:
        gyro_sensor_status = true;  // Liga o sensor de giro
        break;
      case 6:
        gyro_sensor_status = false;  // Desliga o sensor de giro
        break;
      default:
        break;  // Ignora qualquer outro valor
    }
  }

  // Incrementando o number_of_cycles
  if (number_of_cycles < 420) {
    number_of_cycles++;
  } else {
    number_of_cycles = 0;  // Zera o número de ciclos ao chegar em 420
  }

  // Incrementando o life
  if (life < 42) {
    life++;
  } else {
    life = 0;  // Zera o life ao atingir 42
  }

  // Incrementando o stress_strain
  if (stress_strain < 10) {
    stress_strain += 0.3;  // Incrementa de 0.3 em 0.3
  } else {
    stress_strain = 0.0;  // Zera o stress_strain ao atingir 10
  }

  // // Formatar os valores em JSON
  String json = "{\"Number_of_Cycles\": " + String(number_of_cycles) +
                ", \"Stress_Strain\": " + String(stress_strain, 1) +
                ", \"Life\": " + String(life) +
                ", \"Motor_Status\": " + (motor_status ? "true" : "false") +
                ", \"Motor2_Status\": " + (motor2_status ? "true" : "false") +
                ", \"Gyro_Sensor_Status\": " + (gyro_sensor_status ? "true" : "false") + "}";

  Serial.print("$"); 
  Serial.print(json);
  Serial.print("#");

  // Atraso de 0.4 segundos
  delay(500);  // Atraso de 400 milissegundos entre as atualizações
}
