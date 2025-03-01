import RPi.GPIO as GPIO
import time

SENSOR_PIN = 10  # Defina corretamente o GPIO que está usando

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Adiciona pull-up interno

print("Monitorando o sensor... Pressione Ctrl+C para sair.")

try:
    while True:
        estado = GPIO.input(SENSOR_PIN)
        if estado == GPIO.LOW:
            print("⚡ Objeto detectado!")
        else:
            print("🔍 Nenhum objeto próximo.")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nSaindo...")
    GPIO.cleanup()
