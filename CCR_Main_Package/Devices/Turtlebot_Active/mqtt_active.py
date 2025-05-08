import paho.mqtt.client as mqtt
import time
import socket
import json

# Configurable parameters
ROBOT_ID = "INR90"
ROLE = "active"
DOMINANCE = 5
DEVICE_TYPE = "Active"
DEVICE_NAME = "Turtlebot1"
DECISION = "Scanning"

MQTT_BROKER = "134.169.117.5"
MQTT_PORT = 1883

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

def main():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    topic = f"robots/{ROBOT_ID}/{ROLE}"  

    while True:
        try:
            data = {
                "id": ROBOT_ID,
                "role": ROLE,
                "device_type": DEVICE_TYPE,
                "device_name": DEVICE_NAME,
                "ip_address": get_ip(),
                "status": "",  # Not applicable for active
                "dominance": DOMINANCE,
                "decision": DECISION  
            }

            client.publish(topic, json.dumps(data))
            print(f"Published to {topic}: {data}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.5)  

if __name__ == "__main__":
    main()
