#include "config.h"

CRGB leds[NUM_LEDS];

int scrollX = WIDTH;

void setup() {
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(40);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  // static uint8_t frame = 0;
  // static uint32_t last = 0;

  // const uint16_t frameDelayMs = 120;   // Vitesse d'animation (ms par frame)

  // uint32_t now = millis();
  // if (now - last >= frameDelayMs) {
  //   last = now;

  //   drawFrame(leds, help_animation_data[frame]);
  //   FastLED.show();

  //   frame = (frame + 1) % HELP_ANIMATION_FRAME_COUNT;
  // }

// ----------------------------------------------------------------------------------------------------------

  FastLED.clear();

  const char* text = "Tantot c'est les grosses cal*** de queues et les pipes !";
  int textLen = strlen(text);
  int charWidth = 6;  // 5 pixels + 1 espace

  for (int i = 0; i < textLen; i++) {
    int charX = scrollX + i * charWidth;
    int charY = (HEIGHT - 7) / 2;  // Centrage vertical (≈0 ou 1)

    drawChar(leds, charX, charY, text[i], CRGB(255, 0, 0));  // Rouge
  }

  scrollX--;
  if (scrollX < - (textLen * charWidth)) {
    scrollX = WIDTH;
  }

  FastLED.show();
  delay(120);  // Vitesse du défilement (ajustez : 50 = plus rapide, 120 = plus lent)

// ----------------------------------------------------------------------------------------------------------

  // // put your main code here, to run repeatedly:
  // int index_r = 0;
  // int index_g = 0;
  // int index_b = 0;

  // for (index_r = 0 ; index_r < NUM_LEDS + 2; index_r++) {
  //   index_g = index_r - 1;
  //   index_b = index_r - 2;

  //   if (index_g < 0) {
  //     fill_solid(leds, NUM_LEDS, CRGB::Black); // éteint tous les pixels
  //     leds[index_r] = CRGB(255, 0, 0); // rouge
  //     FastLED.show();
  //   }
  //   else if (index_b < 0) {
  //     fill_solid(leds, NUM_LEDS, CRGB::Black); // éteint tous les pixels
  //     leds[index_r] = CRGB(255, 0, 0); // rouge
  //     leds[index_g] = CRGB(0, 255, 0); // vert
  //     FastLED.show();
  //   }
  //   else if (index_g == NUM_LEDS - 1) {
  //     fill_solid(leds, NUM_LEDS, CRGB::Black); // éteint tous les pixels
  //     leds[index_g] = CRGB(0, 255, 0); // vert
  //     leds[index_b] = CRGB(0, 0, 255); // bleu
  //     FastLED.show();
  //   }
  //   else if (index_b == NUM_LEDS - 1) {
  //     fill_solid(leds, NUM_LEDS, CRGB::Black); // éteint tous les pixels
  //     leds[index_b] = CRGB(0, 0, 255); // bleu
  //     FastLED.show();
  //   }
  //   else {
  //     fill_solid(leds, NUM_LEDS, CRGB::Black); // éteint tous les pixels
  //     leds[index_r] = CRGB(255, 0, 0); // rouge
  //     leds[index_g] = CRGB(0, 255, 0); // vert
  //     leds[index_b] = CRGB(0, 0, 255); // bleu
  //     FastLED.show();
  //   }
    
  //   delay(0);
  // }
}