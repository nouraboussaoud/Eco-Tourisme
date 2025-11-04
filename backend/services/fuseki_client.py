# Fuseki Client Service
import requests
from typing import Dict, List, Any
from config import FUSEKI_ENDPOINT

class FusekiClient:
    """Client pour interagir avec Apache Jena Fuseki"""
    
    def __init__(self, endpoint: str = FUSEKI_ENDPOINT):
        self.endpoint = endpoint
        self.headers = {
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/sparql-query"
        }
    
    def query(self, sparql_query: str) -> Dict[str, Any]:
        """Exécute une requête SPARQL SELECT"""
        try:
            response = requests.post(
                self.endpoint,
                data=sparql_query,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur Fuseki: {str(e)}")
    
    def update(self, sparql_update: str) -> bool:
        """Exécute une requête SPARQL UPDATE"""
        try:
            update_endpoint = self.endpoint.replace("/sparql", "/update")
            response = requests.post(
                update_endpoint,
                data=sparql_update,
                headers={"Content-Type": "application/sparql-update"},
                timeout=30
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur mise à jour Fuseki: {str(e)}")
    
    def parse_results(self, results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Parse les résultats SPARQL"""
        try:
            bindings = results.get("results", {}).get("bindings", [])
            parsed = []
            for binding in bindings:
                row = {}
                for var, value_obj in binding.items():
                    if isinstance(value_obj, dict) and "value" in value_obj:
                        row[var] = value_obj["value"]
                parsed.append(row)
            return parsed
        except Exception as e:
            raise Exception(f"Erreur parsing résultats: {str(e)}")
