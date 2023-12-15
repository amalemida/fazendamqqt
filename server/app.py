import json
import time
import paho.mqtt.client as mqtt
import requests
from datetime import datetime

id = '91c4a0a0-0e35-40cb-a603-3b42611f15dd'  # gerado no guidgen
client_telemetry_topic_sensor1 = id + '/telemetry/sensor1'
client_telemetry_topic_sensor2 = id + '/telemetry/sensor2'
client_telemetry_topic_sensor3 = id + '/telemetry/sensor3'
server_command_topic = id + '/commands'
client_name = id + 'embarcados_server'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

tmax1 = float('-inf')  # Inicializando tmax como infinito negativo
tmin1 = float('inf')  # Inicializando tmin como infinito positivo
tmax2 = float('-inf')
tmin2 = float('inf')

def handle_telemetry(client, userdata, message):
    global tmax1, tmedia1, tmin1, tmax2, tmin2, tmedia2, tmax3, tmedia3, tmin3 
    global irrigar, tempo_medicao

    tempo_medicao = 30 # intervalo das medicoes

    endpoint_url = 'http://localhost:5088/api/temperatura'
    endpoint_irrigacao = 'http://localhost:5088/api/Estado_Irrigacao/'
    current_datetime = datetime.now()
    current_time = datetime.strptime(current_time_str, "%H:%M:%S").time()
    start_time = datetime.strptime("08:00:00", "%H:%M:%S").time()
    end_time = datetime.strptime("17:05:00", "%H:%M:%S").time()
    payload = json.loads(message.payload.decode())

    #Enviar informações de temperatura sensor 1
    if 'temperature_sensor1' in payload:
        temperature_sensor1 = payload['temperature_sensor1']
        print('Message received from sensor 1:', temperature_sensor1)
        
        if temperature_sensor1 < tmin1:
            tmin1 = temperature_sensor1
            print(f'temperature_sensor1: {temperature_sensor1}, tmax1: {tmax1}')
        if temperature_sensor1 > tmax1:
            tmax1 = temperature_sensor1
            print(f'temperature_sensor1: {temperature_sensor1}, tmax1: {tmax1}')

        tmedia1 = (tmax1 + tmin1)/2

        command_sensor1 = {
            "sensorId": 1,
            "tmax": tmax1,
            "tmin": tmin1,
            "tmedia": tmedia1,
            "data": current_datetime
        }

        print('Sending command for sensor 1:', command_sensor1)
        
        command_json_sensor1 = json.dumps(command_sensor1)

        if start_time <= current_time <= end_time:
            response_sensor1 = requests.post(endpoint_url, data=command_json_sensor1, headers={'Content-Type': 'application/json'})
        
            if response_sensor1.status_code == 201:
                print("Command for sensor 1 successfully sent!")
            else:
                print("Error sending command for sensor 1:", response_sensor1.status_code)
                print("Response content:", response_sensor1.content)
        else:
            print("Waiting for telemetry transmission window.")

    #Enviar informações de irrigação sensor 1
    if 'umidade_sensor1' in payload:
        umidade_sensor1 = payload['umidade_sensor1']
        print('Message received from sensor 1:', umidade_sensor1)

        if umidade_sensor1 > 450:
            irrigar = True
        else:
            irrigar = False

        command_irrigar_sensor1 = {
            "irrigar" : irrigar
        }

        command_json_irrigar_sensor1 = json.dumps(command_irrigar_sensor1)

        if start_time <= current_time <= end_time:
            response_irrigar_sensor1 = requests.put(endpoint_irrigacao+'1', data=command_json_irrigar_sensor1, headers={'Content-Type': 'application/json'})
        
            if response_irrigar_sensor1.status_code == 201:
                print("Command for sensor 1 successfully sent!")
            else:
                print("Error sending command for sensor 1:", response_irrigar_sensor1.status_code)
                print("Response content:", response_irrigar_sensor1.content)
        else:
            print("Waiting for telemetry transmission window.")

    #Enviar informações de temperatura sensor 2
    if 'temperature_sensor2' in payload:
        temperature_sensor2 = payload['temperature_sensor2']
        print('Message received from sensor 2:', temperature_sensor2)

        if temperature_sensor2 < tmin2:
            tmin2 = temperature_sensor2
        if temperature_sensor2 > tmax2:
            tmax2 = temperature_sensor2
        
        tmedia2 = (tmax2 + tmin2)/2
            
        command_sensor2 = { 
            "sensorId": 2,
            "tmax": tmax2,
            "tmin": tmin2,
            "tmedia" : tmedia2,
            "data": current_datetime
        }
        print('Sending command for sensor 2:', command_sensor2)
        
        command_json_sensor2 = json.dumps(command_sensor2)
        
        if start_time <= current_time <= end_time:
            response_sensor2 = requests.post(endpoint_url, data=command_json_sensor2, headers={'Content-Type': 'application/json'})
            
            if response_sensor2.status_code == 201:
                print("Command for sensor 2 successfully sent!")
            else:
                print("Error sending command for sensor 2:", response_sensor2.status_code)
                print("Response content:", response_sensor2.content)
        else:
            print("Waiting for telemetry transmission window.")
    
    #Enviar informações de irrigação sensor 2
    if 'umidade_sensor2' in payload:
        umidade_sensor2 = payload['umidade_sensor2']
        print('Message received from sensor 2:', umidade_sensor2)

        if umidade_sensor2 > 450:
            irrigar = True
        else:
            irrigar = False

        command_irrigar_sensor2 = {
            "irrigar" : irrigar
        }

        command_json_irrigar_sensor2 = json.dumps(command_irrigar_sensor2)

        if start_time <= current_time <= end_time:
            response_irrigar_sensor2 = requests.put(endpoint_irrigacao+'2', data=command_json_irrigar_sensor2, headers={'Content-Type': 'application/json'})
        
            if response_irrigar_sensor2.status_code == 201:
                print("Command for sensor 1 successfully sent!")
            else:
                print("Error sending command for sensor 1:", response_irrigar_sensor2.status_code)
                print("Response content:", response_irrigar_sensor2.content)
        else:
            print("Waiting for telemetry transmission window.")

    #Enviar informações de temperatura sensor 3
    if 'temperature_sensor3' in payload:
        temperature_sensor3 = payload['temperature_sensor3']
        print('Message received from sensor 3:', temperature_sensor3)
        
        if temperature_sensor3 < tmin3:
            tmin3 = temperature_sensor3
            print(f'temperature_sensor3: {temperature_sensor3}, tmax1: {tmax3}')
        if temperature_sensor3 > tmax3:
            tmax3 = temperature_sensor3
            print(f'temperature_sensor3: {temperature_sensor3}, tmax3: {tmax3}')

        tmedia3 = (tmax3 + tmin3)/2

        command_sensor3 = {
            "sensorId": 3,
            "tmax": tmax3,
            "tmin": tmin3,
            "tmedia": tmedia3,
            "data": current_datetime
        }

        print('Sending command for sensor 3:', command_sensor3)
        
        command_json_sensor3 = json.dumps(command_sensor3)

        if start_time <= current_time <= end_time:
            response_sensor3 = requests.post(endpoint_url, data=command_json_sensor3, headers={'Content-Type': 'application/json'})
        
            if response_sensor3.status_code == 201:
                print("Command for sensor 3 successfully sent!")
            else:
                print("Error sending command for sensor 3:", response_sensor3.status_code)
                print("Response content:", response_sensor3.content)
        else:
            print("Waiting for telemetry transmission window.")

    #Enviar informações de irrigação sensor 3
    if 'umidade_sensor3' in payload:
        umidade_sensor3 = payload['umidade_sensor3']
        print('Message received from sensor 3:', umidade_sensor3)

        if umidade_sensor3 > 450:
            irrigar = True
        else:
            irrigar = False

        command_irrigar_sensor3 = {
            "irrigar" : irrigar
        }

        command_json_irrigar_sensor3 = json.dumps(command_irrigar_sensor3)

        if start_time <= current_time <= end_time:
            response_irrigar_sensor3 = requests.put(endpoint_irrigacao+'3', data=command_json_irrigar_sensor3, headers={'Content-Type': 'application/json'})
        
            if response_irrigar_sensor3.status_code == 201:
                print("Command for sensor 1 successfully sent!")
            else:
                print("Error sending command for sensor 1:", response_irrigar_sensor3.status_code)
                print("Response content:", response_irrigar_sensor3.content)
        else:
            print("Waiting for telemetry transmission window.")

while True:
    mqtt_client.subscribe(client_telemetry_topic_sensor1)
    mqtt_client.subscribe(client_telemetry_topic_sensor2)
    mqtt_client.subscribe(client_telemetry_topic_sensor3)
    mqtt_client.on_message = handle_telemetry

    time.sleep(tempo_medicao)
