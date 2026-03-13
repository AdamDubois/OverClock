from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time
import json

VALEUR_SWITCHES_INIT = [True, True, False, True]

VALEUR_SWITCH_FIN = [False, True, False, False]

SEQUENCE_ATTENDUE = [0, 1, 0, 2, 2, 3, 0, 1]

valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()


ADDR_ESPIO = 0x10
ADDR_ESPNEO = 0x12
I2C_BUS = 1        # Bus I2C habituels sur Pi (bus 1 sur la plupart des modèles)

bus = SMBus(I2C_BUS)

switch_values = []
last_switch_values = []

num_sequence = 0



def test_sequence(valeur_sequence_attendue=VALEUR_SWITCHES_INIT.copy()):
    #print("Séquence attendue : 0", valeur_sequence_attendue)

    for sequence, valeur in enumerate(SEQUENCE_ATTENDUE):
        for i in range(4):
            if i == valeur:
                valeur_sequence_attendue[i] = not valeur_sequence_attendue[i]
                sequence += 1
                #print("Séquence attendue :", sequence, valeur_sequence_attendue)
                break # Passe à la prochaine valeur de la séquence attendue après avoir trouvé le switch à toggler

    if valeur_sequence_attendue == VALEUR_SWITCH_FIN:
        #print("Séquence finale correcte !")
        valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()  # Réinitialiser pour la prochaine séquence
        return

    else:
        #print("Séquence finale incorrecte.")
        quit()



def getI2C():
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
        #print("Réponse reçue:", strReceived)

        return strReceived
    
    except Exception as e:
        pass
        #print("Erreur de lecture I2C:", e)

def decodeJSON(json_str):
    """
    Décoder une chaîne JSON pour récupérer les valeurs des switchs.
    Le JSON est au format: {N:"IO",BANA0:1,BANA1:0,BANA2:1,BANA3:0,BANA4:1,BANA5:0,BANA6:1,SW3:0,BTN2:1,BTN1:0,BTN0:1,BTN3:0,BTN4:1,SW0:0,SW1:1,SW2:0}
    """
    switch_values = [False] * 4  # Liste pour stocker les valeurs des switchs
    error = False
    try:
        # Prétraitement : ajouter des guillemets autour des clés si absent
        import re
        # Ajoute des guillemets autour des clés non entourées
        json_str_corrige = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_str)
        #print("JSON corrigé pour décodage:", json_str_corrige)
        data = json.loads(json_str_corrige)
        # Extraire les valeurs des switchs
        for key, value in data.items():
            if key.startswith('N') and value != "IO":
                print("Le message n'est pas au format attendu (N doit être 'IO').")
                return None
            elif key.startswith('SW'):
                index = int(key[2:])  # Extraire l'index du switch (ex: SW3 -> 3)
                if value == 1:
                    #print(f"Switch {index} est ON")
                    switch_values[index] = True
                elif value == 0:
                    #print(f"Switch {index} est OFF")
                    switch_values[index] = False
                else:
                    print(f"Valeur inattendue pour {key}: {value}")
                    return None
    except Exception as e:
        #print("Erreur lors du décodage JSON:", e)
        error = True
    finally:
        #print("Décodage terminé.")
        if not error:
            return switch_values

try:
    test_sequence()

    message = str(0)
    data = [ord(c) for c in message]
    try:
        i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
        bus.i2c_rdwr(i2c_msg_write)
        print("Message envoyé:", message)
    except Exception as e:
        print("Erreur d'écriture I2C:", e)

    while True:
        getI2C()
        switch_values_temp = decodeJSON(getI2C())

        if switch_values_temp is not None:
            switch_values = switch_values_temp

        if switch_values != last_switch_values:
            print("Modification des switchs détectée :", switch_values)
            print("Sequence attendu :", valeur_sequence_attendue)
            last_switch_values = switch_values.copy()

            if switch_values == valeur_sequence_attendue:
                print("Séquence correcte !")

                if num_sequence >= len(SEQUENCE_ATTENDUE):
                    print("Séquence finale atteinte, félicitations !")
                    message = str(2)
                    data = [ord(c) for c in message]
                    try:
                        i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
                        bus.i2c_rdwr(i2c_msg_write)
                        print("Message envoyé:", message)
                    except Exception as e:
                        print("Erreur d'écriture I2C:", e)
                    break

                message = str(num_sequence + 3)
                data = [ord(c) for c in message]
                try:
                    i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
                    bus.i2c_rdwr(i2c_msg_write)
                    print("Message envoyé:", message)
                except Exception as e:
                    print("Erreur d'écriture I2C:", e)

                for i in range(4):
                    if i == SEQUENCE_ATTENDUE[num_sequence]:
                        valeur_sequence_attendue[i] = not valeur_sequence_attendue[i]
                        num_sequence += 1
                        break

                print("Nouvelle séquence attendu :", valeur_sequence_attendue)

            elif num_sequence != 0:
                print("Mauvaise séquence, recommencez depuis le début.")
                message = str(1)
                data = [ord(c) for c in message]
                try:
                    i2c_msg_write = i2c_msg.write(ADDR_ESPNEO, data)
                    bus.i2c_rdwr(i2c_msg_write)
                    print("Message envoyé:", message)
                except Exception as e:
                    print("Erreur d'écriture I2C:", e)

                time.sleep(1 * 5)

                num_sequence = 0
                valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()  # Réinitialiser pour la prochaine séquence
                last_switch_values = [False] * 4


        time.sleep(0.01)
        

except KeyboardInterrupt:
    print("\nFin du programme !")

finally:
    print("Fermeture du bus I2C.")
    bus.close()
    print("Programme terminé.")