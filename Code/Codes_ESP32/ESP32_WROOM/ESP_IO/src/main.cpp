#include "config.h"
#include "Debug_Neo.h"
#include "GPIO_Handler.h"

// Instance de la classe Simple_Neo pour gérer la LED de débogage
Debug_Neo Neo;

// Instance de la classe GPIO_Handler pour gérer les entrées/sorties via le MCP23S17
GPIO_Handler EXPANDER;

void onRequest();

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

  debug("\n");
  debug("I2C slave initialized with address 0x%02X\n", SLAVE_ADDR);


  EXPANDER.init(); // Initialiser le MCP23S17

  Neo.init(); // Initialiser les LEDs NeoPixel
  Neo.waiting(); // Indiquer que le système est en attente

  debug("Looping...\n");
}

void loop() {
  int*states = EXPANDER.readAll(); // Lire l'état de tous les boutons/switches
  
}

// ============================================================================================================
// Définitions des fonctions
// ============================================================================================================
/*
Brief : Fonction de rappel appelée lorsqu'une demande est reçue du maître I2C.
*/
void onRequest() {
  Neo.working(); // Indiquer que le système est en train de travailler

  String jsonData = ""; // String pour stocker les données JSON à envoyer

  debug("Maître a demandé les données.\n");

  int* states = EXPANDER.readAll(); // Lire l'état de tous les boutons/switches

  debug("Current states: S0=%d, S1=%d, S2=%d, S3=%d, BTN0=%d, BTN1=%d, BTN2=%d, BTN3=%d, BTN4=%d, BANA0=%d, BANA1=%d, BANA2=%d, BANA3=%d, BANA4=%d, BANA5=%d, BANA6=%d\n",
        states[0], states[1], states[2], states[3],
        states[4], states[5], states[6], states[7], states[8],
        states[9], states[10], states[11], states[12], states[13], states[14], states[15]);

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

  debug("Données JSON à envoyer : %s\n", jsonData.c_str());

  // Envoyer les données JSON au maître I2C
  Wire.write(jsonData.c_str());
  Wire.write(0x00); // Ajouter un caractère de nouvelle ligne pour indiquer la fin des données
  
  Neo.success(); // Indiquer que les données ont été préparées avec succès
  Neo.waiting(); // Revenir à l'état d'attente
}