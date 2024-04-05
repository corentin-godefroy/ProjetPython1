import requests

class Commune:
    nom: str = ""
    code: str = ""
    deptCode: str = ""
    siren: str = ""
    codeEpci: str = ""
    codeRegion: str = ""
    codesPostaux: list[str] = []
    population: int = 0
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

    def search(postalCode: str):
        default_url = "https://geo.api.gouv.fr/communes/"
        result = requests.get(default_url, params={"codePostal": postalCode})
        if result.status_code != 200:
            print("request went wrong")
            return
        commune = Commune(result.json()[0])
        commune.search_url = result.url
        return commune

    def print_population(self):
        print(f"Population de la commune de {self.nom}: {self.population} habitants")
