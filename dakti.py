import tkinter as tk
import subprocess

liste_mots = []
mot_index = 0
mot_a_taper = ""
index_lettre = 0

# Création de la fenêtre
root = tk.Tk()
root.title("Dactylo avec espeak")
root.geometry("1000x600")

afficher_lettre = tk.BooleanVar(root, value=True)
jouer_son = tk.BooleanVar(root, value=True)
theme_sombre = tk.BooleanVar(root, value=True)
afficher_majuscule = tk.BooleanVar(root, value=True)

def appliquer_theme():
    bg_color = "black" if theme_sombre.get() else "white"
    fg_color = "white" if theme_sombre.get() else "black"
    root.configure(bg=bg_color)
    label_mot.config(bg=bg_color, fg=fg_color)
    label_statut.config(bg=bg_color, fg=fg_color)
    label_lettre.config(bg=bg_color, fg=fg_color)
    entry_mot.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    bouton_demarrer.config(bg=bg_color, fg=fg_color)
    bouton_rejouer.config(bg=bg_color, fg=fg_color)

def parler(texte):
    if jouer_son.get():
        subprocess.run(["espeak", "-v", "fr", texte])

def verifier_touche(event):
    global index_lettre, mot_index
    if not mot_a_taper or index_lettre >= len(mot_a_taper):
        return

    lettre_tapee = event.keysym.lower()
    if lettre_tapee == mot_a_taper[index_lettre]:  
        label_statut.config(text="✔ Correct", fg="green")
        index_lettre += 1
    else:
        label_statut.config(text="✘ Erreur", fg="red")
        parler("Erreur")
        return
    
    if index_lettre < len(mot_a_taper):
        afficher_lettre_majuscule()
        parler(mot_a_taper[index_lettre])  # Annonce de la prochaine lettre
    else:
        label_statut.config(text="🎉 Mot correct !", fg="blue")
        parler("Bravo !")
        root.bind("<Return>", prochain_mot)

def afficher_lettre_majuscule():
    if afficher_lettre.get():
        texte_a_afficher = mot_a_taper[index_lettre].upper() if afficher_majuscule.get() else mot_a_taper[index_lettre]
        label_lettre.config(text=texte_a_afficher)

def prochain_mot(event=None):
    global mot_index
    mot_index += 1
    if mot_index < len(liste_mots):
        demarrer(depuis_liste=True)
    else:
        label_statut.config(text="Fin de la liste !", fg="blue")
        bouton_rejouer.grid(row=4, column=1, pady=20)

def demarrer(depuis_liste=False):
    global mot_a_taper, index_lettre, mot_index
    if depuis_liste:
        mot_a_taper = liste_mots[mot_index]
    else:
        liste_mots.clear()
        mots = entry_mot.get().strip().lower().split()
        if mots:
            liste_mots.extend(mots)
            mot_index = 0
            mot_a_taper = liste_mots[mot_index]
    
    if mot_a_taper:
        index_lettre = 0
        label_mot.config(text=f"Mot à taper : {mot_a_taper}")
        afficher_lettre_majuscule()
        label_statut.config(text="En attente...", fg="black")
        bouton_rejouer.grid_remove()
        root.unbind("<KeyPress>")
        root.bind("<KeyPress>", verifier_touche)
        parler(mot_a_taper[index_lettre])
        appliquer_theme()

def quitter():
    root.quit()

# Barre de menu
menu_bar = tk.Menu(root)
menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Quitter", command=quitter)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

menu_options = tk.Menu(menu_bar, tearoff=0)
menu_options.add_checkbutton(label="Afficher la lettre", variable=afficher_lettre)
menu_options.add_checkbutton(label="Jouer le son", variable=jouer_son)
menu_options.add_checkbutton(label="Thème sombre", variable=theme_sombre, command=appliquer_theme)
menu_options.add_checkbutton(label="Afficher en majuscules", variable=afficher_majuscule, command=afficher_lettre_majuscule)
menu_bar.add_cascade(label="Options", menu=menu_options)

root.config(menu=menu_bar)

# Configuration des colonnes
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Champ pour entrer plusieurs mots
entry_mot = tk.Entry(root, font=("Arial", 14))
entry_mot.grid(row=0, column=1, padx=20, pady=20)

# Bouton pour démarrer
bouton_demarrer = tk.Button(root, text="Jouer", command=demarrer)
bouton_demarrer.grid(row=1, column=1, pady=20)

# Labels dans chaque colonne
label_mot = tk.Label(root, text="Mot à taper : ", font=("Arial", 18))
label_mot.grid(row=2, column=0, padx=20, pady=20)

label_lettre = tk.Label(root, text="?", font=("Arial", 300))
label_lettre.grid(row=2, column=1, padx=20, pady=20)

label_statut = tk.Label(root, text="En attente...", font=("Arial", 18))
label_statut.grid(row=2, column=2, padx=20, pady=20)

# Bouton rejouer
bouton_rejouer = tk.Button(root, text="Rejouer", command=demarrer)
bouton_rejouer.grid(row=4, column=1, pady=20)
bouton_rejouer.grid_remove()

appliquer_theme()
root.mainloop()
