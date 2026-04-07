import QtQuick

Rectangle {
    anchors.fill: parent
    color: "black"

    property int timeRemaining: 0

    Image {
        id: overClock_Logo
        anchors.centerIn: parent
        source: "images/OverClock_Logo.png"
        fillMode: Image.PreserveAspectFit
        width: 500
        height: 220
        opacity: 1.0
    }

    Timer {
        id: lightTimer
        interval: 50
        running: true
        repeat: true

        property int step: 0

        onTriggered: {
            if (step < 5) {
                // descente rapide (extinction)
                overClock_Logo.opacity -= 0.15
            } else if (step < 10) {
                // montée rapide (allumage)
                overClock_Logo.opacity += 0.15
            } else if (step < 40) {
                // pause (lumière stable)
            } else {
                step = -1
            }

            // clamp sécurité
            if (overClock_Logo.opacity < 0) overClock_Logo.opacity = 0
            if (overClock_Logo.opacity > 1) overClock_Logo.opacity = 1

            step++
        }
    }
}
