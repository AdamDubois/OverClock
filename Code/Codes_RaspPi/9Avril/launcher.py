#!/usr/bin/env python3
import subprocess
import sys
import time

# Chemins des scripts à lancer
MAIN_UI = "/home/admin/Documents/Projet_InXtremis/code/Code/Codes_RaspPi/Qt/Interface_9avril/OverClockUI/OverClock/main.py"
MAIN_GAME = "/home/admin/Documents/Projet_InXtremis/code/Code/Codes_RaspPi/9Avril/tout.py"

print("Démarrage du launcher...")
print(f"1. Lancement de l'interface: {MAIN_UI}")
print(f"2. Lancement du jeu: {MAIN_GAME}")
print()

try:
    # Lancer l'interface graphique
    print("Lancement de l'interface graphique...")
    ui_process = subprocess.Popen([sys.executable, MAIN_UI])
    
    # Attendre un peu pour que l'interface se charge
    time.sleep(3)
    
    # Lancer le jeu
    print("Lancement du jeu...")
    game_process = subprocess.Popen([sys.executable, MAIN_GAME])
    
    # Attendre la fin des deux processus
    print("Les deux processus sont en cours d'exécution...")
    print("(Utilisez Ctrl+C pour arrêter)")
    print()
    
    ui_process.wait()
    game_process.terminate()
    game_process.wait(timeout=5)
    
except KeyboardInterrupt:
    print("\n\nArrêt du launcher...")
    try:
        game_process.terminate()
        game_process.wait(timeout=5)
    except:
        game_process.kill()
    try:
        ui_process.terminate()
        ui_process.wait(timeout=5)
    except:
        ui_process.kill()
    print("Processus arrêtés.")
except Exception as e:
    print(f"Erreur: {e}")
    sys.exit(1)
