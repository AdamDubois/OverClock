import QtQuick
import QtQuick.Window
import "."

Window {
    id: root
    width: 1280
    height: 800
    visible: true
    color: "#0F1419"
    title: "OverClock"
	
    visibility: Window.FullScreen

    IdleScreen {
        anchors.fill: parent
        visible: !backend.game_start
        timeRemaining: backend.time_remaining

        onVisibleChanged: {
            if (visible) {
                backend.reset_timer()
            }
        }
    }

    Enigme1 {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 1

        enigme: backend.enigme
        rfidState: backend.rfid
        timeRemaining: backend.time_remaining
    }

    Enigme2 {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 2

        timeRemaining: backend.time_remaining
    }

    Enigme3 {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 3

        timeRemaining: backend.time_remaining
    }

    FinScreen {
        anchors.fill: parent
        visible: backend.game_start && backend.enigme === 4

        timeRemaining: backend.time_remaining
    }
}