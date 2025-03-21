import RPi.GPIO as GPIO
import time

# Configuração dos pinos GPIO
DIR_PIN = 27     # Pino GPIO para controle de direção
STEP_PIN = 17    # Pino GPIO para envio de pulsos
SPR = 200        # Passos por rotação (ex: 1.8° por passo = 200 passos/rev)

# Configurações GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

# Função para mover o motor
def move_motor(steps, direction, delay=0.001):
    GPIO.output(DIR_PIN, direction)  # Define a direção (True = horário, False = anti-horário)
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)  # Pulso HIGH
        time.sleep(delay)                # Aguarda
        GPIO.output(STEP_PIN, GPIO.LOW)  # Pulso LOW
        time.sleep(delay)                # Aguarda

try:
    print("Movendo motor para frente (horário)...")
    move_motor(SPR, True, delay=0.001)  # 1 rotação completa (200 passos)

    time.sleep(1)

    print("Movendo motor para trás (anti-horário)...")
    move_motor(SPR, False, delay=0.001)  # 1 rotação completa (200 passos)

except KeyboardInterrupt:
    print("\nEncerrando o programa...")

finally:
    GPIO.cleanup()
