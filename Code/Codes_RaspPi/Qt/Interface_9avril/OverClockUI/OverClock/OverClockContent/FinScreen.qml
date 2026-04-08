import QtQuick

Rectangle {
    id: root
    anchors.fill: parent
    color: "#0A0F0A"

    property int timeRemaining: 0

    function formatTime(seconds) {
        var min = Math.floor(seconds / 60)
        var sec = seconds % 60
        return min.toString().padStart(2, "0") + ":" +
               sec.toString().padStart(2, "0")
    }

    Text {
        x: 40
        y: 40
        text: root.formatTime(root.timeRemaining)
        color: "#4CAF75"
        font.pixelSize: 42
        font.bold: true
        font.family: "Courier New"
    }

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 280
        text: "MODULE DÉSACTIVÉ"
        color: "#4CAF75"
        font.pixelSize: 52
        font.bold: true
    }

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 360
        text: "Mission accomplie"
        color: "#E6EDF3"
        font.pixelSize: 28
    }
}
