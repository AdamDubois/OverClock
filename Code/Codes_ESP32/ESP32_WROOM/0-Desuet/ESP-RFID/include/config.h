/**
 * @file config.h
 * @brief Fichier de configuration des broches et paramètres pour la gestion des lecteurs RFID MFRC522 avec ESP32 en tant qu'esclave I2C.
 * @author Adam Dubois
 * @date 2026-02-05
 * @version 1.0
 * 
 * Ce fichier définit les broches utilisées pour la communication I2C et SPI, 
 * ainsi que les paramètres spécifiques aux lecteurs RFID MFRC522.
 * Si vous voulez modifier le nombre de lecteurs ou les broches utilisées, c'est ici que ça se passe.
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
#include <SPI.h> //Bibliothèque SPI pour la communication avec le MFRC522
#include <MFRC522.h> //Bibliothèque MFRC522 pour la gestion du lecteur RFID
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
const String ESP32_NAME = "RFID";

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
#define SLAVE_ADDR  0x11
#define SDA_PIN     6
#define SCL_PIN     7

// --------------------------------
// Configuration SPI
// --------------------------------
#define SCK_PIN     4
#define MOSI_PIN    10
#define MISO_PIN    5

// --------------------------------
// Configuration SPI du MFRC522
// --------------------------------
#define RST_PIN     0

// --------------------------------
// Configuration des lecteurs RFID MFRC522
// --------------------------------
// ==============================================================================================================
// Configuration des broches SS pour les lecteurs RFID
// Les broches SS sont utilisées pour sélectionner le lecteur RFID actif lors de la communication SPI.
// Si vous voulez ajouter ou retirer des lecteurs, modifiez les broches SS ici et ajustez le tableau ssPins en conséquence.
// ===============================================================================================================
#define NR_OF_READERS 4 // Nombre de lecteurs RFID connectés (doit correspondre au nombre de broches SS définies)

#define SS_1_PIN    3
#define SS_2_PIN    1
#define SS_3_PIN    18
#define SS_4_PIN    19

//xtern byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN}; // Tableau des broches SS
extern byte ssPins[]; // Tableau des broches SS
#endif // CONFIG_H