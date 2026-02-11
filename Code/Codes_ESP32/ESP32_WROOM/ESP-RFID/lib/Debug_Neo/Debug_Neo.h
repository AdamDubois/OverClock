#ifndef DEBUG_NEO_H
#define DEBUG_NEO_H

class Debug_Neo {
public:
    Adafruit_NeoPixel strip;

    void init();
    void waiting();
    void working();
    void success();
    void error();
    void problem();
};

#endif