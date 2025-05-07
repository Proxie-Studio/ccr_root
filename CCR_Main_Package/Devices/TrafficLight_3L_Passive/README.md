## Traffic Light (ESP32-Based Passive Device)

This section outlines the setup of a passive traffic light system using an ESP32 and three LED rings. The device simulates a traffic light cycle and periodically publishes its status (belief) to the MQTT broker.

### Device Role

- **Device Name**: `TrafficLight1`
- **Device Type**: `Passive`
- **MQTT Role**: Publishes its current light color as a belief
- **LED Behavior**:
  - Cycles through **Red → Yellow → Green**
  - Reports only **Red** and **Green** states as beliefs
  - Updates every 5 seconds (Yellow light lasts 2.5 seconds)

---

### Hardware Setup

- **Board**: ESP32
- **LEDs**: 3 x Adafruit NeoPixel rings (Red, Yellow, Green)
- **Wiring**:
  - Red Ring connected to GPIO **D8**
  - Yellow Ring connected to GPIO **D4**
  - Green Ring connected to GPIO **D5**

---

### Firmware Upload Instructions

1. Connect the ESP32 to your computer via USB.
2. Open the Arduino sketch located at:
   traffic3_light/traffic3_light.ino
3. Install the following libraries via Arduino Library Manager:
- `WiFi.h`
- `PubSubClient`
- `Adafruit_NeoPixel`
4. In the sketch, update the following:
- Set your WiFi SSID and password
- Set the MQTT broker IP to match your Ubuntu host machine
5. Upload the code to the ESP32.
6. Open the Serial Monitor to confirm:
- Successful WiFi connection
- MQTT connection established
- Publishing data to MQTT topics

---

### Web Dashboard Integration

After uploading the firmware and powering the device, it will automatically appear in the real-time dashboard hosted on your Ubuntu machine:

---
