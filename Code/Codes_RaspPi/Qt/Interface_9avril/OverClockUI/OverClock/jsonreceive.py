import socket
import threading
import json
import time

from PySide6.QtCore import QObject, Property, Signal, Slot

HOST = "0.0.0.0"
PORT = 5000


class JsonReceive(QObject):
    gameStartChanged = Signal()
    enigmeChanged = Signal()
    rfidChanged = Signal()
    timeRemainingChanged = Signal()

    def __init__(self):
        super().__init__()

        self._game_start = False
        self._enigme = 0
        self._rfid = [False, False, False, False]
        self._time_remaining = 900

        self._running = False
        self._timer_running = True
        self._lock = threading.Lock()

        timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        timer_thread.start()

    @Property(bool, notify=gameStartChanged)
    def game_start(self):
        return self._game_start

    @Property(int, notify=enigmeChanged)
    def enigme(self):
        return self._enigme

    @Property("QVariantList", notify=rfidChanged)
    def rfid(self):
        return self._rfid

    @Property(int, notify=timeRemainingChanged)
    def time_remaining(self):
        return self._time_remaining

    @Slot()
    def reset_timer(self):
        with self._lock:
            self._time_remaining = 900
        self.timeRemainingChanged.emit()
        print("[TIMER] reset à 900")

    @Slot(int)
    def set_timer(self, value):
        with self._lock:
            self._time_remaining = max(0, int(value))
        self.timeRemainingChanged.emit()
        print(f"[TIMER] nouvelle valeur : {self._time_remaining}")

    def partir_serveur(self):
        if self._running:
            return
        self._running = True
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()

    def arrêter_serveur(self):
        self._running = False
        self._timer_running = False

    def _run_timer(self):
        while self._timer_running:
            time.sleep(1)

            emit_needed = False

            with self._lock:
                if self._game_start and self._time_remaining > 0:
                    self._time_remaining -= 1
                    emit_needed = True
                    current_time = self._time_remaining

            if emit_needed:
                self.timeRemainingChanged.emit()
                print(f"[TIMER] {current_time}")

    def _run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(5)

            print(f"Serveur JSON en écoute sur {HOST}:{PORT}")

            while self._running:
                try:
                    conn, addr = server.accept()
                except OSError:
                    break

                with conn:
                    raw = conn.recv(4096)
                    if not raw:
                        continue

                    message_str = raw.decode("utf-8").strip()
                    if not message_str:
                        continue

                    for line in message_str.split("\n"):
                        line = line.strip()
                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError:
                            print("JSON invalide :", line)
                            continue

                        self._update_values(data)

    def _update_values(self, data):
        if "game_start" in data:
            new_game_start = bool(data["game_start"])
            if self._game_start != new_game_start:
                self._game_start = new_game_start
                self.gameStartChanged.emit()
                print(f"[GAME_START] {self._game_start}")

        if "enigme" in data:
            enigme = int(data["enigme"])
            if self._enigme != enigme:
                self._enigme = enigme
                self.enigmeChanged.emit()
                print(f"[ENIGME] {self._enigme}")

        if "rfid" in data:
            rfid = list(data["rfid"])
            if len(rfid) == 4:
                rfid = [bool(x) for x in rfid]
                if self._rfid != rfid:
                    self._rfid = rfid
                    self.rfidChanged.emit()
                    print(f"[RFID] {self._rfid}")