from Config import *
from I2C_handler import I2C
from Log import logger
import time

class Bouton:
    def __init__(self):
        self.I2C_handler = I2C()

        self.boutons_values_temp = [None] * NB_MODULES  # Valeurs temporaires des boutons pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
        self.boutons_values = [None] * NB_MODULES  # Valeurs actuelles des boutons
        self.last_boutons_values = self.boutons_values

        print(f"Valeurs boutons de départ : {self.boutons_values}, Valeurs boutons last : {self.last_boutons_values}")


bouton = Bouton()