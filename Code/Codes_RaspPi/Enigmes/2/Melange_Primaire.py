# Couleurs de base (peinture)
BLANC = [255, 255, 255]
ROUGE = [255, 0, 0]
JAUNE = [255, 255, 0]
BLEU = [0, 0, 255]
ORANGE = [255, 128, 0]
VERT = [0, 255, 0]
VIOLET = [128, 0, 128]
MARRON = [128, 64, 0]
NOIR = [0, 0, 0]

# Strips
STRIP_0 = [0, 0, 0]
STRIP_1 = [0, 0, 0]
STRIP_2 = [0, 0, 0]
STRIP_3 = [0, 0, 0]
STRIP_4 = [0, 0, 0]

# --- Gestion de boutons pour mélange de couleurs ---
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


# Table de vérité pour les mélanges soustractifs (peinture)
def melange_peinture(rouge, jaune, bleu):
    if rouge and jaune and bleu:
        return MARRON  # ou NOIR selon préférence
    elif rouge and jaune:
        return ORANGE
    elif jaune and bleu:
        return VERT
    elif rouge and bleu:
        return VIOLET
    elif rouge:
        return ROUGE
    elif jaune:
        return JAUNE
    elif bleu:
        return BLEU
    else:
        return BLANC

def set_strip_color(color):
	global STRIP_0
	STRIP_0 = color
	print(f"Couleur du strip changée: {STRIP_0}")

# --- Système toggle pour chaque couleur ---
etat_rouge = False
etat_jaune = False
etat_bleu = False

# Pour mémoriser l'état précédent des boutons (pour détecter le front descendant)
prev_btn_rouge = GPIO.input(PIN_BTN_ROUGE)
prev_btn_jaune = GPIO.input(PIN_BTN_JAUNE)
prev_btn_bleu = GPIO.input(PIN_BTN_BLEU)

try:
    while True:
        btn_rouge = GPIO.input(PIN_BTN_ROUGE)
        btn_jaune = GPIO.input(PIN_BTN_JAUNE)
        btn_bleu = GPIO.input(PIN_BTN_BLEU)

        # Toggle sur front descendant (appui)
        if btn_rouge == GPIO.LOW and prev_btn_rouge == GPIO.HIGH:
            etat_rouge = not etat_rouge
        if btn_jaune == GPIO.LOW and prev_btn_jaune == GPIO.HIGH:
            etat_jaune = not etat_jaune
        if btn_bleu == GPIO.LOW and prev_btn_bleu == GPIO.HIGH:
            etat_bleu = not etat_bleu

        prev_btn_rouge = btn_rouge
        prev_btn_jaune = btn_jaune
        prev_btn_bleu = btn_bleu

        couleur_finale = melange_peinture(etat_rouge, etat_jaune, etat_bleu)
        set_strip_color(couleur_finale)
        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()