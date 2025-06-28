from Bibliotheque import Livre,Membre,Bibliotheque
from exception import(
    LivreInexistantError,
    LivreIndisponibleError,
    MembreInexistantError,
    QuotaEmpruntDepasseError
)
from visualisations import histogramme, diag_circulaire, courbe_temporelle


def main():
   Biblio=Bibliotheque()
   Biblio.chargement_donnees()
   while True: 
       print("------GESTION BIBLIOTHEQUE------")
       print("1.Ajouter un livre")
       print("2.Inscrire un membre")
       print("3.Emprunter un livre")
       print("4.Rendre un livre")
       print("5.Lister tous les livres et Les membres")
       print("6.Afficher les statistiques")
       print("7. Supprimer un livre")       
       print("8. Supprimer un membre") 
       print("9.Souvegarder et quitter")

       choix=input("Choissisez une option :")

       match choix:
           case "1":
               print("---Ajout d'un livre---")
               while True:
                 ISBN=int(input("Entrer l isbn du livre:"))
                 if ISBN in Biblio.livres:
                    print(f"Erreur: un livre avec ce ISBN existe déja.Veuillez saisir un autre ISBN.")
                 else:
                    titre=input("Entrer le titre du livre:")
                    auteur=input("Entrer le nom de l'auteur:")
                    année=int(input("Entrer l'année de publication:"))
                    genre=input("De quel genre ?:")
                    livre=Livre(ISBN,titre,auteur,année,genre,"disponible")
                    Biblio.ajouter_livre(livre)
                    print("Livre bien ajouté!")
                    break

           case "2":
                print("---Ajout d'un membre---")
                while True:
                  ID=int(input("Entrer l id du membre :"))
                  if ID in Biblio.membres:
                      print(f"Erreur: un membre avec ce ID existe déja.Veuillez saisir un autre ID.")
                  else:
                     nom=input("Entrer le nom du membre:")
                     membre=Membre(ID,nom)
                     Biblio.enregistrer_membres(membre)
                     print("Membre bien ajouté!")
                     break
            
           case "3":
               print("---Emprunt un livre:---")
               isbn=int(input("Entrer l'isbn du livre que vous voulez emprunter:"))
               id=int(input("Entrer l'id du membre qui veux emprunter le livre:"))
               try:
                  if isbn not in Biblio.livres:
                       raise LivreInexistantError()
                  if id not in Biblio.membres:
                      raise MembreInexistantError()
                  livre=Biblio.livres[isbn]
                  membre=Biblio.membres[id]
                  Biblio.gestion_emprunts(livre,membre)
                  print("Livre emprunté avec succes")
               except(LivreIndisponibleError,LivreInexistantError,MembreInexistantError,QuotaEmpruntDepasseError) as e:
                   print (f"Erreur : {e}")


    
           case "4":
               print("---Retour d'un livre---")
               isbn=int(input("Entrer l'isbn du livre que vous voulez retourner:"))
               id=int(input("Entrer l'id du membre qui veux retourner le livre:"))
               try:
                   if isbn not in Biblio.livres:
                       raise LivreInexistantError()
                   if id not in Biblio.membres:
                       raise MembreInexistantError()
                   livre=Biblio.livres[isbn]
                   membre=Biblio.membres[id]
                   Biblio.gestion_retours(livre,membre)
                   print("Livre retourné avec succes")
               except(LivreInexistantError,MembreInexistantError) as e:
                   print (f"Erreur : {e}")
               
           case "5":
               print("---Affichage des elements de la bibliotheque---")
               Biblio.afficher_donnees()

           case "6":
               print("---Affichage de statistiques---")
               diag_circulaire(Biblio)
               histogramme(Biblio)
               courbe_temporelle()
               

           case "7":
               print("---Suppression d’un livre---")
               try:
                   isbn = int(input("Entrer l'ISBN du livre à supprimer : "))
                   if isbn not in Biblio.livres:
                     raise LivreInexistantError()
                   livre = Biblio.livres[isbn]
                   Biblio.supprimer_livre(livre)
                   print("Livre supprimé avec succès.")
               except (LivreInexistantError, LivreIndisponibleError) as e:
                print(f"Erreur : {e}")
               
           case "8":
               print("---Suppression d’un membre---")
               try:
                   id_membre = int(input("Entrer l'ID du membre à supprimer : "))
                   if id_membre not in Biblio.membres:
                      raise MembreInexistantError()
                   membre = Biblio.membres[id_membre]
                   Biblio.supprimer_membre(membre)
                   print("Membre supprimé avec succès.")
               except (MembreInexistantError, Exception) as e:
                   print(f"Erreur : {e}")

           case "9":
               print("---Souvegarde des données---")
               Biblio.souvegarde_donnees()
               print("---Données souvegardées avec succes")
               break


           
        
           
if __name__ == "__main__":
    main()


