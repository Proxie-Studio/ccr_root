#include <Adafruit_NeoPixel.h>

#define RED_PIN D6    // Pin for red LEDs
#define GREEN_PIN D7  // Pin for green LEDs
#define NUMPIXELS 9   // Number of LEDs in each strip

// Create two NeoPixel objects
Adafruit_NeoPixel redPixels(NUMPIXELS, RED_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenPixels(NUMPIXELS, GREEN_PIN, NEO_GRB + NEO_KHZ800);

// Color definitions
uint32_t RED = redPixels.Color(255, 0, 0);    // Pure red
uint32_t GREEN = greenPixels.Color(0, 255, 0); // Pure green
uint32_t OFF = redPixels.Color(0, 0, 0);      // Lights off

// Variable to track current state
char currentState = 'o';  // 'o' for off, 'r' for red, 'g' for green

void setup() {
  Serial.begin(9600);         // Start serial communication
  redPixels.begin();          // Initialize red LED strip
  greenPixels.begin();        // Initialize green LED strip
  
  // Turn off all LEDs initially
  clearAll();
  Serial.println("System started - lights OFF");
}

void loop() {
  // Check if data is available on serial monitor
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming character
    
    // Only process valid commands and if they're different from current state
    if (command != currentState) {
      switch (command) {
        case 'r':                    // If 'r' is received
          setRed();                  // Turn on red light
          currentState = 'r';
          Serial.println("Red Light ON");
          break;
          
        case 'g':                    // If 'g' is received
          setGreen();                // Turn on green light
          currentState = 'g';
          Serial.println("Green Light ON");
          break;
          
        case 'o':                    // If 'o' is received
          clearAll();               // Turn off all lights
          currentState = 'o';
          Serial.println("Lights OFF");
          break;
          
        default:                    // Ignore invalid commands
          Serial.println("Invalid command - use 'r', 'g', or 'o'");
          break;
      }
    }
  }
}

// Function to turn on red light and turn off green
void setRed() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, RED);
    greenPixels.setPixelColor(i, OFF);
  }
  redPixels.show();
  greenPixels.show();
}

// Function to turn on green light and turn off red
void setGreen() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, OFF);
    greenPixels.setPixelColor(i, GREEN);
  }
  redPixels.show();
  greenPixels.show();
}

// Function to turn off all LEDs
void clearAll() {
  for (int i = 0; i < NUMPIXELS; i++) {
    redPixels.setPixelColor(i, OFF);
    greenPixels.setPixelColor(i, OFF);
  }
  redPixels.show();
  greenPixels.show();
}