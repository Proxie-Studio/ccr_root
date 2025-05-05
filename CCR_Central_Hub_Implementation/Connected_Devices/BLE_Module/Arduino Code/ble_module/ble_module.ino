#include "BLEDevice.h"
#include "BLEUtils.h"
#include "BLEBeacon.h"
#include "BLEAdvertising.h"

// Define iBeacon parameters
#define BEACON_UUID "8ec76ea3-6668-48da-9866-75be8bc86f4d"
#define MANUFACTURER_ID 0x4C00  // Apple's ID for iBeacon

BLEAdvertising* pAdvertising;
uint16_t beaconMajor = 1;    // Major value - can be used to group beacons
uint16_t beaconMinor = 0;    // Minor value - used for individual beacon ID
int8_t measuredPower = -59;  // Power value at 1m distance (calibrated RSSI)

void setup() {
  Serial.begin(115200);
  Serial.println("Starting ESP32 iBeacon...");

  // Initialize BLE
  BLEDevice::init("ESP32_BEACON");

  // Create advertising object
  pAdvertising = BLEDevice::getAdvertising();

  // Setup advertising
  setupAdvertising();

  // Start advertising
  pAdvertising->start();
  Serial.println("iBeacon broadcasting started");
}

void setupAdvertising() {
  // Create iBeacon data structure
  BLEBeacon oBeacon = BLEBeacon();
  oBeacon.setManufacturerId(MANUFACTURER_ID);
  oBeacon.setProximityUUID(BLEUUID(BEACON_UUID));
  oBeacon.setMajor(beaconMajor);
  oBeacon.setMinor(beaconMinor);
  oBeacon.setSignalPower(measuredPower);

  // Create advertisement data
  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();

  // Set flags in advertisement data
  oAdvertisementData.setFlags(0x04);  // BR/EDR not supported

  // Get beacon data and convert to Arduino String
  String strBeacon = oBeacon.getData();

  // Set manufacturer data
  oAdvertisementData.setManufacturerData(strBeacon);

  // Set advertisement data
  pAdvertising->setAdvertisementData(oAdvertisementData);

  // Make it non-connectable
  pAdvertising->setAdvertisementType(ADV_TYPE_NONCONN_IND);

  // Set advertising interval
  pAdvertising->setMinInterval(0x20);  // 20ms
  pAdvertising->setMaxInterval(0x40);  // 40ms
}

void loop() {
  // Read serial input for minor value
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    inputString.trim();  // Remove any leading/trailing whitespace

    // Attempt to convert the input to an integer
    int inputValue = inputString.toInt();

    // Check if the conversion was successful and the value is within the valid range
    if (inputValue >= 0 && inputValue <= 65535) {
      beaconMinor = (uint16_t)inputValue;  // Update the beaconMinor value
      Serial.print("Received new minor value: ");
      Serial.println(beaconMinor);
    } else {
      Serial.println("Invalid input. Please enter a number between 0 and 65535.");
    }
  }

  // Update advertising data
  setupAdvertising();

  // Restart advertising to refresh data
  pAdvertising->stop();
  pAdvertising->start();

  Serial.printf("Broadcasting iBeacon - Major: %d, Minor: %d\n", beaconMajor, beaconMinor);

  delay(1000);  // Update every second
}
