/**
 * @file main.cpp
 * @brief Fichier principal pour la gestion des lecteurs RFID MFRC522 avec ESP32 en tant qu'esclave I2C.
 * @author Adam Dubois
 * @date 2026-02-05
 * @version 1.0
 * 
 * Ce code initialise plusieurs lecteurs RFID MFRC522 connectés à un ESP32 configuré en tant qu'esclave I2C.
 * Lorsqu'une demande est reçue du maître I2C, l'ESP32 scanne les lecteurs RFID, lit les UIDs des cartes présentes,
 * et envoie les données formatées en JSON au maître.
 * 
 * La configuration des broches et des paramètres se trouve dans le fichier config.h. (include/config.h)
 */



// ============================================================================================================
// Includes
// ============================================================================================================
#include <config.h> //Fichier de configuration des broches et paramètres (inclut les bibliothèques nécessaires)



// ============================================================================================================
// Variables globales
// ============================================================================================================
//Créer les instances MFRC522 pour chaque lecteur
MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instance.

//Strings contenant les UID des cartes lues
String g_uidReaders[NR_OF_READERS] = {"NONE", "NONE", "NONE", "NONE"}; // UIDs des cartes lues

// Instance de la classe Simple_Neo pour gérer la LED de débogage
Debug_Neo Neo;

// Définition du tableau ssPins
byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN};



// ============================================================================================================
// Déclarations des fonctions
// ============================================================================================================

void initSerial();
void initI2C();
void initSPI();
void onRequest();
void resetUIDs();
void scanReaders();
String getUIDsAsString(byte *buffer, byte bufferSize);
String formatDataAsJSON();



// ============================================================================================================
// Setup et Loop
// ============================================================================================================
/*
Brief : Initialisation de l'ESP32 en tant qu'esclave I2C et des lecteurs RFID MFRC522.
*/
void setup() {
  initSerial();

  debug("\n");
  debug("Initialisation de l'ESP32 %s...\n", ESP32_NAME.c_str());

  initI2C(); // Initialiser l'I2C en tant qu'esclave

  debug("I2C slave initialized with address 0x%02X\n", SLAVE_ADDR);

  initSPI(); // Initialiser le SPI pour les lecteurs RFID

  Neo.init(); // Initialiser les LEDs NeoPixel

  debug("Initialisation terminée. En attente des demandes du maître I2C...\n");
}

/*
Brief : Boucle principale vide, car l'ESP32 agit en tant qu'esclave I2C.
*/
void loop(){}



// ============================================================================================================
// Définitions des fonctions
// ============================================================================================================

/*
Brief : Initialise le port série pour le débogage si le mode de débogage est activé dans config.h.
*/
void initSerial()
{
  if (DEBUG_MODE)
  {
    Serial.begin(9600);
    while (!Serial); // Attendre que le port série soit prêt
    delay(1000); // Attendre un moment pour s'assurer que tout les caractères de démarrage sont envoyés avant d'afficher les logs de débogage (peut être retirer pour un démarrage plus rapide)
  }
}

/*
Brief : Initialise l'ESP32 en tant qu'esclave I2C avec l'adresse définie dans config.h et 
configure la fonction de rappel pour les demandes du maître.
*/
void initI2C()
{
  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);
  Wire.onRequest(onRequest); // Définir la fonction de rappel pour les demandes du maître
}

/*
Brief : Initialise le SPI pour les lecteurs RFID MFRC522 et configure chaque lecteur avec les broches définies dans config.h.
*/
void initSPI()
{
  // Initialiser SPI matériel avec broches compatibles ESP32-C3
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, -1); // -1: pas de SS global

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) { // Initialisation de chaque lecteur MFRC522
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Utilise la signature compatible
    
    if (DEBUG_MODE)
    {
      Serial.print(F("[DEBUG] Reader "));
      Serial.print(reader);
      Serial.print(F(" initialized : "));
      mfrc522[reader].PCD_DumpVersionToSerial();
    }
  }
}

/*
Brief : Fonction de rappel appelée lorsqu'une demande est reçue du maître I2C.
Scanne les lecteurs RFID, lit les UIDs des cartes, et envoie les données formatées en JSON au maître.
*/
void onRequest() {
  Neo.working(); // Indiquer que le système est en train de travailler

  String jsonData = ""; // String pour stocker les données JSON à envoyer

  debug("Maître a demandé les données.\n");

  resetUIDs();

  scanReaders();

  jsonData = formatDataAsJSON();

  Wire.write(jsonData.c_str()); // Envoyer les données lues
  Wire.write((uint8_t)0x00); // Indicateur de fin de message

  debug("Données envoyées au maître.\n");
  Neo.success(); // Indiquer que les données ont été envoyées avec succès
  //delay(50); // Petite pause pour laisser le temps au maître de lire les données
  Neo.waiting(); // Revenir à l'état d'attente
  //delay(50); // Petite pause pour éviter les rebonds
}

/*
Brief : Réinitialise les UIDs des lecteurs RFID à "NONE".
*/
void resetUIDs() {
  for (int i = 0; i < NR_OF_READERS; i++) {
    g_uidReaders[i] = "NONE";
  }
}

/*
Brief : Scanne tous les lecteurs RFID connectés et met à jour les UIDs des cartes lues dans g_uidReaders.
*/
void scanReaders() {
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) { // Parcourir chaque lecteur MFRC522
    debug("Scanning reader %d...\n", reader);
    // Wake up ALL cards (including halted ones)
    byte bufferATQA[2];
    byte bufferSize = sizeof(bufferATQA);
    MFRC522::StatusCode status = mfrc522[reader].PICC_WakeupA(bufferATQA, &bufferSize); // Wake up cards
    
    if (status == MFRC522::STATUS_OK) { // If a card is found
      if (mfrc522[reader].PICC_ReadCardSerial()) { // Read the card serial number
        g_uidReaders[reader] = getUIDsAsString(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size); // Convert UID to string

        // Halt PICC
        mfrc522[reader].PICC_HaltA();
        // Stop encryption on PCD
        mfrc522[reader].PCD_StopCrypto1();
      }
    }

    debug("Reader %d, Card UID: %s\n", reader, g_uidReaders[reader].c_str());
  }
}

/*
Brief : Convertit un tableau d'octets représentant un UID en une chaîne hexadécimale.

Paramètres :
  - buffer : Pointeur vers le tableau d'octets de l'UID.
  - bufferSize : Taille du tableau d'octets.

Retour : Chaîne hexadécimale représentant l'UID.
*/
String getUIDsAsString(byte *buffer, byte bufferSize) {
  String uidString = ""; // Initialiser une chaîne vide pour l'UID
  for (byte i = 0; i < bufferSize; i++) { // Parcourir chaque octet de l'UID
    uidString += String(buffer[i] < 0x10 ? "0" : ""); // Ajouter un zéro en tête si nécessaire
    uidString += String(buffer[i], HEX); // Ajouter l'octet en hexadécimal
  }
  uidString.toUpperCase(); // Convertir la chaîne en majuscules
  return uidString;
}

/*
Brief : Formate les données des lecteurs RFID en une chaîne JSON.
Retour : Chaîne JSON contenant le nom de l'ESP32 et les UIDs des lecteurs RFID.
*/
String formatDataAsJSON() {
  String jsonString = "{N:\"" + ESP32_NAME + "\","; // Réinitialiser la chaîne avec le nom de l'ESP32

  for (int i = 0; i < NR_OF_READERS; i++) {
    jsonString += "R" + String(i) + ":\"" + g_uidReaders[i] + "\"";
    if (i < NR_OF_READERS - 1) {
      jsonString += ",";
    }
  }
  jsonString += "}";

  return jsonString;
}