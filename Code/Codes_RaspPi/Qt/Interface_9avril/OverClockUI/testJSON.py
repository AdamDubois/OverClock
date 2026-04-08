import socket
import json

HOST = "127.0.0.1"
PORT = 5000

rfid = [0, 0, 0, 0]
enigme = 0
game_start = False

def send_state():
    data = {
        "game_start": game_start,
        "enigme": enigme,
        "rfid": rfid,
    }

    message = json.dumps(data) + "\n"

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.sendall(message.encode("utf-8"))
        client.close()
        print(f"Envoyé -> game_start: {game_start}, enigme: {enigme}, rfid: {rfid}")
    except Exception as e:
        print("Erreur :", e)

print("Contrôles :")
print("g → toggle game_start")
print("0-9 → changer enigme")
print("r1 r2 r3 r4 → toggle RFID")
print("reset → reset RFID")
print("q → quitter")

send_state()

while True:
    key = input(">> ").strip().lower()

    if key == "q":
        break

    elif key == "g":
        game_start = not game_start

    elif key.isdigit():
        enigme = int(key)

    elif key in ["r1", "r2", "r3", "r4"]:
        index = int(key[1]) - 1
        rfid[index] = 0 if rfid[index] == 1 else 1

    elif key == "reset":
        rfid = [0, 0, 0, 0]

    else:
        print("Commande invalide")
        continue

    send_state()