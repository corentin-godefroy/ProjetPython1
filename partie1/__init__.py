import requests

class Commune:
    nom: str = ""
    code: str = ""
    deptCode: str = ""
    siren: str = ""
    codeEpci: str = ""
    codeRegion: str = ""
    codesPostaux: list[str] = []
    population: int = -1
    score: int = 0
    search_url: str = ""

    # Constructeur de la classe, peut prendre en argument facultatif un dict provenant d'un json qui sera alors transformé en objet
    def __init__(self, json_dict: dict={}):
        if len(json_dict) != 0:
            self.nom = json_dict["nom"]
            self.code = json_dict["code"]
            self.deptCode = json_dict["codeDepartement"]
            self.siren = json_dict["siren"]
            self.codeEpci = json_dict["codeEpci"]
            self.codeRegion = json_dict["codeRegion"]
            self.codesPostaux = json_dict["codesPostaux"]
            self.population = json_dict["population"]
            if "score" in json_dict:
                self.score = json_dict["score"]

    # Permet un affichage clair avec le print()
    def __str__(self):
        return f"Commmune(\n\tnom: {self.nom}\n\tcode: {self.code}\n\tdeptCode: {self.deptCode}\n\tsiren: {self.siren}\n\tcodeEpci: {self.codeEpci}\n\tcodeRegion: {self.codeRegion}\n\tcodesPostaux: {self.codesPostaux}\n\tpopulation: {self.population}\n\tscore: {self.score}\n\tsearch_url: {self.search_url}\n)"

    # Permet d'effectuer uen recherche d'une ville ou d'une ccommune. Prends en argument la recherche en texte.
    # Si le texte est numérique, alors on recherche par code postal, snon on essaye une recherche par nom.
    def search(recherche: str):
        default_url = "https://geo.api.gouv.fr/communes/"
        if recherche.isnumeric():
            result = requests.get(default_url, params={"codePostal": recherche})
            if result.status_code != 200:
                print("request went wrong")
                return
            elif not result.json():
                print("Aucun résultat")
            else:
                commune = Commune(result.json()[0])
                commune.search_url = result.url
                return commune
        else:
            result = requests.get(default_url, params={"nom": recherche})
            if result.status_code != 200:
                print(f"request went wrong. error: {result.status_code}")
                return
            elif not result.json():
                print("Aucun résultat")
            else:
                commune = Commune(result.json()[0])
                commune.search_url = result.url
                return commune

            print("Le code postal n'est pas numérique")
        return Commune()

    # Affiche la population si l'objet n'est pas "vide" (valeurs par défaut) puis renvoie le total.
    def print_population(self) -> int:
        if self.population != -1:
            print(f"Population de la commune de {self.nom}: {self.population} habitants")
            return self.population

class Departement:
    communes: list[Commune] = []
    search_url: str = ""

    # Construteur de la classe. Peut prendre en argument facultatif une liste de dict correspondant à des communes, et les transforment en list de communes.
    def __init__(self, data: list[dict]= []):
        for commune in data:
            self.communes.append(Commune(commune))

    # Permet d'afficher clairement la classe avec le print()
    def __str__(self):
        communes_list = ""
        for commune in self.communes:
            communes_list = f"{communes_list}\n{commune.__str__()}"
        return f"Departement(\n\tcommunes: {communes_list}\n\tsearch_url: {self.search_url}\n))"

    # Méthode pour chercher les communes d'un département. Vérifie que le numéro de département est bien numérique.
    def seach(dept_code: str):
        if dept_code.isnumeric():
            url = f"https://geo.api.gouv.fr/departements/{dept_code}/communes"
            result = requests.get(url)
            if result.status_code != 200:
                print(f"request went wrong. error: {result.status_code}")
                return Departement()
            departement = Departement(result.json())
            departement.search_url = result.url
            return departement
        else:
            print("Le département n'est pas numérique")

    # Compte la population totale commune par communes avant de l'afficher et la renvoyer
    def print_population(self) -> int:
        total = 0
        if self.communes:
            for commune in self.communes:
                total += commune.population
            print(f"Population totale dans le département {self.communes[0].deptCode}: {total} habitants")
            return total
