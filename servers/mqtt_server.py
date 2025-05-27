import paho.mqtt.client as mqtt  
import local_status

client_id = 'car'
broker = "192.168.1.5" 
port = 1883 
keepalive = 60

def listen():
    local_status.MQTT_CLIENT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    local_status.MQTT_CLIENT.user_data_set([])
    local_status.MQTT_CLIENT.connect(broker, port, keepalive)
    local_status.MQTT_READY = True
    print(f"[MQTT Ready]")

def driveCar(topic, speed):
    local_status.MQTT_CLIENT.publish(topic, speed)