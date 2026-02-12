#include <Arduino.h>
// Controls an LED via an attached button.

// ok to include only the one needed
// both included here to make things simple for example
#include <Adafruit_MCP23X17.h>
#include <SPI.h>

#define LED_PIN 0     // MCP23XXX pin LED is attached to
#define BUTTON_PIN 1  // MCP23XXX pin button is attached to

// only used for SPI
#define CS_PIN 3

#define SCK_PIN 4
#define MOSI_PIN 10
#define MISO_PIN 5
#define RST_PIN 0

Adafruit_MCP23X17 mcp;
//SPIClass spi;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  delay(1000);
  Serial.println();
  Serial.println("MCP23xxx Combo Test!");
  
  //spi.begin(SCK_PIN, MISO_PIN, MOSI_PIN, CS_PIN);

  //if (!mcp.begin_SPI(CS_PIN, &spi)) {
  if (!mcp.begin_SPI(CS_PIN)) {
    Serial.println("Error.");
    while (1);
  }

  // configure LED pin for output
  mcp.pinMode(LED_PIN, OUTPUT);

  // configure button pin for input with pull up
  mcp.pinMode(BUTTON_PIN, INPUT_PULLUP);

  Serial.println("Looping...");
}

void loop() {
  mcp.digitalWrite(LED_PIN, !mcp.digitalRead(BUTTON_PIN));
}