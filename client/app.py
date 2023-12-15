from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

import json
import time
import paho.mqtt.client as mqtt

CounterFitConnection.init('localhost', 5000)

# Broker
id = '91c4a0a0-0e35-40cb-a603-3b42611f15dd'  # gerado no guidgen
client_name = id + 'embarcados_client'
client_telemetry_topic_sensor1 = id + '/telemetry/sensor1'
client_telemetry_topic_sensor2 = id + '/telemetry/sensor2'
client_telemetry_topic_sensor3 = id + '/telemetry/sensor3'
server_command_topic = id + '/commands'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print('MQTT connected')

sensor1 = DHT("11", 0)
sensor2 = DHT("11", 2)
sensor3 = DHT("11", 4)
adc1 = ADC(7)
adc2 = ADC(9)
adc3 = ADC(11)
relay1 = GroveRelay(6)
relay2 = GroveRelay(8)
relay3 = GroveRelay(10)


def handle_command(client, userdata, message):
    payload_sensor1 = json.loads(message.payload.decode())
    print('Message received for sensor 1:', payload_sensor1)

    payload_sensor2 = json.loads(message.payload.decode())
    print('Message received for sensor 2:', payload_sensor2)

    payload_sensor3 = json.loads(message.payload.decode())
    print('Message received for sensor 3:', payload_sensor3)

while True:
    soil_moisture1 = adc1.read(0)
    print("Soil moisture1:", soil_moisture1)

    if soil_moisture1 > 450:
        print("Soil Moisture 1 is too low, turning relay1 on.")
        relay1.on()
        time.sleep(5)
        print("Turning relay1 off.")
        relay1.off()
    else:
        print("Soil Moisture 1 is ok, turning relay1 off.")
        relay1.off()

    soil_moisture2 = adc2.read(0)
    print("Soil moisture2:", soil_moisture2)

    if soil_moisture2 > 450:
        print("Soil Moisture 2 is too low, turning relay2 on.")
        relay2.on()
        time.sleep(5)
        print("Turning relay2 off.")
        relay2.off()
    else:
        print("Soil Moisture 2 is ok, turning relay2 off.")
        relay2.off()

    soil_moisture3 = adc3.read(0)
    print("Soil moisture3:", soil_moisture3)

    if soil_moisture3 > 450:
        print("Soil Moisture 3 is too low, turning relay3 on.")
        relay3.on()
        time.sleep(5)
        print("Turning relay3 off.")
        relay3.off()
    else:
        print("Soil Moisture 3 is ok, turning relay3 off.")
        relay1.off()

    _, temperature_sensor1 = sensor1.read()
    telemetry_sensor1 = json.dumps({'temperature_sensor1': temperature_sensor1, 'umidade_sensor1': soil_moisture1})
    print(f'temperature_sensor1 {temperature_sensor1}°C')
    mqtt_client.publish(client_telemetry_topic_sensor1, telemetry_sensor1)

    _, temperature_sensor2 = sensor2.read()
    telemetry_sensor2 = json.dumps({'temperature_sensor2': temperature_sensor2, 'umidade_sensor2': soil_moisture2})
    print(f'temperature_sensor2 {temperature_sensor2}°C')
    mqtt_client.publish(client_telemetry_topic_sensor2, telemetry_sensor2)

    _, temperature_sensor3 = sensor3.read()
    telemetry_sensor3 = json.dumps({'temperature_sensor3': temperature_sensor3, 'umidade_sensor3': soil_moisture2})
    print(f'temperature_sensor3 {temperature_sensor3}°C')
    mqtt_client.publish(client_telemetry_topic_sensor2, telemetry_sensor2)

    time.sleep(30)
