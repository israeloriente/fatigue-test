import RPi.GPIO as GPIO
from hx711 import HX711

# Configurações dos pinos
DT = 5   # Data Out
SCK = 6  # Clock

# Inicializa o HX711
hx = HX711(DT, SCK)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()
hx.tare()

print("Coloque o objeto na balança...")

try:
    while True:
        # Leitura do valor bruto
        valor = hx.get_weight(5)
        print("Peso: {:.2f} g".format(valor))
        hx.power_down()
        hx.power_up()
except KeyboardInterrupt:
    print("Saindo...")
    GPIO.cleanup()
