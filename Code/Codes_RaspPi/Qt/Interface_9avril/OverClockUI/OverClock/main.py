"""
Nom du fichier : main.py
Description : Point d’entrée principal de l’application.

Ce script :
- Initialise l’application Qt (PySide6)
- Lance le backend de communication (réception JSON via TCP)
- Connecte le backend à l’interface QML
- Charge et affiche l’interface graphique

Fonctionnement :
- Le backend (JsonReceive) reçoit les données du jeu
- Ces données sont exposées à l’interface via le contexte QML ("backend")
- L’interface est chargée depuis le dossier OverClockContent

Dépendances :
- PySide6 (QtGui, QtQml)
- jsonreceive.py

Auteur : Jérémy Breault
Date : 2026-04-25
"""

import sys
from pathlib import Path  # gestion des chemins de fichier

from PySide6.QtGui import QGuiApplication       # Application Qt (interface graphique)
from PySide6.QtQml import QQmlApplicationEngine # Moteur de chargement QML

from jsonreceive import JsonReceive # Backend Python

# Initialisation de l'application Qt
app = QGuiApplication(sys.argv)

# Initialisation du backend
receiver = JsonReceive() # objet backend 

receiver.partir_serveur() # démarrage du serveur TCP

# Configuration du moteur QML
engine = QQmlApplicationEngine()
# Permet d'accéder à "backend" depuis les fichiers QML
engine.rootContext().setContextProperty("backend", receiver)

# Chargement de l'interface QML
base_path = Path(__file__).resolve().parent
qml_file = base_path / "OverClockContent" / "App.qml" # fichier principale au lancement de l'interface

# Chargement du fichier QML
engine.load(qml_file)

# Vérification du chargement
if not engine.rootObjects():
    print("Erreur chargement QML :", qml_file)
    sys.exit(-1)

# Démarre l'application Qt (boucle d'événements)
sys.exit(app.exec())
