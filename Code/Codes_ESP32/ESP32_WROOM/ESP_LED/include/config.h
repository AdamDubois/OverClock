/**
 * @file config.h
 * @brief Fichier de configuration 
 * @author Adam Dubois
 * @date 2026-02-08
 * @version 1.0
 * 
 * Ce fichier définit les broches utilisées 
 */

#ifndef CONFIG_H
#define CONFIG_H



// ============================================================================================================
// Includes
// ============================================================================================================
#include <Arduino.h>
#include <ArduinoJson.h>
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <string.h> //Pour la manipulation des strings
#include <Adafruit_NeoPixel.h>



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
String const ESP32_NAME = "NEO";



// Configuration I2C
#define SLAVE_ADDR  0x12
#define SDA_PIN     6
#define SCL_PIN     7



// Configuration des NeoPixels
#define NB_STRIPS 7

#define Neo1_PIN 9
#define Neo1_COUNT 40
#define Neo2_PIN 10
#define Neo2_COUNT 40
#define Neo3_PIN 5
#define Neo3_COUNT 40
#define Neo4_PIN 4
#define Neo4_COUNT 40
#define Neo5_PIN 3
#define Neo5_COUNT 40
#define Neo6_PIN 1
#define Neo6_COUNT 9
#define Neo7_PIN 0
#define Neo7_COUNT 256



// Configuration des couleurs
// Table de correspondance entre les noms de couleurs et les codes NeoPixel (à compléter selon les besoins)
struct NamedColor {
  const char* name;
  uint32_t value;
};
const NamedColor color_table[] = {
  { "RED",    Adafruit_NeoPixel::Color(255, 0, 0) },
  { "GREEN",  Adafruit_NeoPixel::Color(0, 255, 0) },
  { "BLUE",   Adafruit_NeoPixel::Color(0, 0, 255) },
  { "YELLOW", Adafruit_NeoPixel::Color(255, 255, 0) },
  { "CYAN",   Adafruit_NeoPixel::Color(0, 255, 255) },
  { "MAGENTA",Adafruit_NeoPixel::Color(255, 0, 255) },
  { "WHITE",  Adafruit_NeoPixel::Color(255, 255, 255) },
  { "BLACK",  Adafruit_NeoPixel::Color(0, 0, 0) },
};
const int NB_COLORS = sizeof(color_table) / sizeof(color_table[0]);

#endif // CONFIG_H