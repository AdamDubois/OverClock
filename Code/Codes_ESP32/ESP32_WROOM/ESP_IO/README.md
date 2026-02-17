# ESP32 RFID - Lecteur Multi-MFRC522

Module ESP32-C3 configuré en esclave I2C pour la lecture de plusieurs entrées numérique (switches et boutons) à l'aide d'un IO expander.

## Description

Ce projet utilise un IO expander SPI (MCP23S17) pour étendre les capacités d'entrée numérique de l'ESP32-C3. L'ESP32 agit en tant qu'esclave I2C, permettant à un maître I2C de lire l'état des entrées numériques via le bus I2C. Le MCP23S17 est configuré pour lire les entrées numériques et transmettre les données à l'ESP32, qui les formate ensuite en JSON pour une communication efficace avec le maître I2C. Ce projet est en développement, je suis en train de tester la communication entre l'ESP32 et le MCP23S17. Pour l'instant, même cette étape n'est pas fonctionnelle.

## Matériel requis

- ESP32-C3-DevKitC-02
- IO expander SPI (MCP23S17)

## Câblage

### Bus I2C (vers le maître)

| Signal | GPIO |
|--------|------|
| SDA    | 6    |
| SCL    | 7    |

### Bus SPI (vers le MCP23S17)

| Signal | GPIO |
|--------|------|
| SCK    | 4    |
| MOSI   | 10   |
| MISO   | 5    |
| RST    | 0    |

## Configuration

### Ajout de lecteurs supplémentaires

## Format de sortie JSON

## Limitations

## Dépendances

## Auteur

Adam Dubois - 2026