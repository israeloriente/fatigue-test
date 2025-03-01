import RPi.GPIO as GPIO
import time

# Definir o pino do sensor (pode mudar se necessário)
SENSOR_PIN = 10  # GPIO 17 (Pino físico 11)

# Configuração do Raspberry Pi
GPIO.setmode(GPIO.BCM)  # Usa a numeração de pinos GPIO (BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)  # Define o pino como entrada

print("Sensor de proximidade pronto! Aguardando detecção...")

try:
    while True:
        estado = GPIO.input(SENSOR_PIN)  # Lê o estado do sensor

        if estado == GPIO.HIGH:  # Se for PNP, será HIGH quando detectar metal
            print("⚡ Objeto detectado!")
        else:
            print("🔍 Nenhum objeto próximo.")

        time.sleep(0.5)  # Pequeno delay para evitar leitura excessiva

except KeyboardInterrupt:
    print("Saindo...")
    GPIO.cleanup()  # Libera os pinos GPIO ao sair
