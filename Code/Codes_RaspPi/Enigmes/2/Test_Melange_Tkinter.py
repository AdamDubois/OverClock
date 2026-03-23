import tkinter as tk

# Choisir le mode de mélange : 'ADDITIF' ou 'SOUSTRACTIF'
MODE_MELANGE = 'SOUSTRACTIF'

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

COULEUR_PAR_DEFAUT_SOUSTRACTIF = BLANC
COULEUR_PAR_DEFAUT_ADDITIF = NOIR

etat_rouge = False
etat_jaune = False
etat_bleu = False
etat_vert = False  # utilisé seulement pour l'additif

index_strip = 0
strips_colors = []
for _ in range(5):
    if MODE_MELANGE == 'ADDITIF':
        strips_colors.append(COULEUR_PAR_DEFAUT_ADDITIF)
    else:
        strips_colors.append(COULEUR_PAR_DEFAUT_SOUSTRACTIF)

strip_states = [{"rouge": False, "jaune": False, "bleu": False, "vert": False} for _ in range(5)]

def melange_additif(rouge, vert, bleu):
    r = 255 if rouge else 0
    g = 255 if vert else 0
    b = 255 if bleu else 0
    return f"#{r:02x}{g:02x}{b:02x}"

def melange_soustractif(rouge, jaune, bleu):
    if rouge and jaune and bleu:
        return MARRON
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

def set_strip_color(index, color):
    strips_colors[index] = color
    strip_labels[index].config(bg=color)

def update_button_colors():
    btn_rouge.config(bg=ROUGE, fg="white")
    btn_jaune.config(bg=JAUNE, fg="black")
    btn_bleu.config(bg=BLEU, fg="white")

def update_composant_labels():
    for i in range(5):
        state = strip_states[i]
        if MODE_MELANGE == 'ADDITIF':
            couleurs = [ROUGE, VERT, BLEU]
            noms = ["rouge", "vert", "bleu"]
        else:
            couleurs = [ROUGE, JAUNE, BLEU]
            noms = ["rouge", "jaune", "bleu"]
        for j, (col, nom) in enumerate(zip(couleurs, noms)):
            if state[nom]:
                composant_labels[i][j].config(bg=col)
            else:
                composant_labels[i][j].config(bg="#eeeeee")
            composant_labels[i][j].config(text=nom[0].upper())

def update_color():
    if MODE_MELANGE == 'ADDITIF':
        couleur_finale = melange_additif(etat_rouge, etat_vert, etat_bleu)
    else:
        couleur_finale = melange_soustractif(etat_rouge, etat_jaune, etat_bleu)
    set_strip_color(index_strip, couleur_finale)
    update_button_colors()
    strip_states[index_strip]["rouge"] = etat_rouge
    strip_states[index_strip]["jaune"] = etat_jaune
    strip_states[index_strip]["bleu"] = etat_bleu
    strip_states[index_strip]["vert"] = etat_vert
    update_composant_labels()

def bouton_noir():
    global index_strip, etat_rouge, etat_jaune, etat_bleu, etat_vert
    strip_states[index_strip] = {
        "rouge": etat_rouge,
        "jaune": etat_jaune,
        "bleu": etat_bleu,
        "vert": etat_vert
    }
    index_strip = (index_strip - 1) % len(strips_colors)
    index_label.config(text=f"Index: {index_strip}")
    etat_rouge = strip_states[index_strip]["rouge"]
    etat_jaune = strip_states[index_strip]["jaune"]
    etat_bleu = strip_states[index_strip]["bleu"]
    etat_vert = strip_states[index_strip]["vert"]
    update_color()

def bouton_blanc():
    global index_strip, etat_rouge, etat_jaune, etat_bleu, etat_vert
    strip_states[index_strip] = {
        "rouge": etat_rouge,
        "jaune": etat_jaune,
        "bleu": etat_bleu,
        "vert": etat_vert
    }
    index_strip = (index_strip + 1) % len(strips_colors)
    index_label.config(text=f"Index: {index_strip}")
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
    global etat_jaune, etat_rouge, etat_vert
    if MODE_MELANGE == 'ADDITIF':
        etat_rouge = not etat_rouge
        etat_vert = not etat_vert
    else:
        etat_jaune = not etat_jaune
    update_color()

def bouton_bleu():
    global etat_bleu
    etat_bleu = not etat_bleu
    update_color()

root = tk.Tk()
root.title("Mélange de Couleurs")

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

btn_noir = tk.Button(control_frame, text="Bouton Noir", command=bouton_noir, bg=NOIR, fg="white")
btn_noir.grid(row=0, column=0, padx=5)

btn_blanc = tk.Button(control_frame, text="Bouton Blanc", command=bouton_blanc, bg=BLANC)
btn_blanc.grid(row=0, column=1, padx=5)

btn_rouge = tk.Button(control_frame, text="Bouton Rouge", command=bouton_rouge, bg=ROUGE, fg="white")
btn_rouge.grid(row=0, column=2, padx=5)

btn_jaune = tk.Button(control_frame, text="Bouton Jaune", command=bouton_jaune, bg=JAUNE, fg="black")
btn_jaune.grid(row=0, column=3, padx=5)

btn_bleu = tk.Button(control_frame, text="Bouton Bleu", command=bouton_bleu, bg=BLEU, fg="white")
btn_bleu.grid(row=0, column=4, padx=5)

update_button_colors()

index_label = tk.Label(root, text=f"Index: {index_strip}")
index_label.pack(pady=10)


# Nouvelle structure : chaque strip et ses indicateurs dans une colonne (Frame)
strips_frame = tk.Frame(root)
strips_frame.pack(pady=10)

strip_labels = []
composant_labels = []
for i in range(5):
    col_frame = tk.Frame(strips_frame)
    col_frame.grid(row=0, column=i, padx=5)
    label = tk.Label(col_frame, text=f"Strip {i}", bg=strips_colors[i], width=20, height=2)
    label.pack()
    strip_labels.append(label)
    indicateurs = []
    for j in range(3):
        comp_label = tk.Label(col_frame, text="", width=4, height=1, relief="ridge", bd=2)
        comp_label.pack(pady=(2 if j==0 else 0, 0))
        indicateurs.append(comp_label)
    composant_labels.append(indicateurs)

update_composant_labels()

root.mainloop()