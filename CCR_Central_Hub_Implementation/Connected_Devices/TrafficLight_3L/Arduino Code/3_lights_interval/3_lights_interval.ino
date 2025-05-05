#include <Adafruit_NeoPixel.h>

#define RED_PIN D8    // Pin for red LEDs
#define YELLOW_PIN D4 // Pin for yellow LEDs
#define GREEN_PIN D5  // Pin for green LEDs
#define NUMPIXELS 9   // Number of LEDs in each strip
#define INTERVAL 5000 // 5 seconds (5000 milliseconds) interval

// Create NeoPixel objects
Adafruit_NeoPixel redPixels(NUMPIXELS, RED_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel yellowPixels(NUMPIXELS, YELLOW_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenPixels(NUMPIXELS, GREEN_PIN, NEO_GRB + NEO_KHZ800);

// Color definitions
uint32_t RED = redPixels.Color(255, 0, 0);
uint32_t YELLOW = yellowPixels.Color(255, 255, 0);
uint32_t GREEN = greenPixels.Color(0, 255, 0);
uint32_t OFF = redPixels.Color(0, 0, 0);

void setup() {
  Serial.begin(115200);
  redPixels.begin();
  yellowPixels.begin();
  greenPixels.begin();
  clearAll(); // Start with all lights off
}

void loop() {
  Serial.println("red");
  setRed();
  delay(INTERVAL);
  
  Serial.println("yellow");
  setYellow();
  delay(INTERVAL / 2);
  
  Serial.println("green");
  setGreen();
  delay(INTERVAL);
}

// Function to turn on red light and turn off others
void setRed() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, RED);
    yellowPixels.setPixelColor(i, OFF);
    greenPixels.setPixelColor(i, OFF);
  }
  redPixels.show();
  yellowPixels.show();
  greenPixels.show();
}

// Function to turn on yellow light and turn off others
void setYellow() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, OFF);
    yellowPixels.setPixelColor(i, YELLOW);
    greenPixels.setPixelColor(i, OFF);
  }
  redPixels.show();
  yellowPixels.show();
  greenPixels.show();
}

// Function to turn on green light and turn off others
void setGreen() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, OFF);
    yellowPixels.setPixelColor(i, OFF);
    greenPixels.setPixelColor(i, GREEN);
  }
  redPixels.show();
  yellowPixels.show();
  greenPixels.show();
}

// Function to turn off all LEDs
void clearAll() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, OFF);
    yellowPixels.setPixelColor(i, OFF);
    greenPixels.setPixelColor(i, OFF);
  }
  redPixels.show();
  yellowPixels.show();
  greenPixels.show();
}
