# import time
# import RPi.GPIO as GPIO
# from hx711 import HX711  # Importa a biblioteca instalada

# # Definição dos pinos do HX711
# DT = 5   # GPIO 5 (Pino físico 29)
# SCK = 6  # GPIO 6 (Pino físico 31)

# # Inicializa o HX711
# hx = HX711(DT, SCK)

# # Ajuste do fator de calibração (precisa ser calibrado conforme a balança usada)
# hx.set_reference_unit(82)  # Ajuste este valor durante a calibração

# # Faz a tara (zera a balança)
# hx.reset()
# hx.tare()

# print("Balança pronta! Iniciando leituras...")

# try:
#     while True:
#         peso = hx.get_weight(5) / 1000  # Média de 5 leitura
#         print(f"Peso lido: {peso:.3f} g")  # Exibe o peso arredondado para 2 casas decimais
#         time.sleep(1)  # Aguarda 1 segundo antes da próxima leitura

# except KeyboardInterrupt:
#     print("Saindo...")
#     GPIO.cleanup()


import time
import RPi.GPIO as GPIO
from hx711 import HX711  # Importa a biblioteca instalada

# Definição dos pinos do HX711
DT = 5   # GPIO 5 (Pino físico 29)
SCK = 6  # GPIO 6 (Pino físico 31)

# Inicializa o HX711
hx = HX711(DT, SCK)

# Faz a tara (zera a balança)
hx.reset()
hx.tare()

# Ajuste do fator de calibração
# Você pode precisar definir o valor manualmente durante a calibração
calibration_factor = 82  # Ajuste este valor durante a calibração

print("Balança pronta! Iniciando leituras...")

try:
    while True:
        peso = hx.get_weight(5) / calibration_factor  # Média de 5 leituras ajustada com o fator de calibração
        print(f"Peso lido: {peso:.3f} g")  # Exibe o peso arredondado para 3 casas decimais
        time.sleep(1)  # Aguarda 1 segundo antes da próxima leitura

except KeyboardInterrupt:
    print("Saindo...")
    GPIO.cleanup()
