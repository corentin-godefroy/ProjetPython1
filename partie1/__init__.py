import requests

class Commune:
    nom: str
    code: str
    deptCode: str
    siren: str
    codeEpci: str
    codeRegion: str
    codesPost: list[str]
    population: int
    score: int
    search_url: str

    def from_json(self, json: dict):
        return

    def search(self, postalCode: str):
        default_url = "https://geo.api.gouv.fr/communes/"
        result = requests.get(default_url, params=postalCode)
        if result.status_code != 200:
            print("request went wrong")
            return {}
        return json.loads(result.content)["items"]

    'https://geo.api.gouv.fr/communes?codePostal=78000'

class Departement:
    communes: list[Commune]
    search_url: str

    def search(self):
        default_url = "https://geo.api.gouv.fr/departements/"
        
    def get_population_totale(self) -> int:
        total = 0
        for commune in self.communes:
            total += commune.population
        return total