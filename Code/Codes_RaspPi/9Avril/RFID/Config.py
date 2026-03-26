#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Config.py
Description: """
__author__ = "Adam Dubois"
__version__ = "1.0.1"
__date__ = ""
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Configuration  de  l'énigme                                                                                                           #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# Le but est de mettre les cartes RFID dans le bon ordre sur les 4 lecteurs RFID
# Les ID des cartes sont les suivants (Les noms de référence de carte peuvent être changés)
ID_CARTE_9 = "264D5C42"
ID_CARTE_3 = "C64C5C42"
ID_CARTE_4 = "F64C5C42"
ID_CARTE_1 = "164C5C42"

SOLUTION = "9341"

SOLUTION_READER0 = ID_CARTE_9
SOLUTION_READER1 = ID_CARTE_3
SOLUTION_READER2 = ID_CARTE_4
SOLUTION_READER3 = ID_CARTE_1



#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Configuration logicielle                                                                                                              #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# Debug mode configuration
DEBUG_MODE = True  # Change to False to disable debug messages

# I2C Configuration
ADDR_ESPRFID = 0x11
ADDR_ESPNEO = 0x12



#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Hardware component pin definitions                                                                                                    #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# I2C Configuration
I2C_BUS_NUMBER = 1 # Bus I2C habituel sur les Raspberry Pi (bus 1 sur la plupart des modèles pins GPIO 2 (SDA) et GPIO 3 (SCL))