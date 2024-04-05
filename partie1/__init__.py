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

    def search(postalCode: str):
        default_url = "https://geo.api.gouv.fr/communes/"
        result = requests.get(default_url, params={"codePostal": postalCode})
        if result.status_code != 200:
            print("request went wrong")
            return []
        return result.json()