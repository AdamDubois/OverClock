#include <FastLED.h>

// Configuration de la seule bande conservée
#define LED_PIN      9
#define LED_COUNT    18

CRGB leds[LED_COUNT];

void setup() {
  FastLED.addLeds<WS2815, LED_PIN, GRB>(leds, LED_COUNT);  // WS2815, ordre GRB standard
  FastLED.setBrightness(255);  // 0-255, ajuste selon ton alimentation
  FastLED.clear();
  FastLED.show();
}

void loop() {
  for (int i = 0; i < LED_COUNT; i++) {
    if (i % 2 == 0) {
      leds[i] = CRGB::Red;  // Allume en rouge
    }
  }
  FastLED.show();
  delay(1000);  // Délai pour voir l'effet

  for (int i = 0; i < LED_COUNT; i++) {
    if (i % 2 == 0) {
      leds[i] = CRGB::Green;  // Allume en vert
      FastLED.show();
      delay(1000);  // Délai pour voir l'effet
    }
  }
}