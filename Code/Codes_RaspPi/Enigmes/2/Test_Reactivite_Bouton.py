from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time
import json
import re # Pour ajouter des guillemets autour des clés du JSON si nécessaire
from Log import logger

bus = SMBus(1)

ADDR_ESPIO = 0x10  # Adresse I2C de l'ESPIO
ADDR_ESPNEO = 0x12  # Adresse I2C de l'ESPNEO

couleurs_attendu = [[0,255,0],[0,255,0],[0,255,0],[0,255,0],[0,255,0]]
couleurs_depart = [[255,0,255],[255,255,0],[255,255,255],[0,0,0],[0,255,255]]

RED = [255, 0, 0]
YELLOW = [255, 255, 0]
BLUE = [0, 0, 255]



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
                logger.warning("Le message n'est pas au format attendu (N doit être 'IO').")
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
                    logger.warning(f"Valeur inattendue pour {key}: {value}")
                    return None
                
        return button_values # Retourne la liste des valeurs des boutons après décodage (Si on se rends ici, c'est qu'il n'y a pas d'erreur)
    

    except Exception as e:
        logger.error(f"[decodeJSON] Erreur lors du décodage JSON: {e}")
        return None



try:
    compteur = 0

    while True:
        strReceived = getI2C()
        if strReceived is not None:
            switch_values_temp = decodeJSON(strReceived)
            if switch_values_temp is not None:
                #logger.debug(f"Valeurs des boutons décodées : {switch_values_temp}")
                if switch_values_temp != [False, False, False, False, False]: 
                    logger.info(f"Bouton appuyé ! {compteur}")
                    compteur += 1
            else:
                #logger.debug("Impossible de décoder les valeurs des boutons à partir du message reçu.")
                pass
        else:
            #logger.debug("Aucun message reçu via I2C.")
            pass

except Exception as e:
    logger.error(f"Erreur dans la boucle principale: {e}")
except KeyboardInterrupt:
    print("\nFin du programme !")
finally:
    bus.close()