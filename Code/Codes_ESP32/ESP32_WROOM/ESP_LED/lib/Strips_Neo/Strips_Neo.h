#ifndef STRIPS_NEO_H
#define STRIPS_NEO_H

#include "config.h" //Fichier de configuration des broches et paramètres (inclut les bibliothèques nécessaires)

class Strips_Neo {
public:
    Adafruit_NeoPixel strips[NB_STRIPS];

    void init();
};

#endif