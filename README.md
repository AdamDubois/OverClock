# Projet Bombe - InXtremis

## Description

Le projet Bombe à pour but de simuler une bombe pour un jeu d'évasion (escape game). Le joueur doit désamorcer la bombe en résolvant une série d'énigmes avant que le temps ne soit écoulé. Pour l'instant, le projet est en cours de développement et ne dispose pas encore de fonctionnalités complètes. Certains éléments de base ont été mis en place, mais ne sont pas intégrés dans un système de jeu complet. Par exemple, le contrôleur des lecteurs de cartes RFID est complètement fonctionnel et le contrôleur principal peut recevoir les données des lecteurs de cartes, mais il n'y a pas encore de logique de jeu pour utiliser ces données.

## Logique des composantes utilisées

**Contrôleur principal** : Il s'agit d'un Raspberry Pi 4 qui gère l'ensemble du système. Il reçoit les données des lecteurs de cartes RFID, des entrées/sorties (switchs et boutons) et peut contrôler d'autres composants tels que les LED, les buzzers, etc. Il est également responsable de la logique de jeu, c'est-à-dire de déterminer si les conditions pour désamorcer la bombe sont remplies ou non. Il gère également l'interface utilisateur qui sera sur un écran HDMI.

**Contrôleurs secondaires** : Il s'agit de trois ESP32-C3-WROOM-02U. Ils sont utilisés pour gérer la partie matérielle de la bombe, notamment les lecteurs de cartes RFID, les switchs, les boutons et les strips de DELs programmables. Ils communiquent avec le contrôleur principal via une I2C pour transmettre les données des entrées/sorties et recevoir les commandes pour contrôler les LED et autres composants.

## Fonctionnalités des différents ESP32

**ESP "RFID"** : Ce contrôleur est dédié à la gestion des lecteurs de cartes RFID. Il lit les données des cartes RFID et les transmet au contrôleur principal via I2C quand le Raspberry Pi en fait la demande.

**ESP "IO"** : Ce contrôleur gère les switchs et les boutons. Il lit l'état de ces entrées et les transmet au contrôleur principal via I2C quand le Raspberry Pi en fait la demande.

**ESP "LED"** : Ce contrôleur est responsable de la gestion des strips de DELs programmables. Il reçoit les commandes du contrôleur principal via I2C pour contrôler les LED en fonction de la logique de jeu.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour les différents composants du projet Bombe. Il est organisé de la manière suivante :
- `Code/` : Contient tous les fichiers de code pour les différents composants du projet, y compris le code pour le contrôleur principal (Raspberry Pi) et les contrôleurs secondaires (ESP32). Chaque composant a son propre sous-dossier pour organiser les fichiers de manière claire.
- `Documentation/` : Contient tous les documents liés au projet, tels que les diagrammes d'architecture, les schémas de câblage, les instructions d'installation et d'utilisation, les schémas électiques d'Altium, etc.
- `Matériel/` :  Contient les fichiers liés au matériel utilisé dans le projet, tels que les listes de composants, les schémas de câblage, les modèles 3D des boîtiers, etc.