from Bibliotheque import Livre,Membre,Bibliotheque
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import csv

def diag_circulaire(self,livre:Livre,biblio:Bibliotheque):
  genre=[]
  for livre in biblio.livres:
     genre=livre.genre

  compteur=Counter(genres)

  
