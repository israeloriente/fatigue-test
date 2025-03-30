import RPi.GPIO as GPIO
import time

# Definição dos pinos
SENSOR_PIN = 17  # Pino GPIO onde o fio preto do sensor está conectado
contaRodrigo = 0
isBlocked = False

# Configuração do GPIO
GPIO.setmode(GPIO.BCM)  # Usando o esquema de numeração BCM
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Configura o pino do sensor como entrada com pull-up

print("Sensor Indutivo LJ12A3-4-Z/BX Iniciado (Ctrl+C para sair)")

try:
    while True:
        sensor_state = GPIO.input(SENSOR_PIN)
        if sensor_state == GPIO.HIGH and not isBlocked:
            contaRodrigo += 1
            isBlocked = True
        if (sensor_state == GPIO.LOW):
            isBlocked = False
        print(contaRodrigo)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nEncerrando o programa...")

finally:
    GPIO.cleanup()  # Restaura os pinos GPIO ao estado original
