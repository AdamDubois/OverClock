# Projet Bombe - Code/Codes_RaspPi

## Description

Ici se trouvent tous les fichiers de code utilisés par le Raspberry Pi dans le projet Bombe.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour les différents composants du projet Bombe. Il est organisé de la manière suivante :
- `0-Desuet/` : Contient les codes qui ont été fait avant de choisir qu'on allait utiliser les ESP32. Ces codes sont donc fait pour communiquer avec tous les composants du projet, mais ils sont désuets et ne sont plus utilisés. Ils sont cependant gardés pour référence.
- `Codes_Interactions_ESP/` : Contient les codes pour les interactions entre le Raspberry Pi et les ESP32, notamment la communication I2C. Il y a des codes uniquement pour envoyer et recevoir des données sur le bus I2C et il y en a pour tester uniqement les animations de DEL programmables sur le ESP32_DEL.
- `Qt/` : Contient les fichiers de code pour l'interface graphique développée avec PyQt5. Cette interface permet de visualiser les données en temps réel, d'afficher les logs et d'interagir avec le système de manière plus intuitive.