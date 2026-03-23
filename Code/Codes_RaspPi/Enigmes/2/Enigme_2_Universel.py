#from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time
import json
import re # Pour ajouter des guillemets autour des clés du JSON si nécessaire
import random
from Log import logger

#bus = SMBus(1)

ADDR_ESPIO = 0x10  # Adresse I2C de l'ESPIO
ADDR_ESPNEO = 0x12  # Adresse I2C de l'ESPNEO

NB_STRIPS = 5
NB_DEL_PAR_STRIP = [8, 8, 8, 8, 8]  # Nombre de DELs par strip (peut être modifié selon les besoins)

if len(NB_DEL_PAR_STRIP) != NB_STRIPS:
    logger.error("La longueur de NB_DEL_PAR_STRIP doit être égale à NB_STRIPS.")
    quit()

# Choisir le mode de mélange : 'ADDITIF' ou 'SOUSTRACTIF'
MODE_MELANGE = 'SOUSTRACTIF'

# Couleurs
if MODE_MELANGE == 'ADDITIF':
    ALL_COULEURS = {
    # Couleurs de base utilisées pour l'additif
    "ROUGE": "#FF0000",
    "VERT": "#00FF00",
    "BLEU": "#0000FF",

    # Mélanges
    "NOIR": "#000000",   # Aucun bouton appuyé
    "JAUNE": "#FFFF00",  # Rouge + Vert
    "CYAN": "#00FFFF",    # Vert + Bleu
    "MAGENTA": "#FF00FF", # Rouge + Bleu
    "BLANC": "#FFFFFF"   # Rouge + Vert + Bleu
}
    COULEUR_PAR_DEFAUT = ALL_COULEURS["NOIR"] # Couleur qui sera affichée lorsque aucun bouton n'est appuyé (tous les filtres sont éteints)

elif MODE_MELANGE == 'SOUSTRACTIF':
    ALL_COULEURS = {
    # Couleurs de base utilisées pour le soustractif
    "ROUGE": "#FF0000",
    "JAUNE": "#FFFF00",
    "BLEU": "#0000FF",

    # Mélanges
    "BLANC": "#FFFFFF",   # Aucun bouton appuyé
    "ORANGE": "#FF8000",   # Rouge + Jaune
    "VERT": "#00FF00",     # Jaune + Bleu
    "VIOLET": "#800080",   # Rouge + Bleu
    "MARRON": "#804000"   # Rouge + Jaune + Bleu
}
    COULEUR_PAR_DEFAUT = ALL_COULEURS["BLANC"] # Couleur qui sera affichée lorsque aucun bouton n'est appuyé (tous les filtres sont éteints)


COULEURS_CIBLES = [ALL_COULEURS["ORANGE"], ALL_COULEURS["VERT"], ALL_COULEURS["VIOLET"], ALL_COULEURS["MARRON"], ALL_COULEURS["BLANC"]]  # Couleurs cibles à atteindre pour résoudre l'énigme (peuvent être modifiées selon les besoins)

COULEURS_DEPART = [COULEUR_PAR_DEFAUT] * NB_STRIPS  # Couleur de départ pour chaque strip (peut être modifiée selon les besoins)

for i in range(NB_STRIPS):
    couleur_rand = None
    # Génere des couleurs de départ différentes pour chaque strip avec random
    while couleur_rand is None or couleur_rand == COULEURS_CIBLES[i]:
        couleur_rand = random.choice(list(ALL_COULEURS.values()))
    COULEURS_DEPART[i] = couleur_rand


logger.debug(f"Couleurs de départ générées pour chaque strip : {COULEURS_DEPART}")
logger.debug(f"Couleurs cibles à atteindre pour résoudre l'énigme : {COULEURS_CIBLES}")

quit()


def getI2C():
    """
    Demande une lecture I2C à l'adresse ADDR_ESPIO et retourne la chaîne de caractères reçue.
    La fonction lit jusqu'à 256 octets de données, convertit les octets en caractères et les concatène pour former une chaîne.

    Returns:
        La string reçue via I2C, ou None en cas d'erreur de lecture.
    """

    try:
        strReceived = ""
        # Lecture de la réponse
        response = i2c_msg.read(ADDR_ESPIO, 256)  # Lire jusqu'à 256 octets
        bus.i2c_rdwr(response)

        for value in response:
            if (value == 0x00):
                break
            strReceived += chr(value)
        # Convertir la liste d'octets en chaîne
        #logger.debug(f"[getI2C] Données reçues : {strReceived}")

        return strReceived
    
    except Exception as e:
        logger.error(f"[getI2C] Erreur de lecture I2C: {e}")
        time.sleep(1)  # Petite pause pour éviter de surcharger le bus en cas d'erreur répétée
        return None
    


def decodeJSON(json_str):
    """
    Décoder une chaîne JSON pour récupérer les valeurs des switchs.
    Le JSON est au format: {N:"IO",BANA0:1,BANA1:0,BANA2:1,BANA3:0,BANA4:1,BANA5:0,BANA6:1,SW3:0,BTN2:1,BTN1:0,BTN0:1,BTN3:0,BTN4:1,SW0:0,SW1:1,SW2:0}
    La fonction ajoute des guillemets autour des clés si nécessaire pour assurer un format JSON valide, puis utilise json.loads pour décoder la chaîne.
    Elle extrait ensuite les valeurs des boutons BTN0 à BTN4 en les stockant dans une liste de booléens, où True représente un bouton en position OFF (0 logique) et False représente un bouton en position ON (1 logique).

    Parameters:
        json_str (str): La chaîne JSON à décoder.

    Returns:
        list: Une liste de booléens représentant les états des boutons [BTN0, BTN1, BTN2, BTN3, BTN4], ou None en cas d'erreur de décodage.
    """
    button_values = [False] * 5  # Liste pour stocker les valeurs des boutons

    try:
        # Prétraitement : ajouter des guillemets autour des clés si absent
        # Ajoute des guillemets autour des clés non entourées
        json_str_corrige = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_str)
        #print("JSON corrigé pour décodage:", json_str_corrige)
        data = json.loads(json_str_corrige)
        # Extraire les valeurs des boutons
        for key, value in data.items():
            if key.startswith('N') and value != "IO":
                logger.warning("[decodeJSON] Le message n'est pas au format attendu (N doit être 'IO').")
                return None
            elif key.startswith('BTN'):
                index = int(key[3:])  # Extraire l'index du bouton (ex: BTN3 -> 3)
                if value == 1:
                    #logger.debug(f"Bouton {index} est False, bouton non appuyé")
                    button_values[index] = False
                elif value == 0:
                    #logger.debug(f"Bouton {index} est True, bouton appuyé")
                    button_values[index] = True
                else:
                    logger.warning(f"[decodeJSON] Valeur inattendue pour {key}: {value}")
                    return None
                
        return button_values # Retourne la liste des valeurs des boutons après décodage (Si on se rends ici, c'est qu'il n'y a pas d'erreur)
    

    except Exception as e:
        logger.error(f"[decodeJSON] Erreur lors du décodage JSON: {e}")
        return None



try:
    button_values = [False] * 5  # Initialisation de la liste des valeurs des boutons
    last_button_values = [False] * 5  # Variable pour stocker les valeurs des boutons lors de la dernière itération
    button_values_temp = [False] * 5  # Variable temporaire pour stocker les valeurs des boutons avant de les copier dans button_values

    selection_strip = 0  # Variable pour suivre la sélection actuelle (0 à 4)
    couleurs_strip = couleurs_depart.copy()  # Initialisation des couleurs du strip avec les couleurs de départ

    message = "{" + ",".join(f'"S{i}":{c}' for i, c in enumerate(couleurs_strip)) + "}"
    logger.debug(f"[lancer_enigme] Message initial à envoyer via I2C : {message}")
    data = [ord(c) for c in message]
    logger.debug(f"[lancer_enigme] Données à envoyer via I2C (en octets) : {data}")

    try:
        i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
        bus.i2c_rdwr(i2c_msg_write)
        logger.debug(f"[lancer_enigme] Message envoyé via I2C : {message}")

    except Exception as e:
        logger.error(f"[lancer_enigme] Erreur lors de l'écriture I2C: {e}")
        quit()

    while True:
        strReceived = getI2C()

        if strReceived is not None:
            button_values_temp = decodeJSON(strReceived)
            if button_values_temp is not None:
                button_values = button_values_temp.copy()

        if button_values != last_button_values:
            logger.debug(f"Changement détecté dans les valeurs des boutons: {button_values}")
            last_button_values = button_values.copy()

except Exception as e:
    logger.error(f"Erreur dans la boucle principale: {e}")
except KeyboardInterrupt:
    print("\nFin du programme !")
finally:
    bus.close()