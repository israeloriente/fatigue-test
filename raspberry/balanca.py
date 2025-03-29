import time
import RPi.GPIO as GPIO
from hx711 import HX711  # Importa a biblioteca instalada

# Definição dos pinos do HX711
DT = 5   # GPIO 5 (Pino físico 29)
SCK = 6  # GPIO 6 (Pino físico 31)

# Inicializa o HX711
hx = HX711(DT, SCK)

# Ajuste do fator de calibração (precisa ser calibrado conforme a balança usada)
hx.set_reference_unit(82)  # Ajuste este valor durante a calibração

# Faz a tara (zera a balança)
hx.reset()
hx.tare()

print("Balança pronta! Iniciando leituras...")

try:
    while True:
        peso = hx.get_weight(5) / 1000  # Média de 5 leitura
        print(f"Peso lido: {peso:.3f} g")  # Exibe o peso arredondado para 2 casas decimais
        time.sleep(1)  # Aguarda 1 segundo antes da próxima leitura

except KeyboardInterrupt:
    print("Saindo...")
    GPIO.cleanup()


# import time
# import RPi.GPIO as GPIO
# from hx711 import HX711

# # Defina os pinos do Raspberry Pi conectados ao HX711
# DT = 5  # Pino de dados (DT) do HX711
# SCK = 6  # Pino de clock (SCK) do HX711

# # Inicialize a interface do HX711
# hx = HX711(DT, SCK)

# # Função para calibrar o HX711
# def calibrar():
#     print("Calibrando... Coloque um peso conhecido sobre a balança.")
#     input("Pressione Enter para começar a calibração...")

#     hx.reset()  # Resetar o HX711
#     hx.tare()  # Definir o valor zero

#     # Leia o valor de calibração
#     print("Leitura do valor sem peso:", hx.get_raw_data())

#     print("Agora, coloque um peso conhecido e pressione Enter.")
#     input("Pressione Enter quando estiver pronto para fazer a calibração final...")

#     # Coloque um peso conhecido (ex: 1kg) e defina a calibração
#     hx.set_reference_unit(1)  # Ajuste a unidade de referência (ajuste para o seu sensor)
#     print("Peso de calibração:")
#     print(hx.get_weight(5))  # Medir o peso usando a unidade de referência
#     print("Calibração concluída.")

# # Função para medir o peso
# def medir_peso():
#     hx.tare()  # Definir zero
#     print("Aguarde... medindo o peso")
#     time.sleep(2)  # Aguarde a leitura estabilizar
#     peso = hx.get_weight(5)  # Pegue a média de 5 leituras
#     print(f"Peso medido: {peso:.2f} gramas")
#     hx.power_off()  # Desligue o HX711

# if __name__ == "__main__":
#     try:
#         calibrar()  # Calibrar o sensor
#         while True:
#             medir_peso()  # Medir o peso continuamente
#             time.sleep(1)  # Delay para estabilizar a leitura
#     except KeyboardInterrupt:
#         print("Programa interrompido.")
#         GPIO.cleanup()
