# Mock Fuseki Client - Works without actual Fuseki server
import json
from typing import Dict, List, Any
from datetime import datetime

class MockFusekiClient:
    """Mock Fuseki Client for development without actual Fuseki server"""
    
    def __init__(self):
        # In-memory storage
        self.data = {
            "collection_points": [
                {"id": "cp1", "name": "Point de Collecte Centre-Ville", "city": "Tunis", "address": "Rue de la Paix"},
                {"id": "cp2", "name": "Point de Collecte Banlieue", "city": "Ariana", "address": "Avenue Habib Bourguiba"},
                {"id": "cp3", "name": "Point de Collecte Eco-Park", "city": "Skhira", "address": "Zone Industrielle"},
            ],
            "waste_types": [
                {"id": "wt1", "name": "Plastique", "recyclable": "true"},
                {"id": "wt2", "name": "Papier", "recyclable": "true"},
                {"id": "wt3", "name": "Verre", "recyclable": "true"},
                {"id": "wt4", "name": "Métal", "recyclable": "true"},
                {"id": "wt5", "name": "Organique", "recyclable": "false"},
            ],
            "activities": [
                {"id": "act1", "name": "Nettoyage Plage", "description": "Activité de nettoyage côtier"},
                {"id": "act2", "name": "Tri des Déchets", "description": "Tri manuel des déchets recyclables"},
                {"id": "act3", "name": "Sensibilisation Écologique", "description": "Atelier de sensibilisation"},
            ],
            "badges": [
                {"id": "badge1", "name": "Eco-Warrior", "description": "10 activités complétées"},
                {"id": "badge2", "name": "Green Collector", "description": "100kg de déchets collectés"},
                {"id": "badge3", "name": "Sustainability Hero", "description": "1000kg de déchets collectés"},
            ],
            "users": [
                {"id": "user1", "name": "Ahmed", "points": 150},
                {"id": "user2", "name": "Fatima", "points": 200},
                {"id": "user3", "name": "Mohamed", "points": 100},
            ]
        }
    
    def query(self, sparql_query: str) -> Dict[str, Any]:
        """Mock SPARQL query execution"""
        print(f"[MOCK FUSEKI] Executing: {sparql_query[:100]}...")
        
        # Parse the query to determine what to return
        if "collection_points" in sparql_query.lower() or "pointcollecte" in sparql_query.lower():
            results = self._format_results(self.data["collection_points"])
        elif "waste" in sparql_query.lower() or "dechet" in sparql_query.lower():
            results = self._format_results(self.data["waste_types"])
        elif "activit" in sparql_query.lower():
            results = self._format_results(self.data["activities"])
        elif "badge" in sparql_query.lower():
            results = self._format_results(self.data["badges"])
        elif "count" in sparql_query.lower():
            results = {
                "results": {
                    "bindings": [
                        {
                            "totalUsers": {"type": "literal", "value": str(len(self.data["users"]))},
                            "totalActivities": {"type": "literal", "value": str(len(self.data["activities"]))},
                            "totalPoints": {"type": "literal", "value": str(len(self.data["collection_points"]))}
                        }
                    ]
                }
            }
        else:
            results = {"results": {"bindings": []}}
        
        return results
    
    def update(self, sparql_update: str) -> bool:
        """Mock SPARQL update execution"""
        print(f"[MOCK FUSEKI] Updating: {sparql_update[:100]}...")
        # Simulate successful update
        return True
    
    def parse_results(self, results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Parse SPARQL results"""
        try:
            bindings = results.get("results", {}).get("bindings", [])
            parsed = []
            for binding in bindings:
                row = {}
                for var, value_obj in binding.items():
                    if isinstance(value_obj, dict) and "value" in value_obj:
                        row[var] = value_obj["value"]
                    else:
                        row[var] = str(value_obj)
                parsed.append(row)
            return parsed
        except Exception as e:
            raise Exception(f"Erreur parsing résultats: {str(e)}")
    
    def _format_results(self, data: List[Dict]) -> Dict[str, Any]:
        """Format data as SPARQL results"""
        bindings = []
        for item in data:
            binding = {}
            for key, value in item.items():
                binding[key] = {
                    "type": "literal" if not key.startswith("http") else "uri",
                    "value": str(value)
                }
            bindings.append(binding)
        
        return {
            "head": {"vars": list(data[0].keys()) if data else []},
            "results": {"bindings": bindings}
        }
