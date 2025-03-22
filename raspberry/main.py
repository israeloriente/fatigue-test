# Save
import socket
import RPi.GPIO as GPIO
import time
import json
import threading
# from hx711 import HX711

GPIO.setmode(GPIO.BCM)

# Variáveis globais
weight = 0.0
motorWeightTurnOn = True
motorLapPin = 2
motorLapTurnOn = False
scaleStatus = True
countOfTurnsPin = 17
countOfTurnsIsBlocked = False
countOfTurns = 0

# Configuração do HX711 (sensor de carda)
DT = 5
SCK = 6
# hx = HX711(DT, SCK)
# hx.set_reference_unit(82)
# hx.reset()
# hx.tare()

# Configuração do GPIO
GPIO.setup(motorLapPin, GPIO.OUT)
GPIO.setup(countOfTurnsPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

def log(message, client_socket):
    msg = {"isLog": True, "message": message}
    json_data = json.dumps(msg)
    client_socket.sendall((json_data + "\n").encode())

def processar_comando(command, client_socket):
    global motorWeightTurnOn, motorLapTurnOn, scaleStatus
    try:
        json_data = json.loads(command)
        print("Comando recebido:", json_data)
        if "motorWeightTurnOn" in json_data:
            motorWeightTurnOn = json_data["motorWeightTurnOn"]
        if "motorLapTurnOn" in json_data:
            motorLapTurnOn = json_data["motorLapTurnOn"]
            if motorLapTurnOn:
                GPIO.output(motorLapPin, GPIO.LOW)
            else:
                GPIO.output(motorLapPin, GPIO.HIGH)
    except json.JSONDecodeError as e:
        print("Erro ao parsear JSON:", e)

def startContaVoltas():
    global countOfTurns, countOfTurnsIsBlocked
    try:
        while True:
            sensor_state = GPIO.input(countOfTurnsPin)
            if sensor_state == GPIO.HIGH and not countOfTurnsIsBlocked:
                countOfTurns += 1
                countOfTurnsIsBlocked = True
            if sensor_state == GPIO.LOW:
                countOfTurnsIsBlocked = False
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nEncerrando Conta Voltas...")

def main():
    client_socket = esperar_conexao()  # Certificando que a conexão é feita antes de usar o client_socket
    try:
        while True:
            # weight = round(hx.get_weight(5) / 1000, 2)
            # Criação do JSON com os dados (pode incluir outros sensores aqui)
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
                client_socket = esperar_conexao()  # Recriar a conexão com o cliente

            # --------------------
            # ESCUTA DOS COMANDOS
            # --------------------
            try:
                client_socket.settimeout(0.5)  # Timeout para não travar o loop
                comando = client_socket.recv(1024).decode().strip()
                if comando:
                    processar_comando(comando, client_socket)
            except socket.timeout:
                # Ignora timeout, continua o loop
                pass
            except (ConnectionResetError, BrokenPipeError) as e:
                print("Cliente desconectado:", e)
                print("Tentando reconectar...")
                client_socket.close()
                client_socket = esperar_conexao()  # Recriar a conexão com o cliente

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Saindo...")
    finally:
        client_socket.close()
        server.close()
        GPIO.cleanup()

# Criando e iniciando as threads
thread_conta_voltas = threading.Thread(target=startContaVoltas)
thread_conta_voltas.daemon = True  # Torna a thread em daemon (fecha automaticamente com o programa principal)
thread_conta_voltas.start()

# Chamando a função main na thread principal
main()
