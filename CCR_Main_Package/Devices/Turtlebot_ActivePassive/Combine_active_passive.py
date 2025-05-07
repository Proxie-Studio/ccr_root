import paho.mqtt.client as mqtt
import serial
import time
import socket
import json
import glob

# ==== Config ====
ROBOT_ID = "INR90"
DEVICE_NAME = "Turtlebot1"
DOMINANCE = 58
DECISION = "Scanning"
MQTT_BROKER = "134.169.117.5"
MQTT_PORT = 1883
BAUD_RATE = 9600

# ==== Helpers ====
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

def find_serial_port():
    ports = glob.glob("/dev/ttyACM0") + glob.glob("/dev/ttyUSB*")
    return ports[0] if ports else None

# ==== Main ====
def main():
    ser = None
    port = find_serial_port()
    if port:
        try:
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            time.sleep(2)  # Let Arduino boot
            print(f"Connected to serial at {port}")
        except Exception as e:
            print(f"Serial connection failed: {e}")

    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    last_passive_publish = 0
    last_active_publish = 0
    passive_interval = 0.3
    active_interval = 0.5

    latest_status = ""

    while True:
        now = time.time()

        # Read from Serial if available (passive)
        if ser and ser.in_waiting:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line in ["Object Detected", "No Object Detected"]:
                    latest_status = line
                    print(f"Sensor: {line}")
            except Exception as e:
                print(f"Serial read error: {e}")

        # Publish passive message if new status or interval passed
        if latest_status and now - last_passive_publish > passive_interval:
            passive_payload = {
                "id": ROBOT_ID,
                "role": "passive",
                "device_type": "Passive",
                "device_name": DEVICE_NAME,
                "ip_address": get_ip(),
                "status": latest_status,
                "dominance": DOMINANCE,
                "decision": "Deciding"
            }
            client.publish(f"robots/{ROBOT_ID}/passive", json.dumps(passive_payload))
            print(f"Published Passive: {passive_payload}")
            last_passive_publish = now

        # Publish active message regularly
        if now - last_active_publish > active_interval:
            active_payload = {
                "id": ROBOT_ID,
                "role": "active",
                "device_type": "Active",
                "device_name": DEVICE_NAME,
                "ip_address": get_ip(),
                "status": "",
                "dominance": DOMINANCE,
                "decision": DECISION
            }
            client.publish(f"robots/{ROBOT_ID}/active", json.dumps(active_payload))
            print(f"Published Active: {active_payload}")
            last_active_publish = now

        time.sleep(0.5)

if __name__ == "__main__":
    main()