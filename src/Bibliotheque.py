class Livre:
    def __init__(self,ISBN,titre,auteur,année,genre,statut):
        self.ISBN=ISBN
        self.titre=titre
        self.auteur=auteur
        self.année=année
        self.genre=genre
        self.statut=statut

    def to_dict(self):
        return {
            "ISBN": self.ISBN,
            "titre": self.titre,
            "auteur": self.auteur,
            "année": self.année,
            "genre": self.genre,
            "statut": self.statut,      
        }
    
class Membre:
    def __init__(self,ID,nom):
        self.ID=ID
        self.nom=nom
        self.livres_empruntes=[]

    def to_dict(self):
        return {
            "ID": self.ID,
            "nom": self.nom,
            "livres_empruntes": [livre.ISBN for livre in self.livres_empruntes]
        }


class Bibliotheque:

    def __init__(self):
        self.livres={}
        self.membres={}


    def ajouter_livre(self,livre:Livre):
      self.livres[livre.ISBN]=livre
    


    def supprimer_livre(self,livre:Livre):
        self.livres.pop(livre.ISBN)
    
    def enregistrement_membres(self,membre:Membre):
        self.membres[membre.ID]=membre
    

    def gestion_emprunts(self,livre:Livre,membre:Membre):

        if membre.ID not in self.membres:
            raise  MembreInexistantError()
        
        if (len(membre.livres_empruntes)>=3):
            raise QuotaEmpruntDepasseError()
        
        if livre.ISBN not in self.livres:
            raise LivreInexistantError()
                
        if livre.statut=="emprunté":
            raise LivreIndisponibleError()
        
        livre.statut="disponible"
        membre.livres_empruntes.append(livre)

    def gestion_retours(self,livre:Livre,membre:Membre):
        if livre.ISBN not in self.livres:
            raise LivreInexistantError()
        
        if membre.ID not in self.membres:
            raise  MembreInexistantError()
        
        if livre in membre.livres_empruntes:
            livre.statut="disponible"
            membre.livres_empruntes.remove(livre)
           

    def souvegarde_données(sself):
        with open("livres.txt","w",encoding="utf-8") as f:
           for livre in self.livres.values():
            ligne=f"{livre.ISBN}; {livre.titre}; {livre.auteur};{livre.genre}; {livre.année}; {livre.statut}\n"
            f.write(ligne)

        with open("membres.txt","w",encoding="utf-8") as f:
            for membre in self.membres.values():
                emprunte="/".join([livre.ISBN for livre in membre.livres_emprunte])
                ligne=f"{membre.ID}; {membre.nom}; {emprunte}\n"
                f.write(ligne)

    def chargement_données(self,):
    
