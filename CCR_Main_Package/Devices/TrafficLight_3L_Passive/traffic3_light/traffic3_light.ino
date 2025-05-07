#include <WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

//LED Config 
#define RED_PIN     D8
#define YELLOW_PIN  D4
#define GREEN_PIN   D5
#define NUMPIXELS   9

//WiFi
const char* SSID         = "Your SSID";
const char* PASS         = "SSID Password";
const char* MQTT_BROKER  = "134.169.117.5"; //your Ubuntu machine IP
const int   MQTT_PORT    = 1883;

const char* ROBOT_ID     = "TL1";
const char* DEVICE_NAME  = "TrafficLight1";
const char* DEVICE_TYPE    = "Passive";     
const int   DOMINANCE      = 10;   

Adafruit_NeoPixel redPixels(NUMPIXELS, RED_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel yellowPixels(NUMPIXELS, YELLOW_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenPixels(NUMPIXELS, GREEN_PIN, NEO_GRB + NEO_KHZ800);

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

enum LightState { RED, YELLOW, GREEN };
LightState currentState = RED;
LightState lastPublishedState = YELLOW; 

unsigned long previousMillis = 0;
unsigned long interval = 5000;  //5 sec 

void setup() {
  Serial.begin(115200);
  redPixels.begin();
  yellowPixels.begin();
  greenPixels.begin();
  clearAll();

  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  reconnectMQTT();
}

void loop() {
  if (!mqtt.connected()) reconnectMQTT();
  mqtt.loop();

  unsigned long now = millis();

  if ((currentState == YELLOW && now - previousMillis >= interval / 2) ||
      (currentState != YELLOW && now - previousMillis >= interval)) {
    
    previousMillis = now;
    switch (currentState) {
      case RED:
        setYellow();
        currentState = YELLOW;
        break;
      case YELLOW:
        setGreen();
        currentState = GREEN;
        break;
      case GREEN:
        setRed();
        currentState = RED;
        break;
    }

    if (currentState == RED || currentState == GREEN) {
      if (currentState != lastPublishedState) {
        publishState(currentState);
        lastPublishedState = currentState;
      }
    }
  }
}

//MQTT
void reconnectMQTT() {
  String clientId = String(ROBOT_ID) + "_client";
  delay(random(200, 1000));
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqtt.connect(clientId.c_str())) {
      Serial.println(" connected.");
    } else {
      Serial.print(".");
      delay(500);
    }
  }
}

void publishState(LightState state) {
  String payload = "{";
  payload += "\"device_type\":\"" + String(DEVICE_TYPE) + "\",";
  payload += "\"device_name\":\"" + String(DEVICE_NAME) + "\",";
  payload += "\"ip_address\":\"" + WiFi.localIP().toString() + "\",";
  payload += "\"dominance\":" + String(DOMINANCE) + ",";
  payload += "\"belief\":\"";
  payload += (state == RED) ? "Red" : "Green";
  payload += "\",";
  payload += "\"id\":\"" + String(ROBOT_ID) + "\"";
  payload += "}";

  String topic = "robots/" + String(ROBOT_ID) + "/data";
  mqtt.publish(topic.c_str(), payload.c_str());
  Serial.println("Published: " + payload);
}

void setRed() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, redPixels.Color(255, 0, 0));
    yellowPixels.setPixelColor(i, 0);
    greenPixels.setPixelColor(i, 0);
  }
  redPixels.show(); yellowPixels.show(); greenPixels.show();
  Serial.println("Red");
}

void setYellow() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, 0);
    yellowPixels.setPixelColor(i, yellowPixels.Color(255, 255, 0));
    greenPixels.setPixelColor(i, 0);
  }
  redPixels.show(); yellowPixels.show(); greenPixels.show();
  Serial.println("Yellow");
}

void setGreen() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, 0);
    yellowPixels.setPixelColor(i, 0);
    greenPixels.setPixelColor(i, greenPixels.Color(0, 255, 0));
  }
  redPixels.show(); yellowPixels.show(); greenPixels.show();
  Serial.println("Green");
}

void clearAll() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, 0);
    yellowPixels.setPixelColor(i, 0);
    greenPixels.setPixelColor(i, 0);
  }
  redPixels.show(); yellowPixels.show(); greenPixels.show();
}
