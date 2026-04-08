import QtQuick
import QtQuick.Controls
import QtQuick.Timeline 1.0

Rectangle {
    id: root
    width: 1280
    height: 800
    color: "#140d0d"

    property int timeRemaining: 0

    function formatTime(seconds) {
        var min = Math.floor(seconds / 60)
        var sec = seconds % 60
        return min.toString().padStart(2, "0") + ":" +
               sec.toString().padStart(2, "0")
    }

    Rectangle {
        anchors.fill: parent
        color: "transparent"
        border.width: 2
        border.color: "#3a2727"

        Rectangle {
            x: 10; y: 10
            width: 911; height: 40
            color: "#161C22"
            border.color: "#27313A"; border.width: 1
        }

        Rectangle {
            x: 933; y: 10
            width: 337; height: 40
            color: "#161C22"
            border.color: "#27313A"; border.width: 1
        }

        Text {
            x: 15; y: 10
            text: "TERMINAL : OverClock"
            font.pixelSize: 26
            font.bold: true
            color: "#E6EDF3"
        }

        Text {
            x: 944; y: 13
            text: "SYS STATUS :"
            font.pixelSize: 24
            font.bold: true
            color: "#ff0000"
        }

        Text {
            x: 1116; y: 13
            text: "HORS LIGNE"
            font.pixelSize: 24
            font.bold: true
            color: "#ff0000"
            visible: true
        }

        Rectangle {
            id: terminalWindow
            x: 320; y: 225
            width: 639; height: 397
            color: "#161C22"
            border.width: 2
            border.color: "#ff3b3b"
            radius: 6
            opacity: 1

            Text {
                anchors.fill: parent
                anchors.margins: 16
                text: ""
                color: "#ff0000"
                font.pixelSize: 18
                font.family: "Courier New"
                wrapMode: Text.Wrap
            }
        }

        Image {
            id: image
            x: 0; y: 25
            width: 1278; height: 796
            source: "../../../../Pictures/CadenasRouge.png"
            fillMode: Image.PreserveAspectFit
            visible: true

            Text {
                x: 307; y: 601
                text: "Confirmation de l’identité requise"
                color: "#ff0000"
                font.pixelSize: 45
            }

            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                y: 673
                spacing: 40

                Repeater {
                    model: 4
                    Rectangle {
                        width: 70; height: 70
                        radius: 10
                        border.width: 3
                        border.color: "#3A3A3A"
                        color: "#3A1A1A"
                    }
                }
            }
        }

        Text {
            id: text1
            x: 321; y: 648
            text: "SYSTEM BOOT"
            color: "#8B949E"
            font.pixelSize: 16
            font.bold: true
            visible: false
        }

        Text {
            x: 889; y: 648
            visible: false
            text: "90%"
            color: "#00b4ff"
            font.pixelSize: 16
            font.bold: true
        }

        Rectangle {
            id: rectangle
            x: 321; y: 680
            width: 638; height: 24
            radius: 4
            color: "#161C22"
            border.width: 1
            border.color: "#27313A"
            visible: false
            opacity: 1

            Rectangle {
                width: parent.width * 0.9
                height: parent.height
                radius: 4
                color: "#ff0000"
            }
        }
    }

    // TIMER (ajout correct pour Timeline)
    Text {
        id: textTimer
        x: 40
        y: 100
        width: 220
        height: 80
        text: root.formatTime(root.timeRemaining)
        color: "#ff0000"
        font.pixelSize: 42
        font.bold: true
        font.family: "Courier New"

        visible: false
        opacity: 0
    }

    // TIMELINE
    Timeline {
        id: timeline
        enabled: true
        startFrame: 0
        endFrame: 2000

        animations: [
            TimelineAnimation {
                running: true
                from: 0
                to: 1200
                duration: 10000
            }
        ]

        // apparition du timer à frame 100
        KeyframeGroup {
            target: textTimer
            property: "visible"

            Keyframe { frame: 0; value: false }
            Keyframe { frame: 99; value: false }
            Keyframe { frame: 100; value: true }
        }

        // fade-in
        KeyframeGroup {
            target: textTimer
            property: "opacity"

            Keyframe { frame: 0; value: 0 }
            Keyframe { frame: 100; value: 0 }
            Keyframe { frame: 140; value: 1 }
        }

        KeyframeGroup {
            target: rectangle
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }
        }

        KeyframeGroup {
            target: text1
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }
        }
    }
}
