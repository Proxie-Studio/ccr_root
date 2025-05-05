#include <Adafruit_NeoPixel.h>

#define RED_PIN D8     // Pin for red LEDs
#define YELLOW_PIN D4  // Pin for yellow LEDs
#define GREEN_PIN D5   // Pin for green LEDs
#define NUMPIXELS 9    // Number of LEDs in each strip

// Create NeoPixel objects
Adafruit_NeoPixel redPixels(NUMPIXELS, RED_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel yellowPixels(NUMPIXELS, YELLOW_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenPixels(NUMPIXELS, GREEN_PIN, NEO_GRB + NEO_KHZ800);

// Color definitions
uint32_t RED = redPixels.Color(255, 0, 0);      // Pure red
uint32_t YELLOW = yellowPixels.Color(255, 255, 0); // Pure yellow
uint32_t GREEN = greenPixels.Color(0, 255, 0);   // Pure green
uint32_t OFF = redPixels.Color(0, 0, 0);        // Lights off

// Variable to track current state
char currentState = 'o';  // 'o' for off, 'r' for red, 'y' for yellow, 'g' for green

void setup() {
  Serial.begin(9600);         // Start serial communication
  redPixels.begin();          // Initialize red LED strip
  yellowPixels.begin();       // Initialize yellow LED strip
  greenPixels.begin();        // Initialize green LED strip
  
  // Turn off all LEDs initially
  clearAll();
  Serial.println("System started - lights OFF");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming character
    
    // Only process valid commands and if they're different from the current state
    if (command != currentState) {
      switch (command) {
        case 'r':
          setRed();
          currentState = 'r';
          Serial.println("Red Light ON");
          break;
        
        case 'y':
          setYellow();
          currentState = 'y';
          Serial.println("Yellow Light ON");
          break;
        
        case 'g':
          setGreen();
          currentState = 'g';
          Serial.println("Green Light ON");
          break;
        
        case 'o':
          clearAll();
          currentState = 'o';
          Serial.println("Lights OFF");
          break;
        
        default:
          Serial.println("Invalid command - use 'r', 'y', 'g', or 'o'");
          break;
      }
    }
  }
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
