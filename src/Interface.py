import tkinter as tk
from tkinter import ttk, messagebox

from Bibliotheque import Bibliotheque, Livre, Membre
from exception import *
from visualisations import histogramme, diag_circulaire, courbe_temporelle

class InterfaceBibliotheque(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de Bibliothèque")
        self.geometry("800x600")

        self.biblio = Bibliotheque()
        self.biblio.chargement_donnees()

        # Création des onglets
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill="both")

        self.tab_livres = ttk.Frame(self.tabs)
        self.tab_membres = ttk.Frame(self.tabs)
        self.tab_emprunts = ttk.Frame(self.tabs)
        self.tab_stats = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_livres, text="Livres")
        self.tabs.add(self.tab_membres, text="Membres")
        self.tabs.add(self.tab_emprunts, text="Emprunts")
        self.tabs.add(self.tab_stats, text="Statistiques")

        # Appels aux méthodes pour peupler les onglets
        self.init_livres_tab()
        self.init_membres_tab()
        self.init_emprunts_tab()
        self.init_stats_tab()

    # -------------------- LIVRES -----------------------
    def init_livres_tab(self):
        label = tk.Label(self.tab_livres, text="Ajout d'un livre", font=("Arial", 14))
        label.pack(pady=10)

        frame = tk.Frame(self.tab_livres)
        frame.pack()

        tk.Label(frame, text="ISBN").grid(row=0, column=0)
        tk.Label(frame, text="Titre").grid(row=1, column=0)
        tk.Label(frame, text="Auteur").grid(row=2, column=0)
        tk.Label(frame, text="Année").grid(row=3, column=0)
        tk.Label(frame, text="Genre").grid(row=4, column=0)

        self.entry_isbn = tk.Entry(frame)
        self.entry_titre = tk.Entry(frame)
        self.entry_auteur = tk.Entry(frame)
        self.entry_annee = tk.Entry(frame)
        self.entry_genre = tk.Entry(frame)

        self.entry_isbn.grid(row=0, column=1)
        self.entry_titre.grid(row=1, column=1)
        self.entry_auteur.grid(row=2, column=1)
        self.entry_annee.grid(row=3, column=1)
        self.entry_genre.grid(row=4, column=1)

        btn_ajouter = tk.Button(frame, text="Ajouter", command=self.ajouter_livre)
        btn_ajouter.grid(row=5, columnspan=2, pady=10)

         # Tableau des livres
        self.tree_livres = ttk.Treeview(self.tab_livres, columns=("ISBN", "Titre", "Auteur", "Année", "Genre", "Statut"), show="headings")
        for col in self.tree_livres["columns"]:
            self.tree_livres.heading(col, text=col)
        self.tree_livres.pack(pady=10, fill="x")

        self.mettre_a_jour_tableau_livres()

                # Bouton supprimer livre
        btn_supprimer_livre = tk.Button(self.tab_livres, text="Supprimer le livre sélectionné", command=self.supprimer_livre)
        btn_supprimer_livre.pack(pady=5)
        btn_modifier_livre = tk.Button(self.tab_livres, text="Modifier le livre sélectionné", command=self.modifier_livre)
        btn_modifier_livre.pack(pady=5)



    def ajouter_livre(self):
        try:
            isbn = int(self.entry_isbn.get())
            if isbn in self.biblio.livres:
                raise ValueError("Ce ISBN existe déjà.")
            titre = self.entry_titre.get()
            auteur = self.entry_auteur.get()
            annee = int(self.entry_annee.get())
            genre = self.entry_genre.get()

            livre = Livre(isbn, titre, auteur, annee, genre, "disponible")
            self.biblio.ajouter_livre(livre)
            messagebox.showinfo("Succès", "Livre ajouté avec succès.")
            self.mettre_a_jour_tableau_livres()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_livre(self):
        selected = self.tree_livres.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre à supprimer.")
            return
        # Récupérer l'ISBN du livre sélectionné
        isbn = int(self.tree_livres.item(selected[0])['values'][0])
        livre = self.biblio.livres.get(isbn)
        if not livre:
            messagebox.showerror("Erreur", "Livre introuvable.")
            return
        try:
            self.biblio.supprimer_livre(livre)
            self.biblio.souvegarde_donnees()  # sauvegarder les changements dans les fichiers
            messagebox.showinfo("Succès", "Livre supprimé avec succès.")
            self.mettre_a_jour_tableau_livres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier_livre(self):
     selected = self.tree_livres.selection()
     if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner un livre à modifier.")
        return
     try:
        ancien_isbn = int(self.tree_livres.item(selected[0])['values'][0])
        livre = self.biblio.livres.get(ancien_isbn)
        if not livre:
            raise ValueError("Livre introuvable.")

        # Récupération des nouvelles valeurs depuis les champs
        nouveau_isbn = int(self.entry_isbn.get())
        titre = self.entry_titre.get()
        auteur = self.entry_auteur.get()
        annee = int(self.entry_annee.get())
        genre = self.entry_genre.get()

        # Si l'ISBN a changé, mettre à jour la clé dans le dictionnaire
        if nouveau_isbn != ancien_isbn:
            if nouveau_isbn in self.biblio.livres:
                raise ValueError("Un autre livre avec ce nouvel ISBN existe déjà.")
            del self.biblio.livres[ancien_isbn]
            livre = Livre(nouveau_isbn, titre, auteur, annee, genre, livre.statut)
            self.biblio.livres[nouveau_isbn] = livre
        else:
            # Mise à jour des attributs du livre existant
            livre.titre = titre
            livre.auteur = auteur
            livre.année = annee
            livre.genre = genre

        self.biblio.souvegarde_donnees()
        self.mettre_a_jour_tableau_livres()
        messagebox.showinfo("Succès", "Livre modifié avec succès.")
     except Exception as e:
        messagebox.showerror("Erreur", str(e))




    def mettre_a_jour_tableau_livres(self):
        # Vider le tableau
        for row in self.tree_livres.get_children():
            self.tree_livres.delete(row)
        # Ajouter les livres
        for livre in self.biblio.livres.values():
            self.tree_livres.insert("", "end", values=(livre.ISBN, livre.titre, livre.auteur, livre.année, livre.genre, livre.statut))

    # -------------------- MEMBRES -----------------------
    def init_membres_tab(self):
        label = tk.Label(self.tab_membres, text="Inscription d'un membre", font=("Arial", 14))
        label.pack(pady=10)

        frame = tk.Frame(self.tab_membres)
        frame.pack()

        tk.Label(frame, text="ID").grid(row=0, column=0)
        tk.Label(frame, text="Nom").grid(row=1, column=0)

        self.entry_id = tk.Entry(frame)
        self.entry_nom = tk.Entry(frame)

        self.entry_id.grid(row=0, column=1)
        self.entry_nom.grid(row=1, column=1)

        btn_inscrire = tk.Button(frame, text="Inscrire", command=self.inscrire_membre)
        btn_inscrire.grid(row=2, columnspan=2, pady=10)
        # Tableau des membres
        self.tree_membres = ttk.Treeview(self.tab_membres, columns=("ID", "Nom", "Livres empruntés"), show="headings")
        for col in self.tree_membres["columns"]:
            self.tree_membres.heading(col, text=col)
        self.tree_membres.pack(pady=10, fill="x")

        self.mettre_a_jour_tableau_membres()

                # Bouton supprimer membre
        btn_supprimer_membre = tk.Button(self.tab_membres, text="Supprimer le membre sélectionné", command=self.supprimer_membre)
        btn_supprimer_membre.pack(pady=5)
        btn_modifier_membre = tk.Button(self.tab_membres, text="Modifier le membre sélectionné", command=self.modifier_membre)
        btn_modifier_membre.pack(pady=5)

        



    def mettre_a_jour_tableau_membres(self):
        for row in self.tree_membres.get_children():
            self.tree_membres.delete(row)
        for membre in self.biblio.membres.values():
            empruntes = ", ".join([livre.titre for livre in membre.livres_empruntes]) or "Aucun"
            self.tree_membres.insert("", "end", values=(membre.ID, membre.nom, empruntes))


    def inscrire_membre(self):
        try:
            id = int(self.entry_id.get())
            if id in self.biblio.membres:
                raise ValueError("Ce membre existe déjà.")
            nom = self.entry_nom.get()
            membre = Membre(id, nom)
            self.biblio.enregistrer_membres(membre)
            messagebox.showinfo("Succès", "Membre inscrit avec succès.")
            self.mettre_a_jour_tableau_membres()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_membre(self):
        selected = self.tree_membres.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un membre à supprimer.")
            return
        # Récupérer l'ID du membre sélectionné
        id_membre = int(self.tree_membres.item(selected[0])['values'][0])
        membre = self.biblio.membres.get(id_membre)
        if not membre:
            messagebox.showerror("Erreur", "Membre introuvable.")
            return
        try:
            self.biblio.supprimer_membre(membre)
            self.biblio.souvegarde_donnees()  # sauvegarder les changements dans les fichiers
            messagebox.showinfo("Succès", "Membre supprimé avec succès.")
            self.mettre_a_jour_tableau_membres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def modifier_membre(self):
     selected = self.tree_membres.selection()
     if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner un membre à modifier.")
        return

     try:
        ancien_id = int(self.tree_membres.item(selected[0])['values'][0])
        membre = self.biblio.membres.get(ancien_id)
        if not membre:
            raise ValueError("Membre introuvable.")

        # Récupération des nouvelles valeurs
        nouveau_id = int(self.entry_id.get())
        nouveau_nom = self.entry_nom.get()

        if nouveau_id != ancien_id:
            if nouveau_id in self.biblio.membres:
                raise ValueError("Un autre membre avec ce nouvel ID existe déjà.")
            del self.biblio.membres[ancien_id]
            membre = Membre(nouveau_id, nouveau_nom)
            self.biblio.membres[nouveau_id] = membre
        else:
            membre.nom = nouveau_nom

        self.biblio.souvegarde_donnees()
        self.mettre_a_jour_tableau_membres()
        messagebox.showinfo("Succès", "Membre modifié avec succès.")
     except Exception as e:
        messagebox.showerror("Erreur", str(e))




    # -------------------- EMPRUNTS -----------------------
    def init_emprunts_tab(self):
        label = tk.Label(self.tab_emprunts, text="Gestion des emprunts", font=("Arial", 14))
        label.pack(pady=10)

        frame = tk.Frame(self.tab_emprunts)
        frame.pack()

        tk.Label(frame, text="ISBN Livre").grid(row=0, column=0)
        tk.Label(frame, text="ID Membre").grid(row=1, column=0)

        self.entry_isbn_emp = tk.Entry(frame)
        self.entry_id_emp = tk.Entry(frame)

        self.entry_isbn_emp.grid(row=0, column=1)
        self.entry_id_emp.grid(row=1, column=1)

        btn_emprunter = tk.Button(frame, text="Emprunter", command=self.emprunter_livre)
        btn_retourner = tk.Button(frame, text="Retourner", command=self.retourner_livre)

        btn_emprunter.grid(row=2, column=0, pady=10)
        btn_retourner.grid(row=2, column=1, pady=10)

    def emprunter_livre(self):
        try:
            isbn = int(self.entry_isbn_emp.get())
            id = int(self.entry_id_emp.get())
            livre = self.biblio.livres[isbn]
            membre = self.biblio.membres[id]
            self.biblio.gestion_emprunts(livre, membre)
            messagebox.showinfo("Succès", "Livre emprunté.")
            self.mettre_a_jour_tableau_livres()
            self.mettre_a_jour_tableau_membres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def retourner_livre(self):
        try:
            isbn = int(self.entry_isbn_emp.get())
            id = int(self.entry_id_emp.get())
            livre = self.biblio.livres[isbn]
            membre = self.biblio.membres[id]
            self.biblio.gestion_retours(livre, membre)
            messagebox.showinfo("Succès", "Livre retourné.")
            self.mettre_a_jour_tableau_livres()
            self.mettre_a_jour_tableau_membres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # -------------------- STATS -----------------------
    def init_stats_tab(self):
        label = tk.Label(self.tab_stats, text="Statistiques", font=("Arial", 14))
        label.pack(pady=10)

        btn_genres = tk.Button(self.tab_stats, text="Répartition par genre", command=lambda: diag_circulaire(self.biblio))
        btn_auteurs = tk.Button(self.tab_stats, text="Top auteurs", command=lambda: histogramme(self.biblio))
        btn_temps = tk.Button(self.tab_stats, text="Activité récente", command=courbe_temporelle)

        btn_genres.pack(pady=5)
        btn_auteurs.pack(pady=5)
        btn_temps.pack(pady=5)

if __name__ == "__main__":
    app = InterfaceBibliotheque()
    app.mainloop()
