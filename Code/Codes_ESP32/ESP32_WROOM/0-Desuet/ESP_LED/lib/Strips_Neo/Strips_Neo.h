#ifndef STRIPS_NEO_H
#define STRIPS_NEO_H

#include "config.h" //Fichier de configuration des broches et paramètres (inclut les bibliothèques nécessaires)

class Strips_Neo {
public:
    Adafruit_NeoPixel strips[NB_STRIPS];

    void init();
    void clearStrips();
    void allRed();
    void allGreen();
    void allBlue();
    void allWhite();
    void allRainbow();
    void waterEffect(uint8_t stripIndex, uint32_t color = 0x0000FF, uint16_t speed = 50);
};

#endif