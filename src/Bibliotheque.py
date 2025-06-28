import os

# Définition des chemins vers les fichiers de données
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Dossier racine du projet
DATA_DIR = os.path.join(BASE_DIR, "data")

LIVRES_PATH = os.path.join(DATA_DIR, "livres.txt")
MEMBRES_PATH = os.path.join(DATA_DIR, "membres.txt")
HISTORIQUE_PATH = os.path.join(DATA_DIR, "historique.csv")

import csv 
from datetime import datetime

from exception import (
    LivreInexistantError,
    LivreIndisponibleError,
    MembreInexistantError,
    QuotaEmpruntDepasseError
) 

class Livre:
    def __init__(self,ISBN,titre,auteur,année,genre,statut):
        self.ISBN=ISBN
        self.titre=titre
        self.auteur=auteur
        self.année=année
        self.genre=genre
        self.statut=statut

    def __str__(self):
      return f"Live(ISBN:{self.ISBN}, titre:{self.titre}, auteur: {self.auteur}, année:{self.année}, genre:{self.genre}, statut: {self.statut})"
    
class Membre:
    def __init__(self,ID,nom):
        self.ID=ID
        self.nom=nom
        self.livres_empruntes=[]

   
    def __str__(self):
        empruntes = ", ".join([livre.titre for livre in self.livres_empruntes]) or "Aucun"
        return f"Membre(ID:{self.ID}, nom:{self.nom}, livres empruntes:{empruntes})"
   
class Bibliotheque:

    def __init__(self):
        self.livres={}
        self.membres={}


    def ajouter_livre(self,livre:Livre):
      self.livres[livre.ISBN]=livre
    


    def supprimer_livre(self, livre: Livre):
     if livre.ISBN not in self.livres:
        raise LivreInexistantError()
    
     if livre.statut == "emprunté":
        raise LivreIndisponibleError("Ce livre est actuellement emprunté et ne peut pas être supprimé.")
    
     del self.livres[livre.ISBN]

    
    def enregistrer_membres(self,membre:Membre):
        self.membres[membre.ID]=membre

    def supprimer_membre(self, membre: Membre):
     if membre.ID not in self.membres:
        raise MembreInexistantError()
    
     if membre.livres_empruntes:
        raise Exception("Le membre a encore des livres empruntés.")
    
     del self.membres[membre.ID]

    
    #Emprunter livre avec verifications
    def gestion_emprunts(self,livre:Livre,membre:Membre):

        if membre.ID not in self.membres:
            raise  MembreInexistantError()
        
        if livre.ISBN not in self.livres:
            raise LivreInexistantError()
        
        if (len(membre.livres_empruntes)>=3):
            raise QuotaEmpruntDepasseError()
                
        if livre.statut=="emprunté":
            raise LivreIndisponibleError()
        
        livre.statut="emprunté"
        membre.livres_empruntes.append(livre)
        self.enregistrer_historique(livre,membre,"emprunt")


    #Retourner livre apres verifications
    def gestion_retours(self,livre:Livre,membre:Membre):
        if livre.ISBN not in self.livres:
            raise LivreInexistantError()
        
        if membre.ID not in self.membres:
            raise  MembreInexistantError()
        
        if livre in membre.livres_empruntes:
            livre.statut="disponible"
            membre.livres_empruntes.remove(livre)
            self.enregistrer_historique(livre,membre,"retour")
           
    #Souvegarde les donnees dans les fichiers .txt
    def souvegarde_donnees(self):
        with open(LIVRES_PATH,"w",encoding="utf-8") as f:
           for livre in self.livres.values():
            ligne = f"{livre.ISBN};{livre.titre};{livre.auteur};{livre.année};{livre.genre};{livre.statut}\n"
            f.write(ligne)

        with open(MEMBRES_PATH,"w",encoding="utf-8") as f:
            for membre in self.membres.values():
                emprunte="/".join([livre.ISBN for livre in membre.livres_empruntes])
                ligne=f"{membre.ID}; {membre.nom}; {emprunte}\n"
                f.write(ligne)

    #Recupere les donnees depuis les fichiers .txt
    def chargement_donnees(self):
        with open(LIVRES_PATH,"r",encoding="utf-8") as f:
            for ligne in f:
                isbn_str,titre,auteur,annee,genre,statut=ligne.strip().split(";")
                isbn=int(isbn_str.strip())
                livre=Livre(isbn,titre,auteur,annee,genre,statut)
                self.livres[livre.ISBN]=livre

        with open(MEMBRES_PATH,"r",encoding="utf-8") as f:
            for ligne in f:
                id_str,nom,liste_isbn_livre=ligne.strip().split(";")
                id = int(id_str.strip())
                membre=Membre(id,nom.strip())   
                if liste_isbn_livre.strip():
                 for isbn_str in liste_isbn_livre.split("/"):
                    isbn=int(isbn_str.strip())
                    if isbn in self.livres:
                        livre=self.livres[isbn]
                        membre.livres_empruntes.append(livre)
                    else:
                        print("livre non trouvé")

                self.membres[membre.ID]=membre

              


    #Affiche contenu du biblio
    def afficher_donnees(self):
        print("----Livres----:")
        if not self.livres:
            print("auncun livre n'est dans la bibliotheque")

        else:
            for livre in self.livres.values():
                print(livre)

        print("----Membres:----")
        if not self.membres:
            print("auncun membre n'est dans la bibliotheque")

        else:
            for membre in self.membres.values():
                emprunte = "/".join([str(livre.ISBN) for livre in membre.livres_empruntes])
                print (f" Membre: {membre.ID}; {membre.nom}; {emprunte};")


   #Enregistre une ligne dans le fichier historique pour chaque emprunt ou retour
    def enregistrer_historique(self,livre,membre,action):
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(HISTORIQUE_PATH, "a", newline="", encoding="utf-8") as f:
               writer = csv.writer(f, delimiter=";")
               writer.writerow([date_heure, livre.ISBN, membre.ID, action])



    


    
