from EnigmeBouton import Bouton
from Log import logger
import time

bouton = Bouton()
bouton.start()

try:
    while not bouton.gagnee:
        bouton.play()
        time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins
except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")
except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")
finally:
    bouton.close()