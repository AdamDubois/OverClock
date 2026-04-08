import QtQuick
import QtQuick3D

Node {
    id: node

    // Resources

    // Nodes:
    Model {
        id: overClock
        objectName: "OverClock"
        source: "meshes/overClock_mesh.mesh"
        materials: [
            principledMaterial
        ]
    }

    Node {
        id: __materialLibrary__

        PrincipledMaterial {
            id: principledMaterial
            objectName: "principledMaterial"
            metalness: 1
            roughness: 1
            alphaMode: PrincipledMaterial.Opaque
        }
    }

    // Animations:
}
