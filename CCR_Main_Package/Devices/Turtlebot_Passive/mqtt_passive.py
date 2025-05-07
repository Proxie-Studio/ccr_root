import paho.mqtt.client as mqtt
import serial
import time
import socket
import json

# Configurable parameters
ROBOT_ID = "INR90"
ROLE = "passive"  # Changing to passive
DOMINANCE = 56
DECISION = "Deciding"  # No decision yet in passive mode
DEVICE_TYPE = "Passive"
DEVICE_NAME = "Turtlebot1"
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

MQTT_BROKER = "134.169.117.5"  # Update this if needed
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

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Give Arduino time to boot

    topic = f"robots/{ROBOT_ID}/{ROLE}"  # --> publishes to robots/INR90/passive

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line in ["Object Detected", "No Object Detected"]:
                data = {
                    "id": ROBOT_ID,
                    "role": ROLE,  # Update role to passive
                    "device_type": DEVICE_TYPE,
                    "device_name": DEVICE_NAME,
                    "ip_address": get_ip(),
                    "status": line,
                    "dominance": DOMINANCE,
                    "decision": DECISION  # Decision stays the same for passive
                }

                client.publish(topic, json.dumps(data))
                print(f"Published to {topic}: {data}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.5)

if __name__ == "__main__":
    main()
