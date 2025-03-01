import socket
import RPi.GPIO as GPIO
import time
import json
from hx711 import HX711

# Globals variables
weight = 0.0
motorWeightTurnOn = True
motorLapTurnOn = True
scaleStatus = True
countOfTurns = 12

# Configuração do HX711 (sensor de carda)
DT = 5
SCK = 6
hx = HX711(DT, SCK)
hx.set_reference_unit(82)
hx.reset()
hx.tare()



# Configuração do Servidor TCP
HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 8080       # Porta de comunicação
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f'Servidor TCP rodando em {HOST}:{PORT}')

def esperar_conexao():
    print("Aguardando conexão do cliente...")
    client_socket, addr = server.accept()
    print('Cliente conectado:', addr)
    return client_socket

def log(message):
    msg = {"isLog": True, "message": message}
    json_data = json.dumps(msg)
    client_socket.sendall((json_data + "\n").encode())

client_socket = esperar_conexao()

def processar_comando(command):
    global motorWeightTurnOn, motorLapTurnOn, scaleStatus
    try:
        json_data = json.loads(comando)
        print("Comando recebido:", json_data)
        if "motorWeightTurnOn" in json_data:
            motorWeightTurnOn = json_data["motorWeightTurnOn"]
        if "motorLapTurnOn" in json_data:
            motorLapTurnOn = json_data["motorLapTurnOn"]

    except json.JSONDecodeError as e:
        print("Erro ao parsear JSON:", e)

try:
   while True:
        weight = round(hx.get_weight(5) / 1000, 3)

        # Cria o JSON com os dados do HX711
        data = {
            "weight": str(weight),
            "motorWeightTurnOn": motorWeightTurnOn,
            "motorLapTurnOn": motorLapTurnOn,
            "scaleStatus": scaleStatus,
            "countOfTurns": countOfTurns
        }

        # Converte o dicionário em JSON
        json_data = json.dumps(data)

        try:
            # Envia o JSON como string para o cliente
            client_socket.sendall((json_data + "\n").encode())
        except (BrokenPipeError, ConnectionResetError) as e:
            print("Erro na conexão com o cliente:", e)
            print("Tentando reconectar...")
            client_socket.close()
            client_socket = esperar_conexao()

        # --------------------
        # ESCUTA DOS COMANDOS
        # --------------------
        try:
            client_socket.settimeout(0.5)  # Timeout para não travar o loop
            comando = client_socket.recv(1024).decode().strip()
            if comando:
                processar_comando(comando)
        except socket.timeout:
            # Ignora timeout, continua o loop
            pass
        except (ConnectionResetError, BrokenPipeError) as e:
            print("Cliente desconectado:", e)
            print("Tentando reconectar...")
            client_socket.close()
            client_socket = esperar_conexao()

        time.sleep(0.1)
except KeyboardInterrupt:
    print("Saindo...")
finally:
    client_socket.close()
    server.close()
    # GPIO.cleanup()
