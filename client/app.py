from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT

import json
import time
import paho.mqtt.client as mqtt

CounterFitConnection.init('localhost', 5000)

# Broker
id = '91c4a0a0-0e35-40cb-a603-3b42611f15dd'  # gerado no guidgen
client_name = id + 'embarcados_client'
client_telemetry_topic_sensor1 = id + '/telemetry/sensor1'
client_telemetry_topic_sensor2 = id + '/telemetry/sensor2'
server_command_topic = id + '/commands'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print('MQTT connected')

sensor1 = DHT("11", 0)
sensor2 = DHT("11", 2)


def handle_command(client, userdata, message):
    payload_sensor1 = json.loads(message.payload.decode())
    print('Message received for sensor 1:', payload_sensor1)

    payload_sensor2 = json.loads(message.payload.decode())
    print('Message received for sensor 2:', payload_sensor2)

while True:
    _, temperature_sensor1 = sensor1.read()
    telemetry_sensor1 = json.dumps({'temperature_sensor1': temperature_sensor1})
    print(f'temperature_sensor1 {temperature_sensor1}°C')
    mqtt_client.publish(client_telemetry_topic_sensor1, telemetry_sensor1)

    _, temperature_sensor2 = sensor2.read()
    telemetry_sensor2 = json.dumps({'temperature_sensor2': temperature_sensor2})
    print(f'temperature_sensor2 {temperature_sensor2}°C')
    mqtt_client.publish(client_telemetry_topic_sensor2, telemetry_sensor2)

    time.sleep(10)
