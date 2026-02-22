/**
 * @file config.h
 * @brief Ce fichier header contient toutes les configurations et définitions des constantes utilisées dans le projet, 
 * telles que les paramètres du NeoPixel, les broches utilisées pour l'I2C et le SPI, les types et noms des entrées/sorties 
 * du MCP23S17, etc. Si vous souhaitez faire des changements dans la configuration du projet, c'est dans ce fichier que vous 
 * devez les faire. Il est, cependant, important de noter que le PCB a été conçu avec ces paramètres spécifiques, 
 * donc si vous changez les broches ou d'autres paramètres, assurez-vous que votre configuration matérielle correspond 
 * à ces changements pour éviter les conflits et les erreurs. Si vous n'êtes pas sûr de ce que vous faites, il est recommandé 
 * de laisser les paramètres tels quels.
 * @author Adam Dubois
 * @date 2026-02-22
 * @version 1.0
 * 
 * La configuration des broches et des paramètres se trouve dans ce fichier. C'est dans ce fichier que vous devez faire les changements si vous souhaitez ajuster la configuration du projet.
 */

#ifndef CONFIG_H
#define CONFIG_H



// ============================================================================================================
// Includes
// ============================================================================================================

// L'ordre des includes est important, les includes qui en utilisent d'autres doivent être inclus après ceux-ci. Par exemple, Debug_Neo.h doit être inclus après config.h et Adafruit_NeoPixel.h, car il utilise les paramètres définis dans config.h et la bibliothèque Adafruit_NeoPixel.
#include <Arduino.h>
#include <string.h> //Pour la manipulation des strings
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Adafruit_MCP23X17.h> //Bibliothèque pour la gestion du MCP23S17, qui permet d'ajouter des entrées/sorties supplémentaires à l'ESP32
#include <Adafruit_NeoPixel.h> //Bibliothèque pour la gestion du NeoPixel
#include "Debug_Neo.h" // Classe pour gérer les différentes couleurs du NeoPixel en fonction de l'état du système



// ============================================================================================================
// Définitions des constantes et paramètres
// ============================================================================================================

// --------------------------------
// Débogage série
// --------------------------------
// Si le mode de débogage est activé, les logs seront affichés dans le moniteur série.
// Pour activer ou désactiver le mode de débogage, il suffit de changer la valeur de DEBUG_MODE à true ou false.
// La macro debug(...) peut aussi être modifiée pour afficher ce qu'on veut dans le terminal série.
#define DEBUG_MODE true // Mettre à true pour activer les logs série, false pour désactiver

#if DEBUG_MODE == true // Si le mode débogage est activé on définit les macros debug
    #define debug(...) printf("[DEBUG] : " __VA_ARGS__)
#else
    #define debug(...)
#endif

// --------------------------------
// Nom de l'ESP32 esclave
// --------------------------------
// Le nom de l'ESP32 esclave, qui sera envoyé au maître I2C dans la chaîne JSON.
// Peut être changé.
const String ESP32_NAME = "IO";

// --------------------------------
// Néopixel de l'ESP32 esclave
// --------------------------------
// Les paramètres du NeoPixel (broche, nombre de LEDs, couleurs pour les différents états, etc.) sont définis ici.
// Le numéro de broche et le nombre de NeoPixels ne devrait pas être changé, il s'agit de la façon dont le ESP32-C3-WROOM-02 est câblé. 
// Cependant, les couleurs pour les différents états peuvent être changées en modifiant les valeurs de NEOPIXEL_COLOR_WAITING, NEOPIXEL_COLOR_WORKING, NEOPIXEL_COLOR_SUCCESS, NEOPIXEL_COLOR_ERROR et NEOPIXEL_COLOR_PROBLEM.
#define NEOPIXEL_PIN 8
#define NEOPIXEL_COUNT 1
#define NEOPIXEL_BRIGHTNESS 10 // Valeur de luminosité du NeoPixel (0-255)
#define NEOPIXEL_COLOR_WAITING strip.Color(0, 0, 255) // Bleu pour l'attente
#define NEOPIXEL_COLOR_WORKING strip.Color(255, 0, 255) // Mauve pour le travail
#define NEOPIXEL_COLOR_SUCCESS strip.Color(0, 255, 0) // Vert pour le succès
#define NEOPIXEL_COLOR_ERROR strip.Color(255, 0, 0) // Rouge pour l'erreur
#define NEOPIXEL_COLOR_PROBLEM strip.Color(255, 255, 0) // Jaune pour les problèmes

#if (NEOPIXEL_PIN != 8)
    #error "Le numéro de broche du NeoPixel doit être égal à 8, car il s'agit de la configuration matérielle de l'ESP32-C3-WROOM-02. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif
#if (NEOPIXEL_COUNT != 1)
    #error "Le nombre de NeoPixels devrait être égal à 1, car il s'agit de la configuration matérielle de l'ESP32-C3-WROOM-02. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif

// --------------------------------
// Configuration I2C
// --------------------------------
// Les paramètres de l'I2C (adresse de l'esclave, broches SDA et SCL) sont définis ici. 
// Ces paramètres peuvent être changés en fonction de la configuration matérielle et 
// des besoins du projet, mais il est important de s'assurer que l'adresse de l'esclave 
// ne rentre pas en conflit avec d'autres périphériques I2C sur le même bus.
// Dans le cas du projet InXtremis, le routage a été fait avec ces broches et cette adresse, 
// donc il est recommandé de les laisser tels quels à moins que vous ne sachiez ce que vous 
// faites et que vous ayez ajusté le routage en conséquence.
#define SLAVE_ADDR  0x10
#define SDA_PIN     6
#define SCL_PIN     7

#if (SLAVE_ADDR != 0x10 || SDA_PIN != 6 || SCL_PIN != 7)
    #error "Attention, vous avez changé les paramètres de l'I2C. Assurez-vous que ces paramètres correspondent à votre configuration matérielle et que l'adresse de l'esclave ne rentre pas en conflit avec d'autres périphériques I2C sur le même bus."
#endif

// --------------------------------
// Configuration SPI
// --------------------------------
// Les paramètres de la communication SPI avec le MCP23S17 sont définis ici.
// Ces paramètres peuvent être changés en fonction de la configuration matérielle et des besoins du projet, 
// mais il est important de s'assurer que les broches utilisées pour le SPI ne rentrent pas en conflit avec 
// d'autres périphériques ou fonctions de l'ESP32, et que les connexions sont faites correctement.
#define SCK_PIN     4
#define MOSI_PIN    10
#define MISO_PIN    5

#if (SCK_PIN != 4 || MOSI_PIN != 10 || MISO_PIN != 5)
    #error "Attention, vous avez changé les paramètres du SPI. Assurez-vous que ces paramètres correspondent à votre configuration matérielle et que les broches utilisées pour le SPI ne rentrent pas en conflit avec d'autres périphériques ou fonctions de l'ESP32."
#endif

// --------------------------------
// Configuration SPI MCP23S17
// --------------------------------
// Les paramètres de contrôle du MCP23S17 (broches de reset et de chip select) sont définis ici.
// Ces paramètres peuvent être changés en fonction de la configuration matérielle et des besoins du projet,
// mais il est important de s'assurer que les connexions sont faites correctement et que les broches utilisées 
// ne rentrent pas en conflit avec d'autres périphériques ou fonctions de l'ESP32.
#define RST_PIN     0
#define CS_PIN      3

#if (RST_PIN != 0 || CS_PIN != 3)
    #error "Attention, vous avez changé les paramètres du MCP23S17. Assurez-vous que ces paramètres correspondent à votre configuration matérielle et que les connexions sont faites correctement."
#endif

// --------------------------------
// Configuration des entrées/sorties du MCP23S17
// --------------------------------
// Le nombre de broches du MCP23S17, ainsi que le nombre d'entrées, de sorties et de broches inutilisées sont définis ici.
// Le type de chaque broche (INPUT, OUTPUT, INPUT_PULLUP ou INPUT_PULLDOWN) est défini dans le tableau TYPE_PIN, et les noms 
// des différentes entrées sont définis dans le tableau NAME_INPUTS.
// Ces paramètres peuvent être changés en fonction de la configuration matérielle et des besoins du projet, 
// mais il est important de s'assurer que le nombre total de broches, d'entrées, de sorties et de broches inutilisées correspond 
// à la réalité, et que les types et les noms des broches sont définis correctement pour éviter les conflits et les erreurs dans le code.
#define NB_PINS 16 // Nombre total de broches du MCP23S17 (Devrait rester à 16 si le mcp n'est pas changé)
#define NB_INPUTS 16 // Nombre total d'entrées (INPUT, INPUT_PULLUP ou INPUT_PULLDOWN) connectées au MCP23S17. Doit être égal au nombre d'éléments dans NAME_INPUTS
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
// Voici le mapping physique des broches du MCP23S17
//      -----
// GPB0-|0 28|-GPA7
// GPB1-|1 27|-GPA6
// GPB2-|2 26|-GPA5
// GPB3-|3 25|-GPA4
// GPB4-|4 24|-GPA3
// GPB5-|5 23|-GPA2
// GPB6-|6 22|-GPA1
// GPB7-|7 21|-GPA0
// ...

// Le type peut être INPUT, OUTPUT, INPUT_PULLUP ou INPUT_PULLDOWN
// Si une broche n'est pas utilisée, elle peut être définie comme -1 ou tout autre valeur qui n'est pas un type valide.
const int TYPE_PIN[] = {
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

static_assert(sizeof(TYPE_PIN)/sizeof(TYPE_PIN[0]) == NB_PINS, "TYPE_PIN doit contenir NB_PINS éléments.");

// Ici, le numéro ou le nom des différents boutons/switches/bananes peut être changé.
// Le nom désigne les noms qui seront utilisés dans la chaîne JSON envoyée au maître I2C, donc ils peuvent aussi être changés. 
// Par exemple, BTN0 pourrait être "StartButton" ou "EmergencyStop"
// L'ordre des éléments dans ce tableau doit correspondre à l'ordre des broches définies dans TYPE_PIN. 
// Par exemple, si GPA0 est défini comme une entrée pour une banane, alors le premier élément de NAME_INPUTS 
// doit être le nom de cette banane.
// Si une broche n'est pas utilisée ou est un OUTPUT, elle ne doit pas être incluse dans ce tableau.
const String NAME_INPUTS[] = {
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

static_assert(sizeof(NAME_INPUTS)/sizeof(NAME_INPUTS[0]) == NB_INPUTS, "NAME_INPUTS doit contenir NB_INPUTS éléments.");

#endif // CONFIG_H