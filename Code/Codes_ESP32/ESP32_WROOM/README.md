# Projet Bombe - Code/Codes_ESP32/ESP32_WROOM

## Description

Ce dossier contient les fichiers de code pour tous les projets de code pour les ESP32-WROOM utilisés dans le projet Bombe. Ces projets sont actifs et maintenus, et sont utilisés pour gérer les différentes fonctionnalités du projet Bombe, telles que la gestion des lecteurs de cartes RFID, des switchs, des boutons et des strips de DELs programmables. Chaque projet est organisé de manière claire pour faciliter la navigation et la compréhension du code.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour les projets ESP32-WROOM. Il est organisé de la manière suivante :
- `ESP_IO/` : Contient le projet du ESP qui gère les entrées/sorties, telles que les switchs et les boutons. Il utilise un IO expander pour gérer les entrées/sorties, et communique avec le Raspberry Pi en I2C pour envoyer les données des switchs et des boutons.
- `ESP_LED/` : Contient le projet du ESP qui gère les strips de DELs programmables. Ce projet reçoit des données en I2C et allume les DELs en fonction de ces données.
- `ESP_RFID/` : Contient le projet du ESP qui gère les lecteurs de cartes RFID. Ce projet lit les données des cartes RFID et les envoie les valeurs de UID des cartes en I2C au Raspberry Pi, quand il reçoit une requête de ce dernier.
- `ESP_RFID_Test/` : Contient un projet de test pour le ESP qui gère les lecteurs de cartes RFID. Ce projet lit les données des cartes RFID et les affiche dans la console série pour tester le bon fonctionnement du lecteur de cartes RFID.
- `ESP-RFID/` : Il a le même fonctionnement que le projet `ESP_RFID/`, mais la disposition de la bibliothèque config est placée différemment pour pouvoir être utilisée par une autre bibliothèque, celle qui gère la DEL NeoPixel pour le débuggage. Ce projet est plus complet que le projet `ESP_RFID/`.
- `I2C_Slave/` : Contient un projet de test pour un ESP32-WROOM qui agit comme esclave I2C. Ce projet reçoit des données en I2C et les affiche dans la console série pour tester la communication I2C entre le Raspberry Pi et les ESP32-WROOM.
- `Test_DEL/` : Contient un projet de test pour un ESP32-WROOM qui gère une DEL. Les DELs s'allument toutes seules. Le but de ce projet est de tester le bon fonctionnement d'une DEL connectée à un ESP32-WROOM.