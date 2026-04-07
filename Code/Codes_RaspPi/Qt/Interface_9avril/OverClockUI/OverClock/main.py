import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from jsonreceive import JsonReceive


app = QGuiApplication(sys.argv)

receiver = JsonReceive()
receiver.partir_serveur()

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", receiver)

base_path = Path(__file__).resolve().parent
qml_file = base_path / "OverClockContent" / "App.qml"

engine.load(qml_file)

if not engine.rootObjects():
    print("Erreur chargement QML :", qml_file)
    sys.exit(-1)

sys.exit(app.exec())
