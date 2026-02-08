#include <Arduino.h>
#include "I2C_Slave.h"
#include "config.h" //Fichier de configuration des broches et paramètres (inclut les bibliothèques nécessaires)

void I2C_Slave::init() {
    // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie
    Wire.setPins(SDA_PIN, SCL_PIN);
    Wire.begin(SLAVE_ADDR);
    Wire.onReceive(commandeMaitre); // Définir la fonction de rappel pour les demandes du maître
}

void I2C_Slave::commandeMaitre(int howMany) {
    // Lire les données envoyées par le maître
    String receivedData = "";
    while (Wire.available()) {
        char c = Wire.read();
        receivedData += c;
    }
    Serial.println("Données reçues du maître: " + receivedData);
}

void I2C_Slave::direBonjour() {
    Serial.println("Bonjour depuis I2C_Slave !");
}