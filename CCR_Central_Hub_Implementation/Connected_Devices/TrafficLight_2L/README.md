# TrafficLight_2L

This project simulates a two-light traffic signal (Red and Green) using an ESP board and a Python-based graphical user interface (GUI). The lights are controlled over a serial connection using buttons in the GUI.

## Components

- XIAO_ESP32S3 board
- USB cable for serial connection
- Computer with Arduino IDE and Python installed

## Part 1: Arduino Code - `traffic_2_lights.ino`

### Requirements

- **Board:** XIAO_ESP32S3
- **Library:** `Adafruit NeoPixel`

### Installation Steps

1. Open the Arduino IDE.
2. Add ESP32 board support using this URL in **File > Preferences > Additional Boards Manager URLs**:
3. Install the **esp32** platform from **Tools > Board > Boards Manager**.
4. Select **XIAO_ESP32S3** as the board.
5. Install the `Adafruit NeoPixel` library via **Sketch > Include Library > Manage Libraries**.
6. Open `traffic_2_lights.ino` and upload it to the board.

### Pin Configuration

- `D6` — Red NeoPixel strip
- `D7` — Green NeoPixel strip

## Part 2: Python GUI - `Two lights simulation code`

### Description

This Python program provides a GUI to:

- Run the Python script
- Select the correct serial COM port
- Connect/disconnect to the Arduino
- Control red and green lights using buttons
- Visually reflect the active light state on screen