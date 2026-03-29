# ESP32 IO - Lecteur d'entrées numériques via MCP23S17

Module ESP32-C3 configuré en esclave I2C pour la lecture de plusieurs entrées numériques (switches et boutons) à l'aide d'un IO expander MCP23S17.

## Description

Ce projet utilise un IO expander SPI (MCP23S17) connecté à un ESP32-C3. L'ESP32 agit comme esclave I2C et, sur demande du maître, lit l'état des entrées numériques connectées au MCP23S17 et renvoie leurs états au format JSON.

## Matériel requis

- ESP32-C3-DevKitC-02
- IO expander MCP23S17
- Switches, boutons et/ou connecteurs bananes (selon configuration)

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
| CS     | 3    |
| RST    | 0    |

### Configuration des entrées MCP23S17

Le MCP23S17 dispose de 16 broches GPIO configurables (GPA0-GPA7 et GPB0-GPB7). Par défaut, toutes sont configurées en `INPUT_PULLUP` et associées à des entrées :

| Pin ID | Pin Name | Type         | Nom JSON |
|--------|----------|--------------|----------|
| 0      | GPA0     | INPUT_PULLUP | BANA0    |
| 1      | GPA1     | INPUT_PULLUP | BANA1    |
| 2      | GPA2     | INPUT_PULLUP | BANA2    |
| 3      | GPA3     | INPUT_PULLUP | BANA3    |
| 4      | GPA4     | INPUT_PULLUP | BANA4    |
| 5      | GPA5     | INPUT_PULLUP | BANA5    |
| 6      | GPA6     | INPUT_PULLUP | BANA6    |
| 7      | GPA7     | INPUT_PULLUP | SW3      |
| 8      | GPB0     | INPUT_PULLUP | BTN2     |
| 9      | GPB1     | INPUT_PULLUP | BTN1     |
| 10     | GPB2     | INPUT_PULLUP | BTN0     |
| 11     | GPB3     | INPUT_PULLUP | BTN3     |
| 12     | GPB4     | INPUT_PULLUP | BTN4     |
| 13     | GPB5     | INPUT_PULLUP | SW0      |
| 14     | GPB6     | INPUT_PULLUP | SW1      |
| 15     | GPB7     | INPUT_PULLUP | SW2      |

## Configuration

Tous les paramètres sont dans `include/config.h` :

- `SLAVE_ADDR` : Adresse I2C de l'esclave (défaut: `0x10`)
- `ESP32_NAME` : Nom de l'ESP32 pour l'identification (défaut: `"IO"`)
- `DEBUG_MODE` : Active/désactive les logs série
- `NB_INPUTS` : Nombre total d'entrées numériques
- `NB_OUTPUTS` : Nombre total de sorties (non implémenté dans le code actuel)
- Broches I2C, SPI et configuration du MCP23S17

### Personnalisation des entrées

1. **Modifier le type de broche** : Dans `config.h`, ajustez le tableau `TYPE_PIN[]` pour définir chaque broche comme `INPUT`, `INPUT_PULLUP`, `INPUT_PULLDOWN` ou `OUTPUT`.

2. **Renommer les entrées** : Modifiez le tableau `NAME_INPUTS[]` pour personnaliser les noms utilisés dans le JSON (par exemple, changer `"BTN0"` en `"StartButton"`).

3. **Ajuster le nombre d'entrées** : Modifiez `NB_INPUTS`, `NB_OUTPUTS` et `NB_INUTILISEES` selon votre configuration. La somme doit toujours égaler 16.

## Format de sortie JSON

```json
{N:"IO",BANA0:1,BANA1:0,BANA2:1,BANA3:0,BANA4:1,BANA5:0,BANA6:1,SW3:0,BTN2:1,BTN1:0,BTN0:1,BTN3:0,BTN4:1,SW0:0,SW1:1,SW2:0}
```

- `N` : Nom de l'ESP32
- Chaque entrée : État de l'entrée (`0` pour LOW, `1` pour HIGH)

## Limitations

- L'ESP32, sans modification, ne peut pas envoyer plus de 128 octets en une seule transmission I2C. Le nombre maximal d'entrées dépend donc de la longueur de leurs noms.
- Les sorties (`OUTPUT`) ne sont pas gérées nativement dans le code actuel. Une modification du code est nécessaire pour les utiliser.

## Dépendances

- [Adafruit MCP23017 Arduino Library](https://github.com/adafruit/Adafruit-MCP23017-Arduino-Library)
- [Adafruit NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel)

## État du projet

**En développement** : Ce projet est terminé et fonctionnel. Cependant, la documentation est encore en cours de rédaction et peut être mise à jour pour plus de clarté et de détails.

## Auteur

Adam Dubois - 2026-02-22