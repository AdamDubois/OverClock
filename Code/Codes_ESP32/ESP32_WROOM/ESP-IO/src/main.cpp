/**
 * @file main.cpp
 * @brief Ce code est destiné à être exécuté sur un ESP32 configuré en tant qu'esclave I2C.
 * Il utilise un MCP23S17 pour lire l'état de 16 boutons/switches/bananes, formate ces données en JSON, 
 * et les envoie à un maître I2C (comme un Raspberry Pi) lorsqu'une demande est reçue.
 * Toutes les différentes parties du code sont séparées en fonctions pour une meilleure lisibilité et maintenabilité.
 * Puisque l'ESP32 agit en tant qu'esclave I2C, la boucle principale (loop) est vide, 
 * tout le travail est effectué dans la fonction de rappel onRequest() qui est appelée lorsqu'une demande est reçue du maître I2C.
 * @author Adam Dubois
 * @date 2026-02-22
 * @version 1.0
 * 
 * La configuration des broches et des paramètres se trouve dans le fichier config.h. (include/config.h)
 */



// ============================================================================================================
// Includes
// ============================================================================================================

#include "config.h" // Fichier de configuration avec les paramètres et les définitions des broches (tous les includes nécessaires sont aussi dans ce fichier)



// ============================================================================================================
// Variables globales
// ============================================================================================================

// JSON à envoyer au maître I2C, construit à partir des données lues sur le MCP23S17
String g_jsonData = "";

// Valeur de l'état de chaque bouton/switch/banane, lue à partir du MCP23S17 et utilisée pour construire le JSON à envoyer au maître I2C
int* g_states = nullptr; // Tableau d'entiers pour stocker les états des boutons/switches/bananes, alloué dynamiquement dans la boucle principale et libéré après utilisation

// Instance de la classe Simple_Neo pour gérer la LED de débogage
Debug_Neo g_Neo;

// Instance de la classe Adafruit_MCP23X17 pour gérer les entrées/sorties via le MCP23S17
Adafruit_MCP23X17 g_Mcp;



// ============================================================================================================
// Déclarations des fonctions
// ============================================================================================================

void initSerial();
void initI2C();
void initMCP();
void onRequest();
int* readAllMCP();
String formatDataAsJSON(int* states);



// ============================================================================================================
// Setup et Loop
// ============================================================================================================

/*
Brief : Initialisation de l'ESP32 en tant qu'esclave I2C et des périphériques 
associés (MCP23S17 pour les entrées/sorties, NeoPixel pour le débogage visuel).
*/
void setup()
{
  initSerial();

  debug("\n");
  debug("Initialisation de l'ESP32 %s...\n", ESP32_NAME.c_str());

  initI2C(); // Initialiser l'I2C en tant qu'esclave

  debug("I2C slave initialized with address 0x%02X\n", SLAVE_ADDR);

  initMCP();

  g_Neo.init(); // Initialiser les LEDs NeoPixel

  debug("Initialisation terminée. En attente des demandes du maître I2C...\n");
}

/*
Brief : Boucle principale vide, car l'ESP32 agit en tant qu'esclave I2C.
*/
void loop(){
  g_states = readAllMCP(); // Lire l'état de tous les boutons/switches/bananes pour éviter les problèmes de timeout dans la fonction onRequest() (si on lit les données dans onRequest(), il peut arriver que le maître I2C attende trop longtemps et que la communication échoue)
  g_jsonData = formatDataAsJSON(g_states); // Mettre à jour les données JSON globales pour qu'elles soient prêtes à être envoyées lorsque le maître I2C fera une demande
  delete[] g_states; // Libérer la mémoire allouée pour les états

  delay(100); // Attendre un moment avant de lire à nouveau les données du MCP23S17 pour éviter de surcharger le bus I2C et le processeur de l'ESP32
}

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
Brief : Initialise les entrées/sorties du MCP23S17 en fonction de la configuration définie dans config.h.
Cette fonction effectue également un reset du MCP23S17 pour s'assurer qu'il démarre dans un état connu.
*/
void initMCP()
{
  // Reset du MCP23S17
  pinMode(RST_PIN, OUTPUT);
  digitalWrite(RST_PIN, LOW);
  delay(100); // Attendre un moment pour s'assurer que le reset est pris en compte
  digitalWrite(RST_PIN, HIGH);

  // Initialisation du MCP23S17
  if (!g_Mcp.begin_SPI(CS_PIN, SCK_PIN, MISO_PIN, MOSI_PIN))
  {
    debug("Erreur lors de l'initialisation du MCP23S17.\n");
    while (1);
  }

  for (int i = 0; i < NB_PINS; i++)
  {
    if (TYPE_PIN[i] == INPUT || TYPE_PIN[i] == INPUT_PULLUP || TYPE_PIN[i] == INPUT_PULLDOWN || TYPE_PIN[i] == OUTPUT)
    {
      g_Mcp.pinMode(i, TYPE_PIN[i]);
    }
  }
}

/*
Brief : Fonction de rappel appelée lorsqu'une demande est reçue du maître I2C.
Cette fonction lit l'état de tous les boutons/switches/bananes, formate ces données en JSON, et les envoie au maître I2C.
*/
void onRequest()
{
  g_Neo.working(); // Indiquer que le système est en train de travailler avec le NeoPixel

  debug("Maître a demandé les données.\n");

  // Envoyer les données JSON au maître I2C
  Wire.write(g_jsonData.c_str());
  Wire.write(0x00); // Ajouter un caractère de nouvelle ligne pour indiquer la fin des données

  debug("Données JSON envoyées : %s\n", g_jsonData.c_str());
  
  g_Neo.success(); // Indiquer que les données ont été préparées avec succès avec le NeoPixel
  g_Neo.waiting(); // Revenir à l'état d'attente avec le NeoPixel
}

/*
Brief : Lit l'état de tous les inputes (boutons/switches/bananes) connectés au MCP23S17 et retourne un tableau d'entiers représentant ces états.
Retour :
- Tableau d'entiers où chaque élément correspond à l'état d'un bouton/switch/banane (0 ou 1).
*/
int* readAllMCP()
{
  int* states = new int[NB_INPUTS]; // Tableau pour stocker les états des boutons/switches/bananes
  int compteur = 0;

  for (int i = 0; i < NB_PINS; i++) 
  {
    if (TYPE_PIN[i] == INPUT || TYPE_PIN[i] == INPUT_PULLUP || TYPE_PIN[i] == INPUT_PULLDOWN) {
      states[compteur++] = g_Mcp.digitalRead(i);
    }
  }

  return states;
}

/*
Brief : Formate les états des boutons, switches et bananes en une chaîne JSON à envoyer au maître I2C.
Paramètres :
- states : Tableau d'entiers représentant l'état de chaque bouton/switch/banane (0 ou 1).
Retour :
- String contenant les données formatées en JSON.
*/
String formatDataAsJSON(int* states)
{
  String jsonData = ""; // String pour stocker les données JSON à envoyer
  
  // Construire la chaîne JSON
  jsonData = "{N:\"" + ESP32_NAME + "\"";
  for (int i = 0; i < NB_INPUTS; i++)
  {
    jsonData += "," + NAME_INPUTS[i] + ":" + String(states[i]);
  }
  jsonData += "}";

  return jsonData;
}