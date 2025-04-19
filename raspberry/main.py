import socket
import RPi.GPIO as GPIO
import time
import json
import threading
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

# Variáveis globais
client_socket = None
projectIsRunning = False
chegouAoPeso = False
weight = 0.0
maxWeight = 5 * 9.81
motorWeightTurnOn = False
motorLapPin = 2
motorLapTurnOn = False
countOfTurnsPin = 17
countOfTurnsIsBlocked = False
countOfTurns = 0
directionRotation = False
# Motor De passo #
DIR_PIN = 20     # Pino GPIO para controle de direção
STEP_PIN = 21    # Pino GPIO para envio de pulsos
ENABLE_PIN = 19  # Pino GPIO para habilitação do motor
SPR = 10000       # Qtd voltas

# Configuração do HX711 (sensor de carda)
DT = 5
SCK = 6
hx = HX711(DT, SCK)
hx.set_reference_unit(82)
hx.reset()
hx.tare()

# Configuração do GPIO
GPIO.setup(motorLapPin, GPIO.OUT)
GPIO.setup(countOfTurnsPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

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

def log(message, type="info"):
    global client_socket
    msg = {"isLog": True, "message": message, "type": type}
    json_data = json.dumps(msg)
    client_socket.sendall((json_data + "\n").encode())

def turnOnMotorLap(turnOn):
    global motorLapTurnOn
    if turnOn:
        log("raspberry.motorLapTurnedOn")
        GPIO.output(motorLapPin, GPIO.LOW)
    else:
        log("raspberry.motorLapTurnedOff")
        GPIO.output(motorLapPin, GPIO.HIGH)
    motorLapTurnOn = turnOn

def turnOnMotorWeight(turnOn):
    global motorWeightTurnOn, directionRotation, DIR_PIN, SPR, STEP_PIN
    motorWeightTurnOn = turnOn

    def motor_thread():
        if turnOn:
            log("raspberry.loadMotorTurnedOn", "info")
            GPIO.output(ENABLE_PIN, GPIO.LOW)
            GPIO.output(DIR_PIN, directionRotation)  # Define a direção (True = horário, False = anti-horário)
            for _ in range(SPR):
                if motorWeightTurnOn == False:  # Verifica se motorWeightTurnOn é False antes de cada iteração
                    break  # Sai do loop imediatamente
                GPIO.output(STEP_PIN, GPIO.HIGH)  # Pulso HIGH
                time.sleep(0.001)                # Aguarda
                GPIO.output(STEP_PIN, GPIO.LOW)  # Pulso LOW
                time.sleep(0.001)
        else:
            log("raspberry.loadMotorTurnedOff")
            GPIO.output(ENABLE_PIN, GPIO.HIGH)

    # Criando e iniciando a thread
    motor_thread = threading.Thread(target=motor_thread)
    motor_thread.daemon = True  # Torna a thread em daemon (fecha automaticamente com o programa principal)
    motor_thread.start()

def changeDirectionRotation(direction):
    global directionRotation
    turnOnMotorWeight(False)
    directionRotation = direction
    if direction:
        log("raspberry.directionClosing")
    else:
        log("raspberry.directionOpening")

def startProject():
    global countOfTurns, chegouAoPeso, directionRotation
    countOfTurns = 0
    chegouAoPeso = False
    log("raspberry.startProject", "success")
    changeDirectionRotation(True)
    turnOnMotorLap(True)
    turnOnMotorWeight(True)

def stopProject():
    global directionRotation, weight, chegouAoPeso
    chegouAoPeso = False
    changeDirectionRotation(False)
    turnOnMotorLap(False)
    turnOnMotorWeight(False)

def processar_comando(command):
    global motorWeightTurnOn, motorLapTurnOn, projectIsRunning, maxWeight
    try:
        json_data = json.loads(command)
        print("Comando recebido:", json_data)
        if "projectIsRunning" in json_data:
            projectIsRunning = json_data["projectIsRunning"]
            if projectIsRunning:
                startProject()
            else:
                stopProject()
        if "motorWeightTurnOn" in json_data:
            turnOnMotorWeight(json_data["motorWeightTurnOn"])
        if "directionRotation" in json_data:
            changeDirectionRotation(json_data["directionRotation"])
        if "motorLapTurnOn" in json_data:
            turnOnMotorLap(json_data["motorLapTurnOn"])
        if "maxWeight" in json_data:
            if json_data["maxWeight"] <= (40 * 9.81):
                maxWeight = json_data["maxWeight"]
                log("raspberry.maxWeightChanged", "success")
    except json.JSONDecodeError as e:
        print("Erro ao parsear JSON:", e)

def startContaVoltas():
    global countOfTurns, countOfTurnsIsBlocked, chegouAoPeso
    try:
        while True:
            sensor_state = GPIO.input(countOfTurnsPin)
            if sensor_state == GPIO.HIGH and not countOfTurnsIsBlocked and projectIsRunning and chegouAoPeso:
                countOfTurns += 1
                countOfTurnsIsBlocked = True
            if sensor_state == GPIO.LOW:
                countOfTurnsIsBlocked = False
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nEncerrando Conta Voltas...")

def main():
    global weight, chegouAoPeso, maxWeight, client_socket
    client_socket = esperar_conexao()  # Certificando que a conexão é feita antes de usar o client_socket
    log("raspberry.raspberryConnected", "success")
    try:
        while True:
            weight = round((hx.get_weight(5) / 1000) * 9.81, 2)

            if weight > maxWeight:
                if (not chegouAoPeso):
                    log("raspberry.weightIsOk", "success")
                    turnOnMotorWeight(False)
                chegouAoPeso = True

            # Criação do JSON com os dados (pode incluir outros sensores aqui)
            data = {
                "weight": str(weight),
                "motorWeightTurnOn": motorWeightTurnOn,
                "motorLapTurnOn": motorLapTurnOn,
                "countOfTurns": countOfTurns,
                "projectIsRunning": projectIsRunning,
                "directionRotation": directionRotation,
                "chegouAoPeso": chegouAoPeso,
                "maxWeight": maxWeight
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
                log("raspberry.raspberryConnected", "success")

            # --------------------
            # ESCUTA DOS COMANDOS
            # --------------------
            try:
                client_socket.settimeout(0.05)  # Timeout para não travar o loop
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
                client_socket = esperar_conexao()  # Recriar a conexão com o cliente
                log("raspberry.raspberryConnected", "success")

            time.sleep(0.05)
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
