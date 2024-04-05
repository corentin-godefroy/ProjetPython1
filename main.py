from partie1 import Commune
from partie1 import Departement

print("----- Partie 1 -----")
input = input("Tapez le numéro du code postal ou du département recherché : ")

if len(input) < 4:
    Departement.seach(input).print_population()
else:
    Commune.search(input).print_population()

print("----- Partie 2 -----")