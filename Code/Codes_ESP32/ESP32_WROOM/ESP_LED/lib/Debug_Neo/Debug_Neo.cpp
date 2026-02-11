#include <Arduino.h>
#include "config.h"
#include "Debug_Neo.h"


void Debug_Neo::init() {
    // Initialisation du NeoPixel
    strip = Adafruit_NeoPixel(NEOPIXEL_COUNT, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
    strip.begin();
    strip.setBrightness(10); // Set brightness to about 1/5 (max = 255)
    strip.show(); // Initialize all pixels to 'off'
}

void Debug_Neo::waiting() {
    // Allume en bleu pour indiquer que le système est en attente
    strip.fill(strip.Color(0, 0, 255)); // Allume en bleu
    strip.show();
}

void Debug_Neo::working() {
    // Allume en mauve pour indiquer que le système est en train de travailler
    strip.fill(strip.Color(255, 0, 255)); // Allume en mauve
    strip.show();
}

void Debug_Neo::success() {
    // Allume en vert pour indiquer un succès
    strip.fill(strip.Color(0, 255, 0)); // Allume en vert
    strip.show();
}

void Debug_Neo::error() {
    // Allume en rouge pour indiquer une erreur
    strip.fill(strip.Color(255, 0, 0)); // Allume en rouge
    strip.show();
}

void Debug_Neo::problem() {
    // Allume en jaune pour indiquer un problème
    strip.fill(strip.Color(255, 255, 0)); // Allume en jaune
    strip.show();
}