import paho.mqtt.client as mqtt
import time
import json
import threading

# MQTT Config
MQTT_BROKER = "134.169.115.164"
MQTT_PORT = 1883
COMMAND_TOPIC = "robots/decision/command"

# Decision parameters
CONSENSUS_TIMEOUT = 1.5  
CHECK_INTERVAL = 1.0    
MOVE_STEPS = 10      # Number of steps
CONSENSUS_THRESHOLD = 2  # number of robots that must say "No Object Detected"

# Global maps
device_order = {}
status_map = {}
device_counter = 1

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("robots/+/active")
    client.subscribe("robots/+/passive")
    client.subscribe("robots/+/data")
    # client.subscribe("robots/Turtlebot1/decision")
    # client.subscribe("robots/Turtlebot2/decision")
    client.subscribe("robots/+/decision")
    print("Subscribed to: robots/+/active, robots/+/passive, robots/+/data, robots/+/decision")

def on_message(client, userdata, msg):
    global device_counter
    try:
        payload = json.loads(msg.payload.decode())
        device_name = payload.get("device_name")
        status = payload.get("status", "")
        timestamp = time.time()
        decision = payload.get("decision")  # Get the decision if it's in the payload

        if not device_name:
            return

        # Assign order on first appearance
        if device_name not in device_order:
            device_order[device_name] = device_counter
            print(f"Registered {device_name} as #{device_counter}")
            device_counter += 1

        # Update status
        if status:
            status_map[device_name] = {
                "status": status,
                "last_seen": timestamp
            }

        # Handle decision messages (for the python script itself)
        if decision and "Turtlebot" in msg.topic:
            print(f"Received decision '{decision}' from {msg.topic}")

    except Exception as e:
        print(f"Error handling message: {e}")

# Movement logic
def issue_move_command():
    move_payload = {
        "action": "MOVE",
        "steps": MOVE_STEPS,
        "timestamp": time.time(),
        "device_order": [
            {"name": name, "order": order}
            for name, order in sorted(device_order.items(), key=lambda x: x[1])
        ]
    }

    client.publish(COMMAND_TOPIC, json.dumps(move_payload))
    print(f"Move {MOVE_STEPS} steps")

    # Publish the decision to the active Turtlebots' decision topic
    for device_name, order in device_order.items():
        if "Turtlebot" in device_name:
            decision_payload = {"device_name": device_name, "decision": f"Move {MOVE_STEPS} steps"}  # Include MOVE_STEPS
            client.publish(f"robots/{device_name}/decision", json.dumps(decision_payload))
            print(f"Published decision 'Move {MOVE_STEPS} steps' to robots/{device_name}/decision")

# Consensus check
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

# Main
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print("Decision handler running...")
start_consensus_loop()

# Keep alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    client.loop_stop()
    client.disconnect()
