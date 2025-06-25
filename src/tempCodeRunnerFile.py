from Bibliotheque import Livre,Membre,Bibliotheque
from exception import(
    LivreInexistantError,
    LivreIndisponibleError,
    MembreInexistantError,
    QuotaEmpruntDepasseError
)


def main():
   Biblio=Bibliotheque()
   Biblio.chargement_donnees()
   while True: 
       print("------GESTION BIBLIOTHEQUE------")
       print("1.Ajouter un livre")
       print("2.Inscrire un membre")
       print("3.Emprunter un livre")
       print("4.Rendre un livre")
       print("5.Lister tous les livres")
       print("6.Afficher les statistiques")
       print("7.Souvegarder et quitter")

       choix=input("Choissisez une option :")

       match choix:
           case "1":
               print("---Ajout d'un livre---")
               ISBN=int(input("Entrer l isbn du livre:"))
               titre=input("Entrer le titre du livre:")
               auteur=input("Entrer le nom de l'auteur:")
               année=int(input("Entrer l'année de publication:"))
               genre=input("De quel genre ?:")
               livre=Livre(ISBN,titre,auteur,année,genre,"disponible")
               Biblio.ajouter_livre(livre)
               print("Livre bien ajouté!")

           case "2":
                print("---Ajout d'un membre---")
                ID=int(input("Entrer l id du membre :"))
                nom=input("Entrer le nom du membre:")
                membre=Membre(ID,nom)
                Biblio.enregistrer_membres(membre)
                print("Membre bien ajouté!")
            
           case "3":
               print("---Emprunt un livre:---")
               isbn=int(input("Entrer l'isbn du livre que vous voulez emprunter:"))
               id=int(input("Entrer l'id du membre qui veux emprunter le livre:"))
               try:
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

               
           case "7":
               print("---Souvegarde des données---")
               Biblio.souvegarde_donnees()
               print("---Données souvegardées avec succes")
               break
           
        
           
if __name__ == "__main__":
    main()


