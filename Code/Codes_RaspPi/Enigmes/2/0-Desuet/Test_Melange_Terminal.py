# Choisir le mode de mélange : 'ADDITIF' ou 'SOUSTRACTIF'
MODE_MELANGE = 'SOUSTRACTIF'

import time

# Couleurs de base
NOIR = [0, 0, 0]
ROUGE = [255, 0, 0]
JAUNE = [255, 255, 0]
BLEU = [0, 0, 255]
VERT = [0, 255, 0]
BLANC = [255, 255, 255]
ORANGE = [255, 128, 0]
VIOLET = [128, 0, 128]
MARRON = [128, 64, 0]

# Définir la couleur par défaut en mode soustractif : 'NOIR' ou 'BLANC'
COULEUR_PAR_DEFAUT_SOUSTRACTIF = BLANC  # ou NOIR

# Système toggle pour chaque composante
etat_rouge = False
etat_jaune = False
etat_bleu = False
etat_vert = False  # utilisé seulement pour l'additif

# Index de la strip
index_strip = 0

# Liste des couleurs des strips
strips_colors = []

# Fonction pour le mélange additif
def melange_additif(rouge, vert, bleu):
    r = 255 if rouge else 0
    g = 255 if vert else 0
    b = 255 if bleu else 0
    return [r, g, b]

# Fonction pour le mélange soustractif
def melange_soustractif(rouge, jaune, bleu):
    if rouge and jaune and bleu:
        return MARRON  # ou NOIR selon préférence
    elif rouge and jaune:
        return ORANGE
    elif jaune and bleu:
        return VERT
    elif rouge and bleu:
        return VIOLET
    elif rouge:
        return ROUGE
    elif jaune:
        return JAUNE
    elif bleu:
        return BLEU
    else:
        return COULEUR_PAR_DEFAUT_SOUSTRACTIF

# Fonction pour changer la couleur de la strip
def set_strip_color(index, color):
    if index < len(strips_colors):
        strips_colors[index] = color
    else:
        # Ajouter des strips si l'index dépasse la taille actuelle
        while len(strips_colors) <= index:
            strips_colors.append(NOIR)
        strips_colors[index] = color
    print(f"Couleur du strip {index} changée: {color}")
    afficher_couleurs_strips()

# Fonction pour afficher les couleurs de toutes les strips
def afficher_couleurs_strips():
    print("Couleurs des strips :")
    for i, color in enumerate(strips_colors):
        print(f"Strip {i}: {color}")

# Initialiser les couleurs des strips
for _ in range(5):  # Supposons qu'il y ait 5 strips
    strips_colors.append(COULEUR_PAR_DEFAUT_SOUSTRACTIF)

try:
    while True:
        print("Appuyez sur une touche :")
        print("1: Bouton noir (descend index)")
        print("2: Bouton blanc (monte index)")
        print("3: Bouton rouge")
        print("4: Bouton jaune")
        print("5: Bouton bleu")
        touche = input("Votre choix: ")

        if touche == "1":
            if index_strip == 0:
                index_strip = len(strips_colors) - 1  # Remonter au plus haut index
            else:
                index_strip -= 1
            print(f"Index de la strip: {index_strip}")
        elif touche == "2":
            if index_strip == len(strips_colors) - 1:
                index_strip = 0  # Revenir au plus bas index
            else:
                index_strip += 1
            print(f"Index de la strip: {index_strip}")
        elif touche == "3":
            etat_rouge = not etat_rouge
            print(f"État rouge: {etat_rouge}")
            if MODE_MELANGE == 'ADDITIF':
                couleur_finale = melange_additif(etat_rouge, etat_vert, etat_bleu)
            else:
                couleur_finale = melange_soustractif(etat_rouge, etat_jaune, etat_bleu)
            set_strip_color(index_strip, couleur_finale)

        elif touche == "4":
            etat_jaune = not etat_jaune
            print(f"État jaune: {etat_jaune}")
            if MODE_MELANGE == 'ADDITIF':
                couleur_finale = melange_additif(etat_rouge, etat_vert, etat_bleu)
            else:
                couleur_finale = melange_soustractif(etat_rouge, etat_jaune, etat_bleu)
            set_strip_color(index_strip, couleur_finale)

        elif touche == "5":
            etat_bleu = not etat_bleu
            print(f"État bleu: {etat_bleu}")
            if MODE_MELANGE == 'ADDITIF':
                couleur_finale = melange_additif(etat_rouge, etat_vert, etat_bleu)
            else:
                couleur_finale = melange_soustractif(etat_rouge, etat_jaune, etat_bleu)
            set_strip_color(index_strip, couleur_finale)
        else:
            print("Touche invalide.")

        print(f"Index actuellement sélectionné: {index_strip}")
except KeyboardInterrupt:
    print("Programme arrêté.")