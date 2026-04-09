from Log import logger
from smbus2 import SMBus, i2c_msg
import socket

ui_message = str{{
    "game_start" : False,
    "enigme" : 0,
    "rfid" : [False, False, False, False],
}}

message = str({"E":1,"Selected":-1,"S0":"#000000","S1":"#000000","S2":"#000000","S3":"#000000","S4":"#000000"}) 
data = [ord(c) for c in message]
try:
    i2c_msg_write = i2c_msg.write(0x12, data)
    bus = SMBus(1)
    bus.i2c_rdwr(i2c_msg_write)
    logger.debug(f"[I2C_handle : sendI2C] Message envoyé via I2C : {message}")
except Exception as e:
    logger.error(f"[I2C_handle : sendI2C] Erreur d'écriture I2C: {e}")

message = str({"E":2,"Etape":12}) # Message à envoyer pour éteindre toutes les DELs
data = [ord(c) for c in message]
try:
    i2c_msg_write = i2c_msg.write(0x12, data)
    bus = SMBus(1)
    bus.i2c_rdwr(i2c_msg_write)
    logger.debug(f"[I2C_handle : sendI2C] Message envoyé via I2C : {message}")
except Exception as e:
    logger.error(f"[I2C_handle : sendI2C] Erreur d'écriture I2C: {e}")

bus.close()

rfid = None
bouton = None
switchs = None


try:
    from RFID.RFID import RFID
    rfid = RFID()
    while not rfid.fini:
        rfid.play()

    from Bouton.EnigmeBouton import Bouton
    bouton = Bouton()
    bouton.start()

    while not bouton.gagnee:
        bouton.play()

    from Switchs.Switchs import Switchs
    switchs = Switchs()
    switchs.lancer_enigme()

    while not switchs.termine:
        switchs.main()

except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")
except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")
finally:
    if rfid is not None:
        rfid.close()
    if bouton is not None:
        bouton.close()
    if switchs is not None:
        switchs.close()