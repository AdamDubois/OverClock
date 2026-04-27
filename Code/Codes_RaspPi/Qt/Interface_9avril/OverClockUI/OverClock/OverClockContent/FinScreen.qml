/*
Fichier : FinScreen.qml
Description : Écran de fin du jeu.

- Affiche un message de réussite (désamorçage terminé)
- Présente le temps restant
- Ajoute des effets visuels (scan, glow, animation)
*/


import QtQuick
import Qt5Compat.GraphicalEffects

Rectangle {
    id: root
    anchors.fill: parent
    color: "#0A0F0A"

    property int timeRemaining: 0

    // Convertit un temps en secondes au format MM:SS
    function formatTime(seconds) {
        var min = Math.floor(seconds / 60)
        var sec = seconds % 60
        return min.toString().padStart(2, "0") + ":" +
               sec.toString().padStart(2, "0")
    }

    // Ligne scan
    Rectangle {
        width: parent.width
        height: 2
        color: "#4CAF75"
        opacity: 0.15

        SequentialAnimation on y {
            loops: Animation.Infinite
            NumberAnimation { from: 0; to: parent.height; duration: 2500 }
        }
    }

    // TIMER
    Text {
        x: 40
        y: 40
        text: root.formatTime(root.timeRemaining)
        color: "#4CAF75"
        font.pixelSize: 42
        font.bold: true
        font.family: "Courier New"

        scale: 1.0 + Math.sin(Date.now()/300) * 0.02

        layer.enabled: true
        layer.effect: DropShadow {
            color: "#4CAF75"
            radius: 16
            samples: 12
        }
    }

    // TITRE PRINCIPAL
    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 280

        text: "MODULE DÉSAMORCÉ"
        color: "#4CAF75"
        font.pixelSize: 50
        font.bold: true

        layer.enabled: true
        layer.effect: DropShadow {
            color: "#4CAF75"
            radius: 20
            samples: 16
        }
    }

    // SOUS-TEXTE
    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 350

        text: "Mission accomplie"
        color: "#E6EDF3"
        font.pixelSize: 26
    }

    // TEXTE TECHNIQUE
    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 400

        text: "Système sécurisé • Aucun incident détecté"
        color: "#4CAF75"
        font.pixelSize: 18
        opacity: 0.6
    }

    // BARRE DE COMPLETION
    Rectangle {
        width: parent.width * 0.5
        height: 6
        anchors.horizontalCenter: parent.horizontalCenter
        y: 460
        radius: 3
        color: "#1E2A1E"

        Rectangle {
            width: parent.width
            height: parent.height
            radius: 3
            color: "#4CAF75"
        }
    }
}
