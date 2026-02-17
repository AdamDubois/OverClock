/**
 * @file config.h
 * @brief 
 * @author Adam Dubois
 * @date 2026-02-05
 * @version 1.0
 * 
 */

#ifndef CONFIG_H
#define CONFIG_H



// ============================================================================================================
// Includes
// ============================================================================================================
#include <Arduino.h>
#include <string.h> //Pour la manipulation des strings
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Adafruit_MCP23X17.h>
#include <Adafruit_NeoPixel.h> //Bibliothèque pour la gestion du NeoPixel



// ============================================================================================================
// Définitions des constantes et paramètres
// ============================================================================================================
// Débogage série
#define DEBUG_MODE true // Mettre à true pour activer les logs série, false pour désactiver

#if DEBUG_MODE == true // Si le mode débogage est activé on définit les macros debug
    #define debug(...) printf("[DEBUG] : " __VA_ARGS__)
#else
    #define debug(...)
#endif

// Nom de l'ESP32 esclave
String const ESP32_NAME = "IO";

// Néopixel de l'ESP32 esclave
#define NEOPIXEL_PIN 8
#define NEOPIXEL_COUNT 1

// Configuration I2C
#define SLAVE_ADDR  0x10
#define SDA_PIN     6
#define SCL_PIN     7

// Configuration SPI
#define SCK_PIN     4
#define MOSI_PIN    10
#define MISO_PIN    5

// Configuration MCP23S17
#define RST_PIN     0
#define CS_PIN      3

// Configuration des numéros de broches pour les différents IO
// MCP23S17 Pin #	Pin Name	Pin ID
// 21	            GPA0	    0
// 22	            GPA1	    1
// 23	            GPA2	    2
// 24	            GPA3	    3
// 25	            GPA4	    4
// 26	            GPA5	    5
// 27	            GPA6	    6
// 28	            GPA7	    7
// 1	            GPB0	    8
// 2	            GPB1	    9
// 3	            GPB2	    10
// 4	            GPB3	    11
// 5	            GPB4	    12
// 6	            GPB5	    13
// 7	            GPB6	    14
// 8	            GPB7	    15
#define SW0_PIN 0
#define SW1_PIN 1
#define SW2_PIN 2
#define SW3_PIN 3

#define BTN0_PIN 4
#define BTN1_PIN 5
#define BTN2_PIN 6
#define BTN3_PIN 7
#define BTN4_PIN 8

#define BANA0_PIN 9
#define BANA1_PIN 10
#define BANA2_PIN 11
#define BANA3_PIN 12
#define BANA4_PIN 13
#define BANA5_PIN 14
#define BANA6_PIN 15

#endif // CONFIG_H