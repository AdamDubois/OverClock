# Projet Bombe - Code/Codes_ESP32/ESP32_WROOM/ESP_RFID_Test

## Description

Ce projet utilise 4 lecteurs RFID MFRC522 connectés à un ESP32-C3. Quand une carte est détectée par un lecteur, le ESP affiche l'UID de la carte sur le moniteur série. Ce projet est un test pour vérifier que les lecteurs RFID fonctionnent correctement avec l'ESP32-C3 avant de les intégrer dans le projet principal.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour le projets ESP32-WROOM RFID. Il est organisé de la manière suivante :
- `src/` : Contient tous les fichiers de code qui ont été écrits en C++ pour le projet ESP32-WROOM qui gère les strips de DELs programmables. Ces fichiers sont actifs et maintenus, et sont utilisés pour gérer les différentes fonctionnalités liées aux DELs programmables dans le projet Bombe.