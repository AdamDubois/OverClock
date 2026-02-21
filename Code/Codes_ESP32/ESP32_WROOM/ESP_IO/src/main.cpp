/**
 * @file main.cpp
 * @brief 
 * @author Adam Dubois
 * @date 2026-02-
 * @version 1.0
 * 
 * 
 * La configuration des broches et des paramètres se trouve dans le fichier config.h. (include/config.h)
 */



// ============================================================================================================
// Includes
// ============================================================================================================
#include "config.h"
#include "Debug_Neo.h"



// ============================================================================================================
// Variables globales
// ============================================================================================================
// Instance de la classe Simple_Neo pour gérer la LED de débogage
Debug_Neo Neo;

// Instance de la classe Adafruit_MCP23X17 pour gérer les entrées/sorties via le MCP23S17
Adafruit_MCP23X17 mcp;



// ============================================================================================================
// Déclarations des fonctions
// ============================================================================================================

void onRequest();
String formatDataAsJSON(int* states);
void initMCP();
int* readAllMCP();



// ============================================================================================================
// Setup et Loop
// ============================================================================================================
/*
Brief : Initialisation de l'ESP32 en tant qu'esclave I2C et des périphériques 
associés (MCP23S17 pour les entrées/sorties, NeoPixel pour le débogage visuel).
*/
void setup() {
  Serial.begin(9600);
  while (!Serial);
  delay(1000);

  debug("\n");
  debug("Initialisation de l'ESP32 IO...\n");

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);
  Wire.onRequest(onRequest); // Définir la fonction de rappel pour les demandes du maître

  debug("I2C slave initialized with address 0x%02X\n", SLAVE_ADDR);


  initMCP();

  Neo.init(); // Initialiser les LEDs NeoPixel
  Neo.waiting(); // Indiquer que le système est en attente

  debug("Looping...\n");
}

/*
Brief : Boucle principale vide, car l'ESP32 agit en tant qu'esclave I2C.
*/
void loop() {}

// ============================================================================================================
// Définitions des fonctions
// ============================================================================================================
/*
Brief : Fonction de rappel appelée lorsqu'une demande est reçue du maître I2C.
Cette fonction lit l'état de tous les boutons/switches/bananes, formate ces données en JSON, et les envoie au maître I2C.
*/
void onRequest() {
  Neo.working(); // Indiquer que le système est en train de travailler

  debug("Maître a demandé les données.\n");

  int* states = readAllMCP(); // Lire l'état de tous les boutons/switches/bananes

  String jsonData = formatDataAsJSON(states); // Formater les données en JSON

  // Envoyer les données JSON au maître I2C
  Wire.write(jsonData.c_str());
  Wire.write(0x00); // Ajouter un caractère de nouvelle ligne pour indiquer la fin des données

  debug("Current states: S0=%d, S1=%d, S2=%d, S3=%d, BTN0=%d, BTN1=%d, BTN2=%d, BTN3=%d, BTN4=%d, BANA0=%d, BANA1=%d, BANA2=%d, BANA3=%d, BANA4=%d, BANA5=%d, BANA6=%d\n",
        states[0], states[1], states[2], states[3],
        states[4], states[5], states[6], states[7], states[8],
        states[9], states[10], states[11], states[12], states[13], states[14], states[15]);
  debug("Données JSON envoyées : %s\n", jsonData.c_str());
  
  Neo.success(); // Indiquer que les données ont été préparées avec succès
  Neo.waiting(); // Revenir à l'état d'attente
}

/*
Brief : Formate les états des boutons, switches et bananes en une chaîne JSON à envoyer au maître I2C.
Paramètres :
- states : Tableau d'entiers représentant l'état de chaque bouton/switch/banane (0 ou 1).
Retour :
- String contenant les données formatées en JSON.
*/
String formatDataAsJSON(int* states) {
  String jsonData = ""; // String pour stocker les données JSON à envoyer

  // Construire la chaîne JSON
  jsonData = "{N:\"" + ESP32_NAME + "\"";
  for (int i = 0; i < 4; i++) {
    jsonData += ",S" + String(i) + ":" + String(states[i]);
  }
  for (int i = 0; i < 5; i++) {
    jsonData += ",BTN" + String(i) + ":" + String(states[4 + i]);
  }
  for (int i = 0; i < 7; i++) {
    jsonData += ",BANA" + String(i) + ":" + String(states[9 + i]);
  }
  jsonData += "}";

  return jsonData;
}

/*
Brief : Initialise les entrées/sorties du MCP23S17 en configurant les broches comme entrées avec pull-up.
*/
void initMCP() {
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

  for (int i = 0; i < NB_PINS; i++)
  {
    mcp.pinMode(i, TYPE_PIN[i]);
  }
  
}

/*
Brief : Lit l'état de tous les boutons/switches/bananes connectés au MCP23S17 et retourne un tableau d'entiers représentant ces états.
Retour :
- Tableau d'entiers où chaque élément correspond à l'état d'un bouton/switch/banane (0 ou 1).
*/
int* readAllMCP() {
  static int states[16];

  for (int i = 0; i < NB_INPUTS; i++) 
  {
    states[i] = mcp.digitalRead(i);
  }

  return states;
}