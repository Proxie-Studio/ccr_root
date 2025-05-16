import paho.mqtt.client as mqtt
import time
import json
import threading

# MQTT Config
MQTT_BROKER = "134.169.115.153"
MQTT_PORT = 1883
COMMAND_TOPIC = "robots/decision/command"

# Decision parameters
CONSENSUS_TIMEOUT = 1.5
CHECK_INTERVAL = 1.0
MOVE_STEPS = 10
CONSENSUS_THRESHOLD = 2

# Global state
device_order = {}
status_map = {}
device_counter = 1

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("robots/+/active")
    client.subscribe("robots/+/passive")
    client.subscribe("robots/+/data")

def on_message(client, userdata, msg):
    global device_counter
    try:
        payload = json.loads(msg.payload.decode())
        device_name = payload.get("device_name")
        status = payload.get("status", "")
        timestamp = time.time()

        if not device_name:
            return

        if device_name not in device_order:
            device_order[device_name] = device_counter
            print(f"Registered {device_name} as #{device_counter}")
            device_counter += 1

        if status:
            status_map[device_name] = {
                "status": status,
                "last_seen": timestamp
            }

    except Exception as e:
        print(f"Error handling message: {e}")

def issue_move_command():
    now = time.time()
    move_payload = {
        "action": "MOVE",
        "steps": MOVE_STEPS,
        "timestamp": now,
        "device_order": [
            {"name": name, "order": order}
            for name, order in sorted(device_order.items(), key=lambda x: x[1])
        ]
    }

    # Broadcast to all robots
    client.publish(COMMAND_TOPIC, json.dumps(move_payload))
    print(f"Move {MOVE_STEPS} steps")

    # Send individual decision updates to active turtlebots
    for name in device_order:
        if "Turtlebot" in name:
            decision_payload = {
                "device_name": name,
                "device_type": "Active",
                "decision": f"MOVE {MOVE_STEPS}",
                "timestamp": now
            }
            client.publish(f"robots/{name}/data", json.dumps(decision_payload))
            print(f"Published decision to {name}: {decision_payload}")

def check_consensus():
    now = time.time()

    if not status_map:
        return

    all_recent = all(
        (now - data["last_seen"] < CONSENSUS_TIMEOUT)
        for data in status_map.values()
    )

    if not all_recent:
        print("Waiting for all devices to report in before checking consensus...")
        return

    no_object_count = sum(
        1 for data in status_map.values()
        if data["status"] == "No Object Detected"
    )

    print(f"[Consensus check] {no_object_count} out of {len(status_map)} say 'No Object Detected'")

    if no_object_count >= CONSENSUS_THRESHOLD:
        issue_move_command()

def start_consensus_loop():
    check_consensus()
    threading.Timer(CHECK_INTERVAL, start_consensus_loop).start()

# Main MQTT setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print("Decision handler running...")
start_consensus_loop()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    client.loop_stop()
    client.disconnect()
