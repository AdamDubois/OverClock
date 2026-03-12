from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time
import json

VALEUR_SWITCHES_INIT = [1, 1, 1, 0]

SEQUENCE_ATTENDUE = [1, 2, 1, 4, 4, 3, 1, 2]

valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()

VALEUR_SWITCH_FIN = [0, 1, 1, 1]


ADDR_ESPIO = 0x10
ADDR_ESPNEO = 0x12
I2C_BUS = 1        # Bus I2C habituels sur Pi (bus 1 sur la plupart des modèles)

bus = SMBus(I2C_BUS)

switch_values = []

num_sequence = 0

for i in range(len(SEQUENCE_ATTENDUE)):
    if i == SEQUENCE_ATTENDUE[num_sequence] - 1:
        valeur_sequence_attendue[i] = not valeur_sequence_attendue[i]
        num_sequence += 1

print("Séquence attendue:", valeur_sequence_attendue)

def exit_program():
    bus.close()
    print("Programme terminé.")
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
        print("Réponse reçue:", strReceived)

        return strReceived
    
    except Exception as e:
        print("Erreur de lecture I2C:", e)

def decodeJSON(json_str):
    """
    Décoder une chaîne JSON pour récupérer les valeurs des switchs.
    Le JSON est au format: {N:"IO",BANA0:1,BANA1:0,BANA2:1,BANA3:0,BANA4:1,BANA5:0,BANA6:1,SW3:0,BTN2:1,BTN1:0,BTN0:1,BTN3:0,BTN4:1,SW0:0,SW1:1,SW2:0}
    """
    switch_values = {}  # Dictionnaire pour stocker les valeurs des switchs

    try:
        data = json.loads(json_str)
        # Extraire les valeurs des switchs
        for key, value in data.items():
            print(f"{key}: {value}")

            if key.startswith('N') and value != "IO":
                print("Le message n'est pas au format attendu (N doit être 'IO').")
                return None
            elif key.startswith('SW'):
                index = int(key[2:])  # Extraire l'index du switch (ex: SW3 -> 3)
                if value == 1:
                    print(f"Switch {index} est ON")
                    switch_values[index] = True
                elif value == 0:
                    print(f"Switch {index} est OFF")
                    switch_values[index] = False
                else:
                    print(f"Valeur inattendue pour {key}: {value}")
                    return None
                
    except Exception as e:
        print("Erreur lors du décodage JSON:", e)
        error = True

    finally:
        print("Décodage terminé.")
        if not error:
            return switch_values

try:
    if getI2C() is not None:
        switch_values = decodeJSON(getI2C())
        print("Valeurs des switchs:", switch_values)

        if switch_values is not None:
                if all(switch_values.get(i, 0) == VALEUR_SWITCHES_INIT[i] for i in range(4)):
                    print("Séquence initiale correcte !")
                else:
                    print("Séquence initiale incorrecte.")
                    exit_program()
    while True:
        getI2C()
        switch_values = decodeJSON(getI2C())
        

except KeyboardInterrupt:
    print("\nFin du programme !")

finally:
    exit_program()