#include <WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

// LED Config
#define RED_PIN    D6
#define GREEN_PIN  D7
#define NUMPIXELS  9

Adafruit_NeoPixel redPixels(NUMPIXELS, RED_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenPixels(NUMPIXELS, GREEN_PIN, NEO_GRB + NEO_KHZ800);

// WiFi Config
const char* SSID        = "Norrspect AI";
const char* PASS        = "norrspect.ai";
const char* MQTT_BROKER = "134.169.117.5";  // your Ubuntu machine IP
const int   MQTT_PORT   = 1883;

const char* ROBOT_ID    = "TL2";
const char* DEVICE_NAME = "TrafficLight2";
const char* DEVICE_TYPE = "Active";
const int   DOMINANCE   = 5;

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

char currentState = 'o';  // o = Off, r = Red, g = Green

void setup() {
  Serial.begin(115200);
  redPixels.begin();
  greenPixels.begin();
  clearAll();

  //WiFi
  WiFi.begin(SSID, PASS);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(200);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());
  
  WiFi.setSleep(false);

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(callback);
  reconnectMQTT();

  publishState();
}

void loop() {
  if (!mqtt.connected()) {
    reconnectMQTT();
  }
  mqtt.loop();

  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == '\n' || cmd == '\r') return;
    if (cmd != currentState) {
      switch (cmd) {
        case 'r':
          setRed();
          currentState = 'r';
          break;
        case 'g':
          setGreen();
          currentState = 'g';
          break;
        case 'o':
          clearAll();
          currentState = 'o';
          break;
        default:
          Serial.println("Unknown command received");
          break;
      }
      publishState();  
    }
  }
}

void reconnectMQTT() {
  String clientId = String(ROBOT_ID) + "_client";
  delay(random(200, 1000));

  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqtt.connect(clientId.c_str())) {
      Serial.println(" connected.");

      mqtt.subscribe(("robots/" + String(ROBOT_ID) + "/controller").c_str());
    } else {
      Serial.print(".");
      delay(500);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  msg.trim();

  //Serial.println("MQTT message received: " + msg);

  if ((msg == "g"   || msg.equalsIgnoreCase("Green")) 
      && currentState != 'g') {
    setGreen();
    currentState = 'g';
    publishState();
  }
  else if ((msg == "r"   || msg.equalsIgnoreCase("Red")) 
           && currentState != 'r') {
    setRed();
    currentState = 'r';
    publishState();
  }
  else if ((msg == "o"   || msg.equalsIgnoreCase("Off")) 
           && currentState != 'o') {
    clearAll();
    currentState = 'o';
    publishState();
  }
}

void publishState() {
  String payload = "{";
  payload += "\"device_type\":\"" + String(DEVICE_TYPE) + "\",";
  payload += "\"device_name\":\"" + String(DEVICE_NAME) + "\",";
  payload += "\"ip_address\":\"" + WiFi.localIP().toString() + "\",";
  payload += "\"dominance\":" + String(DOMINANCE) + ",";
  payload += "\"decision\":\"";
  if (currentState == 'r') payload += "Red";
  else if (currentState == 'g') payload += "Green";
  else payload += "Off";
  payload += "\",";
  payload += "\"id\":\"" + String(ROBOT_ID) + "\"";
  payload += "}";

  String topic = "robots/" + String(ROBOT_ID) + "/data";
  mqtt.publish(topic.c_str(), payload.c_str());

  Serial.println("Published: " + payload);
}

// Set Red LED
void setRed() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, redPixels.Color(255, 0, 0));
    greenPixels.setPixelColor(i, greenPixels.Color(0, 0, 0));
  }
  redPixels.show();
  greenPixels.show();
}

// Set Green LED
void setGreen() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, redPixels.Color(0, 0, 0));
    greenPixels.setPixelColor(i, greenPixels.Color(0, 255, 0));
  }
  redPixels.show();
  greenPixels.show();
}

// Clear all LEDs
void clearAll() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, redPixels.Color(0, 0, 0));
    greenPixels.setPixelColor(i, greenPixels.Color(0, 0, 0));
  }
  redPixels.show();
  greenPixels.show();
}
