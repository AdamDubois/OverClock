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

            if button_values != [False] * 5:

                if button_values[0] is True:
                    logger.debug("Bouton Noir appuyé")

                    if selection_strip == 0:
                        selection_strip = 4
                    else:
                        selection_strip -= 1

                    logger.debug(f"Strip sélectionné: {selection_strip}")

                if button_values[1] is True:
                    logger.debug("Bouton Blanc appuyé")

                    if selection_strip == 4:
                        selection_strip = 0
                    else:
                        selection_strip += 1

                    logger.debug(f"Strip sélectionné: {selection_strip}")

                if button_values[2] is True:
                    logger.debug("Bouton Rouge appuyé")

                    if couleurs_strip[selection_strip][0] == 255:
                        couleurs_strip[selection_strip][0] = 0
                        logger.debug(f"Le strip {selection_strip} n'a plus de rouge.")
                    else:
                        couleurs_strip[selection_strip][0] = 255
                        logger.debug(f"Le strip {selection_strip} a maintenant du rouge.")

                if button_values[3] is True:
                    logger.debug("Bouton Jaune appuyé")

                    if couleurs_strip[selection_strip][0] == 255:
                        couleurs_strip[selection_strip][0] = 0
                        logger.debug(f"Le strip {selection_strip} n'a plus de rouge.")
                    else:
                        couleurs_strip[selection_strip][0] = 255
                        logger.debug(f"Le strip {selection_strip} a maintenant du rouge.")

                    if couleurs_strip[selection_strip][1] == 255:
                        couleurs_strip[selection_strip][1] = 0
                        logger.debug(f"Le strip {selection_strip} n'a plus de vert.")
                    else:
                        couleurs_strip[selection_strip][1] = 255
                        logger.debug(f"Le strip {selection_strip} a maintenant du vert.")

                if button_values[4] is True:
                    logger.debug("Bouton Bleu appuyé")

                    if couleurs_strip[selection_strip][2] == 255:
                        logger.debug(f"Le strip {selection_strip} a déjà du bleu, aucune action nécessaire.")
                    else:
                        couleurs_strip[selection_strip][2] = 255
                        logger.debug(f"Le strip {selection_strip} a maintenant du bleu.")

                message = "{" + ",".join(f'"S{i}":{c}' for i, c in enumerate(couleurs_strip)) + "}"
                data = [ord(c) for c in message]

                try:
                    i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
                    bus.i2c_rdwr(i2c_msg_write)
                    logger.debug(f"[lancer_enigme] Message envoyé via I2C : {message}")

                except Exception as e:
                    logger.error(f"[lancer_enigme] Erreur lors de l'écriture I2C: {e}")
                    quit()




except Exception as e:
    logger.error(f"Erreur dans la boucle principale: {e}")
except KeyboardInterrupt:
    print("\nFin du programme !")
finally:
    bus.close()