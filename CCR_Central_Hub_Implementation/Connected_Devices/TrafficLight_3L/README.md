# 3-Traffic-Light Simulation with XIAO ESP32S3

This project simulates a traffic light system using three colors (Red, Yellow, Green) and allows both **automated cycling** and **manual control via a Python GUI**.

## Contents

- `traffic_3_lights.ino` — Arduino code to control lights via serial commands
- `3_lights_interval.ino` — Arduino code for automated cycling of lights with intervals
- `Three lights simulation code` — Python GUI to interact with the lights manually

## Hardware Requirements

- Seeed XIAO ESP32S3 board
- 3 sets of NeoPixel LED strips (Red, Yellow, Green)
- External power (if needed for LED strips)
- USB connection to host computer

---

## Arduino Setup

### Board & Library Installation

1. Open **Arduino IDE**.
2. Go to `Tools > Board > Boards Manager`, search for `ESP32`, and install it.
3. Select `Seeed XIAO ESP32S3` under `Tools > Board`.
4. Install the NeoPixel library:
   - Go to `Sketch > Include Library > Manage Libraries`
   - Search for and install **Adafruit NeoPixel**

---

## 1. `traffic_3_lights.ino` – Serial-Controlled Lights

This sketch waits for serial commands:
- `'r'` — turn on red light
- `'y'` — turn on yellow light
- `'g'` — turn on green light
- `'o'` — turn off all lights

**Usage:**
- Upload the sketch to your XIAO ESP32S3
- Open Serial Monitor and send the commands manually
- Alternatively, use the Python GUI (below)

---

## 2. `3_lights_interval.ino` – Automatic Cycling Mode

This sketch automatically cycles the traffic lights:
- Red for 5 seconds
- Yellow for 2.5 seconds
- Green for 5 seconds

---

## 3. Python UI – Manual Light Control

File: `Three lights simulation code`

This is a Python program with a graphical interface to control the traffic lights.

### Features

- Run the python script
- UI displays red, yellow, and green light indicators
- Click buttons or light icons to send commands to the Arduino
- Select and connect to COM port easily
- Real-time interaction