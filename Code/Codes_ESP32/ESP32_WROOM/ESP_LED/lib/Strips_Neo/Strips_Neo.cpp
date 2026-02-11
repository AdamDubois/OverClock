#include <Arduino.h>
#include "config.h" //Fichier de configuration des broches et paramètres (inclut les bibliothèques nécessaires)
#include "Strips_Neo.h"

void Strips_Neo::init() {
    strips[0] = Adafruit_NeoPixel(Neo1_COUNT, Neo1_PIN, NEO_GRB + NEO_KHZ800);
    strips[1] = Adafruit_NeoPixel(Neo2_COUNT, Neo2_PIN, NEO_GRB + NEO_KHZ800);
    strips[2] = Adafruit_NeoPixel(Neo3_COUNT, Neo3_PIN, NEO_GRB + NEO_KHZ800);
    strips[3] = Adafruit_NeoPixel(Neo4_COUNT, Neo4_PIN, NEO_GRB + NEO_KHZ800);
    strips[4] = Adafruit_NeoPixel(Neo5_COUNT, Neo5_PIN, NEO_GRB + NEO_KHZ800);
    strips[5] = Adafruit_NeoPixel(Neo6_COUNT, Neo6_PIN, NEO_GRB + NEO_KHZ800);
    strips[6] = Adafruit_NeoPixel(Neo7_COUNT, Neo7_PIN, NEO_GRB + NEO_KHZ800);

    for (uint8_t i = 0; i < NB_STRIPS; i++) {
        strips[i].begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
        strips[i].show();            // Turn OFF all pixels ASAP
        strips[i].setBrightness(50); // Set BRIGHTNESS to about 1/5 (max = 255)
    }
}