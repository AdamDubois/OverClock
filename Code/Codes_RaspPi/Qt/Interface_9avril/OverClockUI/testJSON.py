"""
Nom du fichier : testJSON.py
Description : Script permettant de simuler l’envoi de données JSON vers l’interface via une connexion TCP.
Auteur : Jérémy Breault
Date : 2026-04-25

Fonctionnalités :
- Envoi de l’état du jeu (game_start, enigme, RFID)
- Simulation des entrées utilisateur via le terminal
- Communication avec l’interface sur localhost (127.0.0.1:5000)
"""

import socket # pour la communication réseau (TCP) 
import json # données JSON

# Configuration réseau
HOST = "127.0.0.1"
PORT = 5000

rfid = [0, 0, 0, 0] # état des 4 modules RFID
enigme = 0          # énigme en cours
game_start = False  # si le jeu est démarré


def send_state():
    """
    Envoie l'état actuel du jeu à l'interface via une connexion TCP.
    """
    data = {
        "game_start": game_start,
        "enigme": enigme,
        "rfid": rfid,
    }

    # conversion en JSON
    message = json.dumps(data) + "\n"


    try:
        # Création du socket client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connexion au serveur
        client.connect((HOST, PORT))
        # Envoi des données encodées en UTF-8
        client.sendall(message.encode("utf-8"))
        # Fermeture de la connexion
        client.close()
        # Affichage dans le terminal
        print(f"Envoyé -> game_start: {game_start}, enigme: {enigme}, rfid: {rfid}")

    # gestion des erreurs
    except Exception as e:
        print("Erreur :", e)

# Interface utilisateur
print("Contrôles :")
print("g → toggle game_start")
print("0-9 → changer enigme")
print("r1 r2 r3 r4 → toggle RFID")
print("reset → reset RFID")
print("q → quitter")

send_state()

# Boucle principale
while True:
    key = input(">> ").strip().lower()

    if key == "q":
        break

    elif key == "g":
        game_start = not game_start

    # Change l'énigme
    elif key.isdigit():
        enigme = int(key)

    # Active ou desactive un capteur RFID
    elif key in ["r1", "r2", "r3", "r4"]:
        index = int(key[1]) - 1
        rfid[index] = 1 - rfid[index]

    elif key == "reset":
        rfid = [0, 0, 0, 0]

    else:
        print("Commande invalide")
        continue

    send_state()