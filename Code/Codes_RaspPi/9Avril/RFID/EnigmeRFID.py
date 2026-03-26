from Config import *
from Log import logger
from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time
import json
import re # Pour ajouter des guillemets autour des clés du JSON si nécessaire

bus = SMBus(I2C_BUS_NUMBER)

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
        response = i2c_msg.read(ADDR_ESPRFID, 256)  # Lire jusqu'à 256 octets
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
        time.sleep(1)
        return None
    


def decodeJSON(json_str):
    """
    Décoder une chaîne JSON pour récupérer les valeurs des switchs.
    Le JSON est au format: {N:"IO",BANA0:1,BANA1:0,BANA2:1,BANA3:0,BANA4:1,BANA5:0,BANA6:1,SW3:0,BTN2:1,BTN1:0,BTN0:1,BTN3:0,BTN4:1,SW0:0,SW1:1,SW2:0}
    La fonction ajoute des guillemets autour des clés si nécessaire pour assurer un format JSON valide, puis utilise json.loads pour décoder la chaîne.
    Elle extrait ensuite les valeurs des switchs (SW0, SW1, SW2, SW3) et les stocke dans une liste de booléens.

    Parameters:
        json_str (str): La chaîne JSON à décoder.

    Returns:
        list: Une liste de booléens représentant les états des readers [R0, R1, R2, R3], ou None en cas d'erreur de décodage.
    """
    readers_values = [None] * 4  # Liste pour stocker les valeurs des readers

    try:
        # Prétraitement : ajouter des guillemets autour des clés si absent
        # Ajoute des guillemets autour des clés non entourées
        json_str_corrige = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_str)
        #logger.debug(f"JSON corrigé pour décodage: {json_str_corrige}")

        data = json.loads(json_str_corrige)
        # Extraire les valeurs des readers
        for key, value in data.items():
            if key.startswith('N') and value != "RFID":
                logger.warning("Le message n'est pas au format attendu (N doit être 'RFID').")
                return None
            elif key.startswith('R'):
                index = int(key[1:])  # Extraire l'index du reader (ex: R3 -> 3)
                #logger.debug(f"Reader {index} est {value}")
                readers_values[index] = value
                
        return readers_values # Retourne la liste des valeurs des readers après décodage (Si on se rends ici, c'est qu'il n'y a pas d'erreur)
    

    except Exception as e:
        logger.error(f"[decodeJSON] Erreur lors du décodage JSON: {e}")
        return None
    
try:
    readers_values = [None] * 4  # Valeurs actuelles des switchs
    last_readers_values = [None] * 4  # Valeurs des switchs lors de la dernière vérification
    readers_values_temp = [None] * 4  # Valeurs temporaires des switchs pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.

    while True:
        readers_values_temp = decodeJSON(getI2C())

        if readers_values_temp is not None:
            readers_values = readers_values_temp.copy()

        if readers_values != last_readers_values:
            last_readers_values = readers_values.copy()

            logger.debug(f"Modification des readers détectée : {readers_values}")
            logger.debug(f"Sequence attendu : (9) {ID_CARTE_9}, (3) {ID_CARTE_3}, (4) {ID_CARTE_4}, (1) {ID_CARTE_1}")

            if readers_values[0] == ID_CARTE_9:
                logger.debug("Bonne Premiere")
            else:
                logger.debug("Mauvaise Premiere")
            if readers_values[1] == ID_CARTE_3:
                logger.debug("Bonne Deuxieme")
            else:
                logger.debug("Mauvaise Deuxieme")
            if readers_values[2] == ID_CARTE_4:
                logger.debug("Bonne Troisieme")
            else:
                logger.debug("Mauvaise Troisieme")
            if readers_values[3] == ID_CARTE_1:
                logger.debug("Bonne Derniere")
            else:
                logger.debug("Mauvaise Derniere")

        time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins


except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")

except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")

finally:
    bus.close()