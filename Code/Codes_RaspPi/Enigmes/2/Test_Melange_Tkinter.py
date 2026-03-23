import tkinter as tk
from tkinter import messagebox

# Choisir le mode de mélange : 'ADDITIF' ou 'SOUSTRACTIF'
MODE_MELANGE = 'ADDITIF'

# Couleurs de base
NOIR = "#000000"
ROUGE = "#FF0000"
JAUNE = "#FFFF00"
BLEU = "#0000FF"
VERT = "#00FF00"
BLANC = "#FFFFFF"
ORANGE = "#FF8000"
VIOLET = "#800080"
MARRON = "#804000"

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

# Initialiser les couleurs des strips
for _ in range(5):  # Supposons qu'il y ait 5 strips
    strips_colors.append(COULEUR_PAR_DEFAUT_SOUSTRACTIF)

# Ajouter une liste pour stocker les états des couleurs de chaque strip
strip_states = [{"rouge": False, "jaune": False, "bleu": False, "vert": False} for _ in range(5)]

# Fonction pour le mélange additif
def melange_additif(rouge, vert, bleu):
    r = 255 if rouge else 0
    g = 255 if vert else 0
    b = 255 if bleu else 0
    return f"#{r:02x}{g:02x}{b:02x}"

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
    strips_colors[index] = color
    strip_labels[index].config(bg=color)

# Fonction pour mettre à jour la couleur en fonction des états
def update_color():
    if MODE_MELANGE == 'ADDITIF':
        couleur_finale = melange_additif(etat_rouge, etat_vert, etat_bleu)
    else:
        couleur_finale = melange_soustractif(etat_rouge, etat_jaune, etat_bleu)
    set_strip_color(index_strip, couleur_finale)
    update_button_colors()

# Fonction pour mettre à jour les couleurs des boutons
def update_button_colors():
    btn_rouge.config(bg=ROUGE if etat_rouge else "SystemButtonFace")
    btn_jaune.config(bg=JAUNE if etat_jaune else "SystemButtonFace")
    btn_bleu.config(bg=BLEU if etat_bleu else "SystemButtonFace")

# Déplacer les définitions des fonctions des boutons avant la création des boutons

def bouton_noir():
    global index_strip, etat_rouge, etat_jaune, etat_bleu, etat_vert
    # Sauvegarder l'état actuel de la strip
    strip_states[index_strip] = {
        "rouge": etat_rouge,
        "jaune": etat_jaune,
        "bleu": etat_bleu,
        "vert": etat_vert
    }
    # Changer d'index
    index_strip = (index_strip - 1) % len(strips_colors)
    index_label.config(text=f"Index: {index_strip}")
    # Restaurer l'état de la nouvelle strip
    etat_rouge = strip_states[index_strip]["rouge"]
    etat_jaune = strip_states[index_strip]["jaune"]
    etat_bleu = strip_states[index_strip]["bleu"]
    etat_vert = strip_states[index_strip]["vert"]
    update_color()

def bouton_blanc():
    global index_strip, etat_rouge, etat_jaune, etat_bleu, etat_vert
    # Sauvegarder l'état actuel de la strip
    strip_states[index_strip] = {
        "rouge": etat_rouge,
        "jaune": etat_jaune,
        "bleu": etat_bleu,
        "vert": etat_vert
    }
    # Changer d'index
    index_strip = (index_strip + 1) % len(strips_colors)
    index_label.config(text=f"Index: {index_strip}")
    # Restaurer l'état de la nouvelle strip
    etat_rouge = strip_states[index_strip]["rouge"]
    etat_jaune = strip_states[index_strip]["jaune"]
    etat_bleu = strip_states[index_strip]["bleu"]
    etat_vert = strip_states[index_strip]["vert"]
    update_color()

def bouton_rouge():
    global etat_rouge
    etat_rouge = not etat_rouge
    update_color()

def bouton_jaune():
    global etat_jaune
    etat_jaune = not etat_jaune
    update_color()

def bouton_bleu():
    global etat_bleu
    etat_bleu = not etat_bleu
    update_color()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Mélange de Couleurs")

# Boutons de contrôle
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Recréer les boutons avec leurs couleurs respectives et s'assurer qu'ils sont bien ajoutés à l'interface
btn_noir = tk.Button(control_frame, text="Bouton Noir", command=bouton_noir, bg=NOIR, fg="white")
btn_noir.grid(row=0, column=0, padx=5)

btn_blanc = tk.Button(control_frame, text="Bouton Blanc", command=bouton_blanc, bg=BLANC)
btn_blanc.grid(row=0, column=1, padx=5)

btn_rouge = tk.Button(control_frame, text="Bouton Rouge", command=bouton_rouge, bg=ROUGE, fg="white")
btn_rouge.grid(row=0, column=2, padx=5)

btn_jaune = tk.Button(control_frame, text="Bouton Jaune", command=bouton_jaune, bg=JAUNE)
btn_jaune.grid(row=0, column=3, padx=5)

btn_bleu = tk.Button(control_frame, text="Bouton Bleu", command=bouton_bleu, bg=BLEU, fg="white")
btn_bleu.grid(row=0, column=4, padx=5)

# Appeler update_button_colors après la création des boutons pour initialiser leurs couleurs
update_button_colors()

# Affichage de l'index sélectionné
index_label = tk.Label(root, text=f"Index: {index_strip}")
index_label.pack(pady=10)

# Affichage des strips
strips_frame = tk.Frame(root)
strips_frame.pack(pady=10)

strip_labels = []
for i in range(5):
    label = tk.Label(strips_frame, text=f"Strip {i}", bg=strips_colors[i], width=20, height=2)
    label.grid(row=0, column=i, padx=5)
    strip_labels.append(label)

# Lancement de la boucle principale
root.mainloop()