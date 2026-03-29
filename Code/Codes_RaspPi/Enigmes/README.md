# Projet Bombe - Code/Codes_RaspPi/Enigmes

## Description

Contient les codes pour les différentes énigmes du projet Bombe. Ces codes sont utilisés pour gérer la logique des énigmes, les interactions avec les utilisateurs et les différentes fonctionnalités associées à chaque énigme. Chaque énigme a son propre sous-dossier pour organiser les fichiers de manière claire et faciliter la navigation.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour les différentes énigmes du projet Bombe, notamment pour les interactions entre le Raspberry Pi et les ESP32 du projet Bombe. Il est organisé de la manière suivante :
- `1/` : Dossier contenant les codes pour la première énigme du projet Bombe, qui est l'énigme des interrupteurs. Il contient les codes pour lire les données des interrupteurs connectés aux ESP32 via I2C et pour envoyer des commandes I2C aux ESP32_DEL pour tester les animations de DEL programmables.
- `2/` : Dossier contenant les codes pour la deuxième énigme du projet Bombe, qui est l'énigme des boutons et des strips de del ou il faut mettre les strips d'une couleur spécifique en fonction des boutons appuyés. Il contient les codes pour lire les données des boutons connectés aux ESP32 via I2C et pour envoyer des commandes I2C aux ESP32_DEL pour tester les animations de DEL programmables.