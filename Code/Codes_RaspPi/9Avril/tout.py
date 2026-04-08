from Bouton.EnigmeBouton import Bouton
from RFID.RFID import RFID
from Log import logger

rfid = RFID()


try:
    while not rfid.fini:
        rfid.play()

    bouton = Bouton()
    bouton.start()

    while not bouton.gagnee:
        bouton.play()

except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")
except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")
finally:
    rfid.close()
    bouton.close()