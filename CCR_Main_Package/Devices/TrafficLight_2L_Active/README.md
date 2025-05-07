## Traffic Light (ESP32-Based Active Device)

This section describes how to set up an ESP32-based traffic light with two LED rings. The device connects to the MQTT broker and sends its status to the dashboard in real-time.

### Device Role

- **Device Name**: `TrafficLight2`
- **Device Type**: `Active`
- **MQTT Role**: Publishes traffic light state and responds to control commands
- **LED Behavior**:
  - `g` (Green): Green ring turns ON
  - `r` (Red): Red ring turns ON
  - `o` (Off): Both LED rings turn OFF

---

### Hardware Setup

- **Board**: ESP32
- **LEDs**: 2 x Adafruit NeoPixel rings
- **Wiring**:
  - Red Ring connected to GPIO **D6**
  - Green Ring connected to GPIO **D7**

---

### Firmware Upload Instructions

1. Connect the ESP32 to your computer via USB.
2. Open the Arduino sketch located at:
  traffic2_light/traffic2_light.ino
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