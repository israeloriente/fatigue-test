import RPi.GPIO as GPIO
import time

SENSOR_PIN = 10  # Verifique qual GPIO está usando

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_PIN, GPIO.IN)

try:
    while True:
        estado = GPIO.input(SENSOR_PIN)
        print(f"Estado do sensor: {estado}")  # Deve imprimir 0 ou 1
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
