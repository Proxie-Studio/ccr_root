# Traffic Light Simulation Application

## Overview
The Traffic Light Simulation application allows for controlling and simulating traffic light states for both vertical and horizontal traffic lights. The application supports controlling traffic lights through ESP32 devices connected via serial communication (COM ports) and offers BLE support for remote output control. Additionally, users can toggle traffic lights manually and apply logic-based control (TW1, TW2, or TW3) based on the input light states.

## Features
- Simulate traffic lights for input (vertical and horizontal) and output (red and green).
- Control lights using a GUI with manual toggles.
- Select COM ports for the traffic lights (input 1, output) and BLE.
- Apply logic-based control (TW1, TW2, TW3) for output light behavior.
- Connect and disconnect devices through the GUI.

## Requirements
- Python 3.x
- `tkinter` for the GUI interface (comes pre-installed with Python).
- `pyserial` for serial communication (`pip install pyserial`).
- ESP32 devices for controlling the traffic lights.
- BLE-enabled device for remote control (optional).

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install required Python libraries:
    ```bash
    pip install pyserial
    ```
3. Connect the ESP32 devices and BLE module to your computer.
4. Run the Python script to launch the application.

## How to Use

### Launch the Application
Run the Python script to start the GUI. The application will open a window with different controls for the traffic lights and logic selection.

### Select COM Ports
- **Input 1**: Select the COM port for the ESP32 connected to the vertical traffic light.
- **Input 2 & 3**: These as input from the user.
- **BLE**: Select the COM port for the BLE device to control the output traffic light remotely.
- **Output**: Select the COM port for the ESP32 connected to the output traffic light.

### Connect to Devices
- Click the **"Connect"** button to establish serial communication with the devices.
- The application will handle the connection and disconnection processes automatically.

### Control Traffic Lights
- **Input Traffic Lights**: Click on the colored circles for the input traffic lights to toggle between red and green.
- **Output Traffic Light**: The output light is automatically controlled based on the selected logic (TW1, TW2, or TW3).

### Select Logic
- Choose one of the available logic options (**TW1**, **TW2**, or **TW3**) from the dropdown menu.
    - **TW1**: If at least one input is red, the output is red. Otherwise, the output is green.
    - **TW2**: If at least two inputs are red, the output is red. Otherwise, the output is green.
    - **TW3**: If all three inputs are red, the output is red. Otherwise, the output is green.

### Disconnect
- Use the **"Disconnect"** button to close the serial connection to the ESP32 devices or BLE device when you're done.

## Troubleshooting
- **No COM ports available**: Ensure that your ESP32 devices and BLE module are properly connected to your computer and recognized by the system.
- **Connection issues**: Ensure the correct COM ports are selected for the devices, and check for any issues with the device drivers.
