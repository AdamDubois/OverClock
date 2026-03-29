# Couleurs de base utilisées
NOIR = [0, 0, 0]
ROUGE = [255, 0, 0]
VERT = [0, 255, 0]
BLEU = [0, 0, 255]
BLANC = [255, 255, 255]

import RPi.GPIO as GPIO
import time

# Définir les broches GPIO pour les boutons
PIN_BTN_ROUGE = 17
PIN_BTN_JAUNE = 27
PIN_BTN_BLEU = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BTN_ROUGE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BTN_JAUNE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BTN_BLEU, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Système toggle pour chaque composante
etat_rouge = False
etat_vert = False
etat_bleu = False

# Pour mémoriser l'état précédent des boutons (pour détecter le front descendant)
prev_btn_rouge = GPIO.input(PIN_BTN_ROUGE)
prev_btn_jaune = GPIO.input(PIN_BTN_JAUNE)
prev_btn_bleu = GPIO.input(PIN_BTN_BLEU)

# Mélange additif RGB
def melange_additif(rouge, vert, bleu):
    r = 255 if rouge else 0
    g = 255 if vert else 0
    b = 255 if bleu else 0
    return [r, g, b]

def set_strip_color(color):
    print(f"Couleur du strip changée: {color}")

try:
    while True:
        btn_rouge = GPIO.input(PIN_BTN_ROUGE)
        btn_jaune = GPIO.input(PIN_BTN_JAUNE)
        btn_bleu = GPIO.input(PIN_BTN_BLEU)

        # Toggle sur front descendant (appui)
        if btn_rouge == GPIO.LOW and prev_btn_rouge == GPIO.HIGH:
            etat_rouge = not etat_rouge
        if btn_jaune == GPIO.LOW and prev_btn_jaune == GPIO.HIGH:
            # Jaune = toggle rouge ET vert
            etat_rouge = not etat_rouge
            etat_vert = not etat_vert
        if btn_bleu == GPIO.LOW and prev_btn_bleu == GPIO.HIGH:
            etat_bleu = not etat_bleu

        prev_btn_rouge = btn_rouge
        prev_btn_jaune = btn_jaune
        prev_btn_bleu = btn_bleu

        couleur_finale = melange_additif(etat_rouge, etat_vert, etat_bleu)
        set_strip_color(couleur_finale)
        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
