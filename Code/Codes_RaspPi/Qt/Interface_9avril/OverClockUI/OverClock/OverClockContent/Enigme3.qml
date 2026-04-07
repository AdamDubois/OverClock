import QtQuick

Rectangle {
    id: root
    anchors.fill: parent
    color: "#0F1419"

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
        color: root.timeRemaining <= 60 ? "#ff0000" : "#ff3b3b"
        font.pixelSize: 42
        font.bold: true
        font.family: "Courier New"
    }

    Text {
        anchors.centerIn: parent
        text: "ÉNIGME 3"
        color: "#E6EDF3"
        font.pixelSize: 44
        font.bold: true
    }
}
