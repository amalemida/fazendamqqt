import json
import time
import paho.mqtt.client as mqtt
import requests
from datetime import datetime

id = '91c4a0a0-0e35-40cb-a603-3b42611f15dd'  # gerado no guidgen
client_telemetry_topic_sensor1 = id + '/telemetry/sensor1'
client_telemetry_topic_sensor2 = id + '/telemetry/sensor2'
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
    global tmax1, tmin1, tmax2, tmin2

    endpoint_url = 'http://localhost:5088/api/temperatura'
    current_datetime = datetime.now()
    current_date_str = current_datetime.strftime("%d-%m-%Y")
    current_time_str = current_datetime.strftime("%H:%M:%S")
    current_time = datetime.strptime(current_time_str, "%H:%M:%S").time()
    start_time = datetime.strptime("08:00:00", "%H:%M:%S").time()
    end_time = datetime.strptime("17:05:00", "%H:%M:%S").time()
    payload = json.loads(message.payload.decode())

    if 'temperature_sensor1' in payload:
        temperature_sensor1 = payload['temperature_sensor1']
        print('Message received from sensor 1:', temperature_sensor1)
        
        if temperature_sensor1 < tmin1:
            tmin1 = temperature_sensor1
            print(f'temperature_sensor1: {temperature_sensor1}, tmax1: {tmax1}')
        if temperature_sensor1 > tmax1:
            tmax1 = temperature_sensor1
            print(f'temperature_sensor1: {temperature_sensor1}, tmax1: {tmax1}')

        command_sensor1 = {
            "sensorId": 1,
            "tmax": tmax1,
            "tmin": tmin1,
            "data": current_date_str,
            "hora": current_time_str
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

    if 'temperature_sensor2' in payload:
        temperature_sensor2 = payload['temperature_sensor2']
        print('Message received from sensor 2:', temperature_sensor2)

        if temperature_sensor2 < tmin2:
            tmin2 = temperature_sensor2
        if temperature_sensor2 > tmax2:
            tmax2 = temperature_sensor2
            
        command_sensor2 = { 
            "sensorId": 2,
            "tmax": tmax2,
            "tmin": tmin2,
            "data": current_date_str,
            "hora": current_time_str
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

while True:
    mqtt_client.subscribe(client_telemetry_topic_sensor1)
    mqtt_client.subscribe(client_telemetry_topic_sensor2)
    mqtt_client.on_message = handle_telemetry

    time.sleep(10)
