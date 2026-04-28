/*
Fichier : App.qml
Auteur : Jérémy Breault
Date : 2026-04-28
Description : Interface principale de l’application.

- Gère l’affichage des écrans (Idle, Énigmes, Fin)
- Contrôle la navigation selon l’état du jeu (backend)
- Affiche le timer et les données en temps réel
*/

//-------------------------------//
// Liste des imports nécessaires //
//-------------------------------//
import QtQuick         // fournit les éléments de base
import QtQuick.Window  // permet de créer une fenêtre (Window)
import "."             // accès aux composants locaux

//---------------------------------------------------------------//
//-------------- Conteneur principal l'application --------------//
//---------------------------------------------------------------//
Window {
    id: root
    width: 1280
    height: 800
    visible: true
    color: "#0F1419"
    title: "OverClock"

    // Lance l'application en plein écran
    visibility: Window.FullScreen

    // Zone couvrant tout l'écran pour cacher le curseur
    // permet de ne pas voir le curseur de la souris pendant le jeu
    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.BlankCursor
    }

    // Gestion clavier via un Item
    Item {
        id: keyHandler
        anchors.fill: parent
        focus: true

        // Quitte l'application avec la touche Échap
        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Escape) {
                Qt.quit()
            }
        }

        Component.onCompleted: forceActiveFocus() 
    }

    //---------------------------------------------//
    //-- Écran d'attente (avant le début du jeu) --//
    //---------------------------------------------//
    IdleScreen {
        anchors.fill: parent
        visible: !backend.game_start
        timeRemaining: backend.time_remaining

        // Réinitialise le timer lorsque cet écran devient visible
        onVisibleChanged: {
            if (visible) {
                backend.reset_timer()
            }
        }
    }
    
    //----------------------------------------//
    //-- Énigme 1 (affichée si enigme == 1) --//
    //----------------------------------------//
    Enigme1 {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 1

        enigme: backend.enigme
        rfidState: backend.rfid
        timeRemaining: backend.time_remaining
    }

    //----------------------------------------//
    //-- Énigme 2 (affichée si enigme == 2) --//
    //----------------------------------------//
    Enigme2 {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 2

        timeRemaining: backend.time_remaining
    }

    //----------------------------------------//
    //-- Énigme 3 (affichée si enigme == 3) --//
    //----------------------------------------//
    Enigme3 {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 3

        timeRemaining: backend.time_remaining
    }

    //----------------------------------------//
    //-- Écran de fin (enigme == 4) ----------//
    //----------------------------------------//
    FinScreen {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 4

        timeRemaining: backend.time_remaining
    }
}