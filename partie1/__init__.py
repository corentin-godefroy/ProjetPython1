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

    def __str__(self):
        return f"Commmune(\n\tnom: {self.nom}\n\tcode: {self.code}\n\tdeptCode: {self.deptCode}\n\tsiren: {self.siren}\n\tcodeEpci: {self.codeEpci}\n\tcodeRegion: {self.codeRegion}\n\tcodesPostaux: {self.codesPostaux}\n\tpopulation: {self.population}\n\tscore: {self.score}\n\tsearch_url: {self.search_url}\n)"

    def search(code_postal: str):
        if code_postal.isnumeric():
            default_url = "https://geo.api.gouv.fr/communes/"
            result = requests.get(default_url, params={"codePostal": code_postal})
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
            print("Le code postal n'est pas numérique")
        return Commune()

    def print_population(self) -> int:
        if self.population != -1:
            print(f"Population de la commune de {self.nom}: {self.population} habitants")
            return self.population

class Departement:
    communes: list[Commune] = []
    search_url: str = ""

    def __init__(self, data: list[dict]= []):
        for commune in data:
            self.communes.append(Commune(commune))
    def __str__(self):
        communes_list = ""
        for commune in self.communes:
            communes_list = f"{communes_list}\n{commune.__str__()}"
        return f"Departement(\n\tcommunes: {communes_list}\n\tsearch_url: {self.search_url}\n))"

    def seach(dept_code: str):
        if dept_code.isnumeric():
            url = f"https://geo.api.gouv.fr/departements/{dept_code}/communes"
            result = requests.get(url)
            if result.status_code != 200:
                print("request went wrong")
                return Departement()
            departement = Departement(result.json())
            departement.search_url = result.url
            return departement
        else:
            print("Le département n'est pas numérique")

    def print_population(self) -> int:
        total = 0
        if self.communes:
            for commune in self.communes:
                total += commune.population
            print(f"Population totale dans le département {self.communes[0].deptCode}: {total} habitants")
            return total
