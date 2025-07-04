from Bibliotheque import Livre,Membre,Bibliotheque
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORIQUE_PATH = os.path.join(DATA_DIR, "historique.csv")


def diag_circulaire(biblio:Bibliotheque):
  genres=[]
  for livre in biblio.livres.values():
     genres.append(livre.genre)

  compteur=Counter(genres)
  labels=compteur.keys()
  sizes=compteur.values()
  plt.pie(sizes,labels=labels,autopct='%1.1f%%',explode=[0.05]*len(sizes))
  plt.title("Répartition des genres dans la bibliothèque")
  os.makedirs("assets", exist_ok=True)
  plt.savefig("assets/stats_genres.png")
  plt.show()



def histogramme(biblio:Bibliotheque):
   auteurs=[]
   for livre in biblio.livres.values():
      auteurs.append(livre.auteur)

   compteur=Counter(auteurs)
   top=compteur.most_common(10)
   noms=[nom for nom,_ in top]
   valeurs=[nb for _,nb in top]
   plt.bar(noms,valeurs)
   plt.title("TOP 10 auteurs")
   plt.ylabel("Nombre de livres")
   for i, v in enumerate(valeurs):
    plt.text(i, v + 0.1, str(v), ha='center')
   os.makedirs("assets", exist_ok=True)
   plt.savefig("assets/histogramme.png")
   plt.show()



def courbe_temporelle():
    dates = []

    with open(HISTORIQUE_PATH, "r", encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split(";")
            if len(parts) != 4:
                continue  
            
            date_str, ISBN, ID_membre, action = parts
            if action != "emprunt":
                continue

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if date >= datetime.now() - timedelta(days=30):
                    dates.append(date.date())
            except ValueError:
                continue  # pour ignorer les dates invalides

    compteur = Counter(dates)
    jours = sorted(compteur.keys())
    valeurs = [compteur[jour] for jour in jours]
    
    plt.plot(jours, valeurs, marker="o")
    plt.title("Activité des emprunts - 30 derniers jours")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.xticks(rotation=45)
    for i, v in enumerate(valeurs):
        plt.text(i, v + 0.1, str(v), ha='center')
    

    plt.gcf().set_size_inches(10, 5)
    plt.tight_layout()
    plt.show()



   


  
