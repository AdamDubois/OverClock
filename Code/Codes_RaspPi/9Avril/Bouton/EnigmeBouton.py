from Config import *
from I2C_handler import I2C
from Log import logger

I2C_handler = I2C()

button_values = [False] * NB_MODULES  # Initialisation de la liste des valeurs des boutons
last_button_values = [False] * NB_MODULES  # Variable pour stocker les valeurs des boutons lors de la dernière itération
button_values_temp = [False] * NB_MODULES  # Variable temporaire pour stocker les valeurs des boutons avant de les copier dans button_values
etat_couleurs = None # Variable pour stocker l'état des couleurs (rouge, jaune ou vert et bleu) pour chaque strip


# Correction : initialisation correcte de la liste des états de couleurs
etat_couleurs = []
for i in range(NB_STRIPS):
    etat_couleurs.append({
        "rouge": False,
        "jaune": False, # utilisé pour le soustractif
        "bleu": False,
        "vert": False # utilisé seulement pour l'additif
    })

for couleurs in COULEURS_DEPART:
    if MODE_MELANGE == 'ADDITIF': 
        if couleurs == ALL_COULEURS["ROUGE"]:
            etat_couleurs[i]["rouge"] = True
        elif couleurs == ALL_COULEURS["VERT"]:
            etat_couleurs[i]["vert"] = True
        elif couleurs == ALL_COULEURS["BLEU"]:
            etat_couleurs[i]["bleu"] = True
        elif couleurs == ALL_COULEURS["JAUNE"]:
            etat_couleurs[i]["rouge"] = True
            etat_couleurs[i]["vert"] = True
        elif couleurs == ALL_COULEURS["CYAN"]:
            etat_couleurs[i]["vert"] = True
            etat_couleurs[i]["bleu"] = True
        elif couleurs == ALL_COULEURS["MAGENTA"]:
            etat_couleurs[i]["rouge"] = True
            etat_couleurs[i]["bleu"] = True
        elif couleurs == ALL_COULEURS["BLANC"]:
            etat_couleurs[i]["rouge"] = True
            etat_couleurs[i]["vert"] = True
            etat_couleurs[i]["bleu"] = True

    elif MODE_MELANGE == 'SOUSTRACTIF':
        if couleurs == ALL_COULEURS["ROUGE"]:
            etat_couleurs[i]["rouge"] = True
        elif couleurs == ALL_COULEURS["JAUNE"]:
            etat_couleurs[i]["jaune"] = True
        elif couleurs == ALL_COULEURS["BLEU"]:
            etat_couleurs[i]["bleu"] = True
        elif couleurs == ALL_COULEURS["ORANGE"]:
            etat_couleurs[i]["rouge"] = True
            etat_couleurs[i]["jaune"] = True
        elif couleurs == ALL_COULEURS["VERT"]:
            etat_couleurs[i]["jaune"] = True
            etat_couleurs[i]["bleu"] = True
        elif couleurs == ALL_COULEURS["VIOLET"]:
            etat_couleurs[i]["rouge"] = True
            etat_couleurs[i]["bleu"] = True
        elif couleurs == ALL_COULEURS["MARRON"]:
            etat_couleurs[i]["rouge"] = True
            etat_couleurs[i]["jaune"] = True
            etat_couleurs[i]["bleu"] = True

selection_strip = 0  # Variable pour suivre la sélection actuelle (0 à 4)
selection_strip_flash = selection_strip  # Doit être égale à selection_strip, quand la couleur de cette strip est changée une fois, on la met à -1 pour arrêter le flash, et on la remet à selection_strip lorsqu'une nouvelle strip est sélectionnée
couleurs_strip = [None] * NB_STRIPS  # Liste pour stocker les couleurs actuelles des strips, utilisée pour envoyer les bonnes couleurs à l'ESP32 via I2C
couleurs_strip[0] = COULEURS_DEPART.copy()  # Initialisation des couleurs du strip avec les couleurs de départ

nb_bonnes_strips = 0 # Variable pour compter le nombre de strips qui sont dans la bonne couleur cible, utilisée pour vérifier si l'énigme est résolue

def lancer_enigme():
    message = formatToESPCommande() # Format du message à envoyer via I2C : {"E":2,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
    logger.debug(f"[lancer_enigme] Message initial à envoyer via I2C : {message}")
    I2C_handler.sendI2C(message) # Envoie le message formaté à l'ESP32 pour initialiser les couleurs des strips et la sélection

def formatToESPCommande():
    global selection_strip_flash
    # Format du message à envoyer via I2C : {"E":2,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
    #  - E : numéro de l'énigme (pour vérification)
    #  - Selected : numéro du strip sélectionné (0 à 4) ou -1 si aucun strip n'est sélectionné
    message = "{\"E\":" + str(NUM_ENIGME) + ",\"Selected\":" + str(selection_strip_flash) + "," + ",".join(f'"S{i}":"{c}"' for i, c in enumerate(couleurs_strip)) + "}"
    logger.debug(f"[formatToESPCommande] Message formaté à envoyer via I2C : {message}")
    return message

def traiter_changement_boutons():
    global selection_strip, selection_strip_flash
    if button_values[0] == False and last_button_values[0] == True:
        selection_strip = (selection_strip - 1) % NB_STRIPS
        selection_strip_flash = selection_strip
        logger.debug(f"Strip sélectionné : {selection_strip}")

    if button_values[1] == False and last_button_values[1] == True:
        selection_strip = (selection_strip + 1) % NB_STRIPS
        selection_strip_flash = selection_strip
        logger.debug(f"Strip sélectionné : {selection_strip}")

    if button_values[2] == False and last_button_values[2] == True:
        etat_couleurs[selection_strip]["rouge"] = not etat_couleurs[selection_strip]["rouge"] # Inverse l'état de la couleur rouge pour la strip sélectionnée
        selection_strip_flash = -1 # Arrête le flash de la strip sélectionnée lorsque la couleur est changée
        logger.debug(f"Couleur rouge pour la strip {selection_strip} est maintenant {'activée' if etat_couleurs[selection_strip]['rouge'] else 'désactivée'}")

    if button_values[3] == False and last_button_values[3] == True:
        if MODE_MELANGE == 'SOUSTRACTIF':
            etat_couleurs[selection_strip]["jaune"] = not etat_couleurs[selection_strip]["jaune"] # Inverse l'état de la couleur jaune pour la strip sélectionnée
            selection_strip_flash = -1 # Arrête le flash de la strip sélectionnée lorsque la couleur est changée
            logger.debug(f"Couleur jaune pour la strip {selection_strip} est maintenant {'activée' if etat_couleurs[selection_strip]['jaune'] else 'désactivée'}")
        elif MODE_MELANGE == 'ADDITIF':
            etat_couleurs[selection_strip]["vert"] = not etat_couleurs[selection_strip]["vert"] # Inverse l'état de la couleur verte pour la strip sélectionnée
            selection_strip_flash = -1 # Arrête le flash de la strip sélectionnée lorsque la couleur est changée
            logger.debug(f"Couleur verte pour la strip {selection_strip} est maintenant {'activée' if etat_couleurs[selection_strip]['vert'] else 'désactivée'}")

    if button_values[4] == False and last_button_values[4] == True:
        etat_couleurs[selection_strip]["bleu"] = not etat_couleurs[selection_strip]["bleu"] # Inverse l'état de la couleur bleu pour la strip sélectionnée
        selection_strip_flash = -1 # Arrête le flash de la strip sélectionnée lorsque la couleur est changée
        logger.debug(f"Couleur bleu pour la strip {selection_strip} est maintenant {'activée' if etat_couleurs[selection_strip]['bleu'] else 'désactivée'}")

def traiter_changement_couleurs():
    if MODE_MELANGE == 'ADDITIF':
        for i in range(NB_STRIPS):
            couleurs_strip[i] = melange_additif()
    elif MODE_MELANGE == 'SOUSTRACTIF':
        for i in range(NB_STRIPS):
            couleurs_strip[i] = melange_soustractif()

def melange_additif():
    r = 255 if etat_couleurs[selection_strip]["rouge"] else 0
    g = 255 if etat_couleurs[selection_strip]["vert"] else 0
    b = 255 if etat_couleurs[selection_strip]["bleu"] else 0
    return f"#{r:02x}{g:02x}{b:02x}"

def melange_soustractif():
    if etat_couleurs[selection_strip]["rouge"] and etat_couleurs[selection_strip]["jaune"] and etat_couleurs[selection_strip]["bleu"]:
        return ALL_COULEURS["MARRON"]
    elif etat_couleurs[selection_strip]["rouge"] and etat_couleurs[selection_strip]["jaune"]:
        return ALL_COULEURS["ORANGE"]
    elif etat_couleurs[selection_strip]["jaune"] and etat_couleurs[selection_strip]["bleu"]:
        return ALL_COULEURS["VERT"]
    elif etat_couleurs[selection_strip]["rouge"] and etat_couleurs[selection_strip]["bleu"]:
        return ALL_COULEURS["VIOLET"]
    elif etat_couleurs[selection_strip]["rouge"]:
        return ALL_COULEURS["ROUGE"]
    elif etat_couleurs[selection_strip]["jaune"]:
        return ALL_COULEURS["JAUNE"]
    elif etat_couleurs[selection_strip]["bleu"]:
        return ALL_COULEURS["BLEU"]
    else:
        return COULEUR_PAR_DEFAUT
    
def gagne():
    """
    Fonction à appeler lorsque le joueur gagne l'énigme.
    Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
    """

try:
    lancer_enigme()

    button_values_temp = I2C_handler.decodeJSON(I2C_handler.getI2C()) # Lit les valeurs des boutons depuis l'ESP32 via I2C pour initialiser button_values et last_button_values avec les bonnes valeurs au démarrage de l'énigme
    if button_values_temp is not None:
        for i in range(NB_MODULES):
            if button_values_temp[i] == 1:
                button_values[i] = True
                last_button_values[i] = True
            elif button_values_temp[i] == 0:
                button_values[i] = False
                last_button_values[i] = False
            else:
                logger.warning(f"Valeur inattendue pour bouton {i} lors de l'initialisation: {button_values_temp[i]}")
                button_values[i] = True # Par défaut, on considère que les boutons sont à True si on reçoit une valeur inattendue lors de l'initialisation
                last_button_values[i] = True

        last_button_values = button_values.copy() # Assure que last_button_values est correctement initialisé avec les valeurs actuelles des boutons avant de commencer la boucle principale

    while True:
        button_values_temp = I2C_handler.decodeJSON(I2C_handler.getI2C()) # Lit les valeurs des boutons depuis l'ESP32 via I2C

        if button_values_temp is not None:
            for i in range(NB_MODULES):
                if button_values_temp[i] == 1:
                    button_values[i] = True
                elif button_values_temp[i] == 0:
                    button_values[i] = False
                else:
                    logger.warning(f"Valeur inattendue pour bouton {i}: {button_values_temp[i]}")
                    button_values[i] = True # Par défaut, on considère que les boutons sont à True si on reçoit une valeur inattendue

        if button_values != last_button_values:
            logger.debug(f"Changement détecté dans les valeurs des boutons: {button_values}")

            traiter_changement_boutons() # Traite les changements de boutons pour mettre à jour la sélection et les couleurs

            traiter_changement_couleurs() # Traite les changements de couleurs pour mettre à jour les couleurs des strips

            message = formatToESPCommande() # Formate le message à envoyer à l'ESP32 avec les nouvelles couleurs et la sélection
            I2C_handler.sendI2C(message) # Envoie le message formaté à l'ESP32 pour mettre à jour les couleurs des strips et la sélection

            nb_bonnes_strips = 0

            for i in range(NB_STRIPS):
                if couleurs_strip[i] == COULEURS_CIBLES[i]:
                    logger.debug(f"Strip {i} est dans la couleur cible {COULEURS_CIBLES[i]}")
                    nb_bonnes_strips += 1
                else:
                    pass#logger.debug(f"Strip {i} n'est pas dans la couleur cible {COULEURS_CIBLES[i]}, elle est dans la couleur {couleurs_strip[i]}")

            if nb_bonnes_strips == NB_STRIPS:
                logger.info("Toutes les strips sont dans la bonne couleur cible, l'énigme est résolue !")
                gagne()
                quit()

            last_button_values = button_values.copy()




except Exception as e:
    logger.error(f"Erreur lors du démarrage de l'énigme : {e}")

except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")

finally:
    I2C_handler.close()
    quit()