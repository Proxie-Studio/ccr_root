
# BLE Module (ble_module.ino)

This Arduino sketch turns an ESP32-based board into a Bluetooth Low Energy (BLE) iBeacon broadcaster using predefined UUID, major, and minor values. The minor value can be dynamically updated via serial input.

## Requirements

- **Board:** XIAO_ESP32S3 (by Seeed Studio)
- **Arduino IDE** installed (version 1.8.x or newer recommended)
- **Libraries:**
  - `ESP32 BLE Arduino` by Neil Kolban and community

## Setup Instructions

### 1. Install Board Support

To add support for the **XIAO_ESP32S3** in the Arduino IDE:

1. Open Arduino IDE.
2. Go to **File > Preferences**.
3. In the **Additional Boards Manager URLs**, add:
4. Go to **Tools > Board > Boards Manager**.
5. Search for **esp32 by Espressif Systems** and install it.
6. Select **XIAO_ESP32S3** under **Tools > Board**.

### 2. Install Required Libraries

In Arduino IDE:

- Go to **Sketch > Include Library > Manage Libraries**
- Search for and install:

- `ESP32 BLE Arduino` (by Neil Kolban, nkolban)

### 3. Upload the Code

1. Connect your **XIAO_ESP32S3** to your computer via USB.
2. Open `ble_module.ino` in Arduino IDE.
3. Select the correct **board** and **port** under **Tools**.
4. Click **Upload**.

## File

- `ble_module.ino`
