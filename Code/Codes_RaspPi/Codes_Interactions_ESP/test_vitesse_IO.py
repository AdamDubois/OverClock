# Test boucle : lecture I2C, parsing JSON, extraction SW/BTN/BANA, mesure du temps à chaque itération
from smbus2 import SMBus, i2c_msg  # sudo pip install smbus2
import time
import json
import re

ADDR_ESPIO = 0x10  # Adresse I2C de l'ESPIO

def getI2C(bus):
    try:
        strReceived = ""
        response = i2c_msg.read(ADDR_ESPIO, 256)
        bus.i2c_rdwr(response)
        for value in response:
            if value == 0x00:
                break
            strReceived += chr(value)
        return strReceived
    except Exception as e:
        print(f"[getI2C] Erreur de lecture I2C: {e}")
        return None

if __name__ == "__main__":
    bus = SMBus(1)
    try:
        print("Appuyez sur Ctrl+C pour arrêter la boucle.")
        while True:
            t0 = time.perf_counter()
            strReceived = getI2C(bus)
            t1 = time.perf_counter()
            if strReceived is not None:
                print(f"\nRéponse I2C brute : {strReceived}")
                # Correction JSON et parsing
                json_str_corrige = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', strReceived)
                try:
                    data = json.loads(json_str_corrige)
                    sw = {k: v for k, v in data.items() if k.startswith('SW')}
                    btn = {k: v for k, v in data.items() if k.startswith('BTN')}
                    bana = {k: v for k, v in data.items() if k.startswith('BANA')}
                    print(f"SW: {sw}")
                    print(f"BTN: {btn}")
                    print(f"BANA: {bana}")
                except Exception as e:
                    print(f"Erreur parsing JSON: {e}")
            else:
                print("Aucune donnée reçue via I2C.")
            print(f"Durée totale (lecture + parsing): {t1-t0:.6f} secondes")
            time.sleep(0.2)  # Petite pause pour éviter de spammer le bus
    except KeyboardInterrupt:
        print("\nArrêt de la boucle.")
    finally:
        bus.close()