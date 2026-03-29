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
        strips[i].setBrightness(255); // Set BRIGHTNESS to about 1/5 (max = 255)
    }
}

void Strips_Neo::clearStrips() {
    for (uint8_t i = 0; i < NB_STRIPS; i++) {
        strips[i].clear(); // Clear all pixels
        strips[i].show();  // Update the strip to turn off the pixels
    }
}

void Strips_Neo::allRed() {
    for (uint8_t i = 0; i < NB_STRIPS; i++) {
        strips[i].fill(strips[i].Color(255, 0, 0)); // Fill with red
        strips[i].show();
    }
}

void Strips_Neo::allGreen() {
    for (uint8_t i = 0; i < NB_STRIPS; i++) {
        strips[i].fill(strips[i].Color(0, 255, 0)); // Fill with green
        strips[i].show();
    }
}

void Strips_Neo::allBlue() {
    for (uint8_t i = 0; i < NB_STRIPS; i++) {
        strips[i].fill(strips[i].Color(0, 0, 255)); // Fill with blue
        strips[i].show();
    }
}

void Strips_Neo::allWhite() {
    for (uint8_t i = 0; i < NB_STRIPS; i++) {
        strips[i].fill(strips[i].Color(255, 255, 255)); // Fill with white
        strips[i].show();
    }
}

/*
Brief :  Affiche un effet arc-en-ciel sur tous les strips. Il y a 7 strips de 5 DELs chacun, soit 35 DELs au total. 
L'animation fait défiler les couleurs de l'arc-en-ciel à travers les DELs. La première DELs de la strip 0 commence en rouge, 
la première DELs de la strip 1 commence en orange, etc. jusqu'à la strip 6 qui commence en violet.
*/
void Strips_Neo::allRainbow() {
    // Animation infinie avec effet de vague diagonale
    while (true) {
        for (uint16_t j = 0; j < 256; j++) {
            for (uint8_t i = 0; i < NB_STRIPS; i++) {
                for (uint16_t k = 0; k < strips[i].numPixels(); k++) {
                    // Décalage diagonal : chaque strip commence la vague un peu plus tard
                    // On combine l'indice de la strip et de la LED pour créer l'effet de vague
                    uint16_t diagonal_offset = i * strips[0].numPixels() + k;
                    uint32_t color = strips[i].ColorHSV(((diagonal_offset * 65536L / (NB_STRIPS * strips[0].numPixels())) + j * 65536L / 256) % 65536L);
                    strips[i].setPixelColor(k, color);
                }
                strips[i].show();
            }
        }
    }
}

// Effet d'eau : toute la bande est colorée, une "vague" de dégradé plus clair/foncé se déplace
void Strips_Neo::waterEffect(uint8_t stripIndex, uint32_t color, uint16_t speed) {
    if (stripIndex >= NB_STRIPS) return;
    uint16_t n = strips[stripIndex].numPixels();
    int waveLength = n / 2; // longueur de la vague
    int pos = 0;
    while (true) {
        for (uint16_t k = 0; k < n; k++) {
            // Calculer la position relative à la vague
            float rel = (float)(k - pos);
            // Générer un dégradé sinusoïdal pour simuler la lumière sur l'eau
            float brightness = 0.6f + 0.4f * sinf(2 * 3.14159f * rel / waveLength);
            // Clamp brightness entre 0 et 1
            if (brightness < 0) brightness = 0;
            if (brightness > 1) brightness = 1;
            uint8_t r = ((color >> 16) & 0xFF) * brightness;
            uint8_t g = ((color >> 8) & 0xFF) * brightness;
            uint8_t b = (color & 0xFF) * brightness;
            strips[stripIndex].setPixelColor(k, strips[stripIndex].Color(r, g, b));
        }
        strips[stripIndex].show();
        pos = (pos + 1) % n;
        delay(speed);
    }
}