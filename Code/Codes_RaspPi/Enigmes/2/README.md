# Projet Bombe - Code/Codes_RaspPi/Enigmes/2

## Description

Dossier contenant les codes pour la deuxième énigme du projet Bombe, qui est l'énigme des boutons et des strips de DEL. Il contient les codes pour lire les données des boutons connectés aux ESP32 via I2C et pour envoyer des commandes I2C aux ESP32_DEL pour tester les animations de DEL programmables.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour l'énigme des boutons et des strips de DEL, notamment pour les interactions entre le Raspberry Pi et les ESP32 du projet Bombe. Il est organisé de la manière suivante :
- `0-Desuet/` : Dossier contenant les codes désuets pour l'énigme des boutons et des strips de DEL. Ces codes sont des versions précédentes du code principal qui ont été améliorées ou modifiées pour la version finale de l'énigme. Ils sont conservés dans ce dossier à des fins de référence ou de comparaison, mais ils ne sont plus utilisés pour la version finale de l'énigme.
- `Config.py` : Fichier de configuration pour les codes de l'énigme des boutons et des strips de DEL. Il contient les adresses I2C des ESP32 utilisés pour les boutons et les ESP32_DEL, ainsi que les commandes I2C à envoyer pour tester les animations de DEL programmables.
- `Enigme_2_Universel.py` : Code principal pour l'énigme des boutons et des strips de DEL. Lit les données du ESP-IO et les traites pour vérifier si elles correspondent à la solution de l'énigme. Affiche les résultats dans la console et envoie des commandes I2C au ESP32_DEL pour tester les animations de DEL programmables en fonction des données reçues. Ce code est universel dans le sens où on peut faire les mélanges de couleurs en fonction des couleurs additives (RGB) ou soustractives (RJB).
- `Log.py` : Fichier de code pour la gestion des logs à afficher dans le terminal pour l'énigme des boutons et des strips de DEL.
- `Test_Melange_Tkinter.py` : Code de test a la même logique que `Enigme_2_Universel.py` mais avec une interface graphique Tkinter pour tester les mélanges de couleurs en fonction des couleurs additives (RGB) ou soustractives (RJB). Utile pour vérifier que la logique de mélange de couleurs fonctionne correctement avant de l'intégrer dans le code principal de l'énigme.