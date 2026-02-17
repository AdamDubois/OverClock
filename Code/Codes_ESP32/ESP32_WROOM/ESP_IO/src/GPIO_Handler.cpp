#include <Arduino.h>
#include "config.h"
#include "GPIO_Handler.h"

void GPIO_Handler::init() {
    // Reset du MCP23S17
    pinMode(RST_PIN, OUTPUT);
    digitalWrite(RST_PIN, LOW);
    delay(100);
    digitalWrite(RST_PIN, HIGH);

    // Initialisation du MCP23S17
    if (!mcp.begin_SPI(CS_PIN, SCK_PIN, MISO_PIN, MOSI_PIN)) {
        Serial.println("Error initializing MCP23S17.");
        while (1);
    }

    // Configuration des broches du MCP23S17
    mcp.pinMode(SW0_PIN, INPUT_PULLUP); // Configurer le bouton SW0 en entrée avec pull-up
    mcp.pinMode(SW1_PIN, INPUT_PULLUP); // Configurer le bouton SW1 en entrée avec pull-up
    mcp.pinMode(SW2_PIN, INPUT_PULLUP); // Configurer le bouton SW2 en entrée avec pull-up
    mcp.pinMode(SW3_PIN, INPUT_PULLUP); // Configurer le bouton SW3 en entrée avec pull-up

    mcp.pinMode(BTN0_PIN, INPUT_PULLUP); // Configurer le bouton BTN0 en entrée avec pull-up
    mcp.pinMode(BTN1_PIN, INPUT_PULLUP); // Configurer le bouton BTN1 en entrée avec pull-up
    mcp.pinMode(BTN2_PIN, INPUT_PULLUP); // Configurer le bouton BTN2 en entrée avec pull-up
    mcp.pinMode(BTN3_PIN, INPUT_PULLUP); // Configurer le bouton BTN3 en entrée avec pull-up
    mcp.pinMode(BTN4_PIN, INPUT_PULLUP); // Configurer le bouton BTN4 en entrée avec pull-up

    mcp.pinMode(BANA0_PIN, INPUT_PULLUP); // Configurer le bouton BANA0 en entrée avec pull-up
    mcp.pinMode(BANA1_PIN, INPUT_PULLUP); // Configurer le bouton BANA1 en entrée avec pull-up
    mcp.pinMode(BANA2_PIN, INPUT_PULLUP); // Configurer le bouton BANA2 en entrée avec pull-up
    mcp.pinMode(BANA3_PIN, INPUT_PULLUP); // Configurer le bouton BANA3 en entrée avec pull-up
    mcp.pinMode(BANA4_PIN, INPUT_PULLUP); // Configurer le bouton BANA4 en entrée avec pull-up
    mcp.pinMode(BANA5_PIN, INPUT_PULLUP); // Configurer le bouton BANA5 en entrée avec pull-up
    mcp.pinMode(BANA6_PIN, INPUT_PULLUP); // Configurer le bouton BANA6 en entrée avec pull-up
}

int* GPIO_Handler::readAll() {
    static int states[16];
    states[0] = mcp.digitalRead(SW0_PIN);
    states[1] = mcp.digitalRead(SW1_PIN);
    states[2] = mcp.digitalRead(SW2_PIN);
    states[3] = mcp.digitalRead(SW3_PIN);
    states[4] = mcp.digitalRead(BTN0_PIN);
    states[5] = mcp.digitalRead(BTN1_PIN);
    states[6] = mcp.digitalRead(BTN2_PIN);
    states[7] = mcp.digitalRead(BTN3_PIN);
    states[8] = mcp.digitalRead(BTN4_PIN);
    states[9] = mcp.digitalRead(BANA0_PIN);
    states[10] = mcp.digitalRead(BANA1_PIN);
    states[11] = mcp.digitalRead(BANA2_PIN);
    states[12] = mcp.digitalRead(BANA3_PIN);
    states[13] = mcp.digitalRead(BANA4_PIN);
    states[14] = mcp.digitalRead(BANA5_PIN);
    states[15] = mcp.digitalRead(BANA6_PIN);
    return states;
}