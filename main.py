from partie1 import Commune
from partie1 import Departement
from partie2 import bruteforce

print("----- Partie 1 -----")
input = input("Tapez le nom de la commune ou le numéro du code postal ou du département recherché : ")

if input.isnumeric() and len(input) < 4:
    Departement.seach(input).print_population()
else:
    Commune.search(input).print_population()

print("----- Partie 2 -----")
bruteforce()