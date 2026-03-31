from EnigmeBouton_V2 import Bouton
import time

bouton = Bouton()
bouton.I2C_handler.sendI2C(bouton.formatToESPCommande())

try:
    while not bouton.gagnee:
        bouton.play()
        time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins

except Exception as e:
    print(f"Erreur inattendue dans le programme principal: {e}")

except KeyboardInterrupt:
    print("Programme interrompu par l'utilisateur.")

finally:
    bouton.close()