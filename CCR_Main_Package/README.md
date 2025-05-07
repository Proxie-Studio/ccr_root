# Turtlebot MQTT Dashboard Integration

This README provides a step-by-step guide for setting up a real-time MQTT-based dashboard for multiple TurtleBots using Python, Mosquitto, systemd, and a live web interface.

---

## 1. MQTT Broker Setup (Ubuntu Host Machine)

### Install Mosquitto Broker

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

### Configure Mosquitto to Enable WebSocket Support

Open the Mosquitto configuration file:

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Replace all existing contents with the following configuration:

```
pid_file /var/run/mosquitto.pid
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
allow_anonymous true

listener 1883

listener 9001
protocol websockets

include_dir /etc/mosquitto/conf.d
```

Restart and enable Mosquitto to apply the changes:

```bash
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto
```

---

## 2. Python MQTT Publisher Script (TurtleBot Side)

Install `paho-mqtt`:

```bash
pip install paho-mqtt
```

### Select and Place the Appropriate Publisher Script

Choose the correct script from the repository based on the device type and its behavioral role (Passive, Active, or Active+Passive), and place it at:

```python
/home/ubuntu/mqtt_scripts/mqtt_publisher.py
```

---

## 3. Auto-Start the Publisher with systemd (TurtleBot Side)

### Create Service File

```bash
sudo nano /etc/systemd/system/mqtt_publisher.service
```

Paste the following:

```
[Unit]
Description=MQTT Publisher Script for TurtleBot
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/python3 /home/ubuntu/mqtt_scripts/mqtt_publisher.py
WorkingDirectory=/home/ubuntu/mqtt_scripts
Restart=always
User=ubuntu
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable mqtt_publisher.service
sudo systemctl start mqtt_publisher.service
```

---

## 4. Automatically Restart on File Change (TurtleBot Side)

### Install inotify-tools

```bash
sudo apt update
sudo apt install inotify-tools
```

### Create Watch Script

```bash
nano ~/mqtt_scripts/watch_mqtt.sh
```

Paste:

```bash
#!/bin/bash

WATCH_FILE="/home/ubuntu/mqtt_scripts/mqtt_publisher.py"
SERVICE_NAME="mqtt_publisher.service"

echo "Watching $WATCH_FILE for changes..."

while true; do
    inotifywait -q -e close_write "$WATCH_FILE"
    echo "Change detected. Restarting $SERVICE_NAME..."
    systemctl restart $SERVICE_NAME || echo "Failed to restart $SERVICE_NAME" >&2
    sleep 1
done
```

Make it executable:

```bash
chmod +x ~/mqtt_scripts/watch_mqtt.sh
```

### Auto-Start the Watcher Script

```bash
sudo nano /etc/systemd/system/watch_mqtt.service
```

Paste

```bash
[Unit]
Description=Watch mqtt_publisher.py for changes & restart service
After=network.target

[Service]
ExecStart=/home/ubuntu/mqtt_scripts/watch_mqtt.sh
WorkingDirectory=/home/ubuntu/mqtt_scripts
Restart=always
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Run this command to verify:

```bash
./mqtt_scripts/watch_mqtt.sh
```

Make it executable:

```bash
chmod +x /home/ubuntu/mqtt_scripts/watch_mqtt.sh
```

Enable and start:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable watch_mqtt.service
sudo systemctl start watch_mqtt.service
```

---

## 5. Dashboard: Real-Time Web View (Ubuntu Host Machine)

To visualize real-time robot data via MQTT, use the HTML dashboard provided in the repository.
File: mqtt_dashboard.html

Open this file in a web browser on your host machine to view live data from all devices (Passive, Active, or both). The dashboard automatically subscribes to relevant MQTT topics and updates the view dynamically. The dashboard groups devices by ID, shows beliefs from Passive devices, decisions from Active devices, and highlights status and update timestamps. Make sure your MQTT broker supports WebSocket (ws://) connections and that the dashboard is updated with the correct IP and port (default is ws://134.169.117.5:9001).

---