#include <FastLED.h>

// Configuration de la seule bande conservée
#define LED_PIN      9
#define LED_COUNT    1

CRGB leds[LED_COUNT];

void setup() {
  FastLED.addLeds<WS2811, LED_PIN, GRB>(leds, LED_COUNT);  // WS2811, ordre GRB standard
  FastLED.setBrightness(255);  // 0-255, ajuste selon ton alimentation
  FastLED.clear();
  FastLED.show();
}

void loop() {
  leds[0] = CRGB::White;  // Allume la première LED en blanc
  FastLED.show();
}