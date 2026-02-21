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

#define NB_PINS 16 // Nombre total de broches du MCP23S17 (Devrait rester à 16 si le mcp n'est pas changé)
#define NB_INPUTS 16 // Nombre total d'entrées
#define NB_OUTPUTS 0 // Nombre total de sorties (Ne font rien nativement dans le code. Si on veut les utiliser, il faudra modifier le code pour les gérer)
#define NB_INUTILISEES 0 // Nombre de broches inutilisées (NB_INPUTS + NB_OUTPUTS + NB_INUTILISEES doit être égal à NB_PINS)

#if (NB_PINS != 16)
    #error "Le nombre de broches du MCP23S17 doit être égal à 16. Si vous utilisez un autre MCP, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif
#if (NB_INPUTS + NB_OUTPUTS + NB_INUTILISEES != NB_PINS)
    #error "Le nombre total d'entrées, de sorties et de broches inutilisées doit être égal au nombre total de broches du MCP23S17."
#endif

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

// Le type peut être INPUT, OUTPUT, INPUT_PULLUP ou INPUT_PULLDOWN
// Si une broche n'est pas utilisée, elle peut être définie comme -1 ou tout autre valeur qui n'est pas un type valide.
int* const TYPE_PIN = new int[NB_PINS] {
    INPUT_PULLUP,  // GPA0
    INPUT_PULLUP,  // GPA1
    INPUT_PULLUP,  // GPA2
    INPUT_PULLUP,  // GPA3
    INPUT_PULLUP,  // GPA4
    INPUT_PULLUP,  // GPA5
    INPUT_PULLUP,  // GPA6
    INPUT_PULLUP,  // GPA7
    INPUT_PULLUP,  // GPB0
    INPUT_PULLUP,  // GPB1
    INPUT_PULLUP,  // GPB2
    INPUT_PULLUP,  // GPB3
    INPUT_PULLUP,  // GPB4
    INPUT_PULLUP,  // GPB5
    INPUT_PULLUP,  // GPB6
    INPUT_PULLUP   // GPB7
};

// Ici, le numéro ou le nom des différents boutons/switches/bananes peut être changé.
// Le nom désigne les noms qui seront utilisés dans la chaîne JSON envoyée au maître I2C, donc ils peuvent aussi être changés. 
// Par exemple, BTN0 pourrait être "StartButton" ou "EmergencyStop"
// L'ordre des éléments dans ce tableau doit correspondre à l'ordre des broches définies dans TYPE_PIN. 
// Par exemple, si GPA0 est défini comme une entrée pour une banane, alors le premier élément de NAME_INPUTS 
// doit être le nom de cette banane.
// Si une broche n'est pas utilisée ou est un OUTPUT, elle ne doit pas être incluse dans ce tableau.
String* const NAME_INPUTS = new String[NB_INPUTS] {
    "BANA0",    // GPA0
    "BANA1",    // GPA1
    "BANA2",    // GPA2
    "BANA3",    // GPA3
    "BANA4",    // GPA4
    "BANA5",    // GPA5
    "BANA6",    // GPA6
    "SW3",      // GPA7
    "BTN2",     // GPB0
    "BTN1",     // GPB1
    "BTN0",     // GPB2
    "BTN3",     // GPB3
    "BTN4",     // GPB4
    "SW0",      // GPB5
    "SW1",      // GPB6
    "SW2"       // GPB7
};

#endif // CONFIG_H