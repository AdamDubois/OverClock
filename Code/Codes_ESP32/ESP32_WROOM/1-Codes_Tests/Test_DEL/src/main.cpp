#include <FastLED.h>

// Configuration de la seule bande conservée
#define LED1_PIN      9
#define LED1_COUNT    50

#define LED2_PIN      10
#define LED2_COUNT    50

#define LED3_PIN      5
#define LED3_COUNT    50

#define LED4_PIN      4
#define LED4_COUNT    50

#define LED5_PIN      3
#define LED5_COUNT    60


CRGB leds1[LED1_COUNT];
CRGB leds2[LED2_COUNT];
CRGB leds3[LED3_COUNT];
CRGB leds4[LED4_COUNT];
CRGB leds5[LED5_COUNT];

void setup() {
  FastLED.addLeds<WS2815, LED1_PIN, GRB>(leds1, LED1_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED2_PIN, GRB>(leds2, LED2_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED3_PIN, GRB>(leds3, LED3_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED4_PIN, GRB>(leds4, LED4_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED5_PIN, GRB>(leds5, LED5_COUNT);  // WS2815, ordre GRB standard
  FastLED.setBrightness(255);  // 0-255, ajuste selon ton alimentation
  FastLED.clear();
  FastLED.show();
}

void loop() {
  fill_solid(leds1, LED1_COUNT, CRGB::White);  // Allume en blanc
  fill_solid(leds2, LED2_COUNT, CRGB::White);    // Allume en blanc
  fill_solid(leds3, LED3_COUNT, CRGB::White);    // Allume en blanc
  fill_solid(leds4, LED4_COUNT, CRGB::White);    // Allume en blanc
  fill_solid(leds5, LED5_COUNT, CRGB::White);    // Allume en blanc

  FastLED.show();
}