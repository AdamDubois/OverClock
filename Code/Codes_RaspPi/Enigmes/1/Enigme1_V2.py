from Config import *
from Log import logger
from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time
import json
import re # Pour ajouter des guillemets autour des clés du JSON si nécessaire

valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()

bus = SMBus(I2C_BUS_NUMBER)



def test_sequence(valeur_sequence_attendue=VALEUR_SWITCHES_INIT.copy()):
    """
    Test la séquence attendue en fonction de la séquence définie dans SEQUENCE_ATTENDUE.
    La fonction parcourt la séquence attendue et compare les valeurs des switchs à chaque étape.
    Si la séquence finale correspond à VALEUR_SWITCH_FIN, la fonction réinitialise la séquence attendue pour la prochaine tentative.
    Sinon, elle affiche un message d'erreur et termine le programme.
    """
    try:
        logger.debug(f"[Test de la séquence] Séquence : 0, Valeurs des switchs attendues : {valeur_sequence_attendue}")

        for sequence, valeur in enumerate(SEQUENCE_ATTENDUE):
            for i in range(4):
                if i == valeur:
                    valeur_sequence_attendue[i] = not valeur_sequence_attendue[i]
                    sequence += 1
                    logger.debug(f"[Test de la séquence] Séquence : {sequence}, Valeurs des switchs attendues : {valeur_sequence_attendue}")
                    break # Passe à la prochaine valeur de la séquence attendue après avoir trouvé le switch à toggler

        if valeur_sequence_attendue == VALEUR_SWITCH_FIN:
            logger.info("[Test de la séquence] Séquence finale correcte !")
            valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()  # Réinitialiser pour la prochaine séquence
            return

        else:
            logger.error("[Test de la séquence] Séquence finale incorrecte en fonction de la séquence attendue.")
            quit()

    except Exception as e:
        logger.error(f"[Test de la séquence] Erreur lors du test de la séquence : {e}")
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
        #logger.error(f"[getI2C] Erreur de lecture I2C: {e}")
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
        list: Une liste de booléens représentant les états des switchs [SW0, SW1, SW2, SW3], ou None en cas d'erreur de décodage.
    """
    switch_values = [False] * 4  # Liste pour stocker les valeurs des switchs

    try:
        # Prétraitement : ajouter des guillemets autour des clés si absent
        # Ajoute des guillemets autour des clés non entourées
        json_str_corrige = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_str)
        #print("JSON corrigé pour décodage:", json_str_corrige)
        data = json.loads(json_str_corrige)
        # Extraire les valeurs des switchs
        for key, value in data.items():
            if key.startswith('N') and value != "IO":
                logger.warning("Le message n'est pas au format attendu (N doit être 'IO').")
                return None
            elif key.startswith('SW'):
                index = int(key[2:])  # Extraire l'index du switch (ex: SW3 -> 3)
                if value == 1:
                    #logger.debug(f"Switch {index} est True")
                    switch_values[index] = True
                elif value == 0:
                    #logger.debug(f"Switch {index} est False")
                    switch_values[index] = False
                else:
                    logger.warning(f"Valeur inattendue pour {key}: {value}")
                    return None
                
        return switch_values # Retourne la liste des valeurs des switchs après décodage (Si on se rends ici, c'est qu'il n'y a pas d'erreur)
    

    except Exception as e:
        logger.error(f"[decodeJSON] Erreur lors du décodage JSON: {e}")
        return None
    


def lancer_enigme():
    """
    Fonction principale pour lancer l'énigme.
    Elle teste la séquence attendue, lit les données I2C, décode le JSON reçu et vérifie si les valeurs des switchs correspondent à la séquence attendue.
    Si la séquence est correcte, elle affiche un message de succès. Sinon, elle affiche un message d'erreur.
    """
    try:
        test_sequence()

        message = str(MSG_LED_TOUT_ROUGE) # Message à envoyer pour indiquer que l'énigme a été lancée, met toutes les DELs en rouge
        data = [ord(c) for c in message]

        try:
            i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
            bus.i2c_rdwr(i2c_msg_write)
            logger.debug(f"[lancer_enigme] Message envoyé via I2C : {message}")

        except Exception as e:
            logger.error(f"[lancer_enigme] Erreur lors de l'écriture I2C: {e}")
            quit()
        
    except Exception as e:
        logger.error(f"[lancer_enigme] Erreur lors du lancement de l'énigme: {e}")
        quit()



def mauvaise_sequence():
    """
    Fonction à appeler en cas de séquence incorrecte.
    Elle affiche un message d'erreur et peut être utilisée pour déclencher des animations d'échec sur les bandes LED.
    """
    logger.error("Séquence incorrecte, recommencez !")

    message = str(MSG_LED_ECHEC) # Message à envoyer pour indiquer que la séquence est incorrecte, met les DELs en rouge clignotant
    data = [ord(c) for c in message]
    try:
        i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
        bus.i2c_rdwr(i2c_msg_write)
        logger.debug(f"[mauvaise_sequence] Message envoyé via I2C : {message}")
    except Exception as e:
        logger.error(f"[mauvaise_sequence] Erreur d'écriture I2C: {e}")

    time.sleep(1 * 5) # Il faut attendre que l'animation d'échec soit terminée avant de pouvoir recommencer, sinon le ESPNEO va ignorer les messages et il va y avoir un bug dans les lumières allumées. Le delay est de 1 seconde par flash, il y en a 5



def sequence_correcte(index_sequence):
    """
    Fonction à appeler en cas de séquence correcte.
    Elle affiche un message de succès et peut être utilisée pour déclencher des animations de réussite sur les bandes LED.
    """
    logger.info("Séquence correcte !")

    message = str(MSG_LED_VERT[index_sequence]) # Message pour allumer la bonne DEL en vert en fonction de l'étape de la séquence
    data = [ord(c) for c in message]
    try:
        i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
        bus.i2c_rdwr(i2c_msg_write)
        logger.debug(f"[sequence_correcte] Message envoyé via I2C : {message}")
    except Exception as e:
        logger.error(f"[sequence_correcte] Erreur d'écriture I2C: {e}")



def terminer_enigme():
    """
    Fonction à appeler pour terminer l'énigme.
    Elle peut être utilisée pour déclencher une animation de réussite finale sur les bandes LED ou pour effectuer d'autres actions de fin d'énigme.
    """
    logger.info("Séquence finale atteinte, félicitations !")

    message = str(MSG_LED_REUSSI) # Message à envoyer pour indiquer que l'énigme est réussie, met toutes les DELs en vert
    data = [ord(c) for c in message]
    try:
        i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
        bus.i2c_rdwr(i2c_msg_write)
        logger.debug(f"[terminer_enigme] Message envoyé via I2C : {message}")
    except Exception as e:
        logger.error(f"[terminer_enigme] Erreur d'écriture I2C: {e}")



try:
    lancer_enigme()

    switch_values = [False] * 4  # Valeurs actuelles des switchs
    last_switch_values = [False] * 4  # Valeurs des switchs lors de la dernière vérification
    switch_values_temp = [False] * 4  # Valeurs temporaires des switchs pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
    num_sequence = 0  # Numéro de la séquence actuelle
    switch_values_attendues = VALEUR_SWITCHES_INIT.copy()  # Valeurs des switchs attendues pour la séquence actuelle, initialisées à la valeur de départ

    switch_values_temp = decodeJSON(getI2C())
    if switch_values_temp is not None:
        switch_values = switch_values_temp
        if switch_values != VALEUR_SWITCHES_INIT:
            last_switch_values = switch_values.copy() # Initialiser last_switch_values avec les valeurs actuelles des switchs pour éviter de détecter une modification dès le début si les switchs sont déjà

    while True:
        switch_values_temp = decodeJSON(getI2C())

        if switch_values_temp is not None:
            switch_values = switch_values_temp

        if switch_values != last_switch_values:
            last_switch_values = switch_values.copy()

            logger.debug(f"Modification des switchs détectée : {switch_values}")
            logger.debug(f"Sequence attendu : {valeur_sequence_attendue}")

            if switch_values == valeur_sequence_attendue:
                sequence_correcte(num_sequence)

                if num_sequence > len(SEQUENCE_ATTENDUE):
                    terminer_enigme()
                    quit()

                else:
                    num_sequence -= 1
                    
                    for i in range(4):
                        if i == SEQUENCE_ATTENDUE[num_sequence]:
                            valeur_sequence_attendue[i] = not valeur_sequence_attendue[i]
                            num_sequence += 1
                            break

                logger.debug(f"Nouvelle séquence attendu : {valeur_sequence_attendue}")

            elif not premiere_valeur: # Si ce n'est pas la première modification des switchs, alors on affiche les DELs d'erreur, sinon on considère que c'est juste les joueurs qui mettent les switchs à la bonne position au lancement de l'énigme, ce qui peut être confus s'il y a les DELs d'erreur qui s'affichent dès le début
                mauvaise_sequence()

                num_sequence = 0
                valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()  # Réinitialiser pour la prochaine séquence

                if switch_values == VALEUR_SWITCHES_INIT:
                    logger.debug("Les switchs sont à leur position de départ")
                    last_switch_values = [False] * 4 # Réinitialiser. Si les valeurs des switchs actuelles sont celle de départ, on veut pouvoir les détecter comme une modification et afficher la séquence attendue, sinon on ne l'affiche pas et ça peut être confus pour les joueurs qui ne savent pas quelle est la séquence attendue au départ
        time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins


except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")

finally:
    bus.close()