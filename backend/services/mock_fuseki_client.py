# Mock Fuseki Client - Works without actual Fuseki server
import json
from typing import Dict, List, Any
from datetime import datetime

class MockFusekiClient:
    """Mock Fuseki Client for development without actual Fuseki server"""
    
    def __init__(self):
        # In-memory storage - Eco-Tourism Data
        self.data = {
            "destinations": [
                {"nom": "Parc Écologique Ichkeul", "localiseDans": "Bizerte", "description": "Réserve naturelle avec lacs et faune exceptionnelle", "scoreDurabilite": "95"},
                {"nom": "Île de Djerba - Eco-Resort", "localiseDans": "Djerba", "description": "Destination balnéaire durable avec hébergements écologiques", "scoreDurabilite": "88"},
                {"nom": "Montagnes de Dorsal", "localiseDans": "Tunisie centrale", "description": "Randonnée écologique et immersion nature", "scoreDurabilite": "92"},
                {"nom": "Oasis de Douz", "localiseDans": "Sahara", "description": "Tourisme désertique responsable avec guides locaux", "scoreDurabilite": "85"},
                {"nom": "Medina de Tunis - Patrimoine", "localiseDans": "Tunis", "description": "Exploration culturelle avec artisans locaux", "scoreDurabilite": "80"},
            ],
            "hebergements": [
                {"nom": "Hotel Écologique Paradise", "localiseDans": "Djerba", "type": "HotelEcologique", "scoreDurabilite": "95", "certification": "EcoTourism", "description": "Hôtel 5 étoiles avec panneaux solaires et gestion écologique de l'eau"},
                {"nom": "Gîte Rural Nomade", "localiseDans": "Douz", "type": "GiteRural", "scoreDurabilite": "88", "certification": "GreenGlobe", "description": "Hébergement traditionnel avec matériaux locaux"},
                {"nom": "Auberge Bio Oasis", "localiseDans": "Tozeur", "type": "Auberge", "scoreDurabilite": "85", "certification": "EcoTourism", "description": "Auberge avec jardin bio et cuisine locale"},
                {"nom": "Camping Écologique Plage", "localiseDans": "Bizerte", "type": "CampingEcoResponsable", "scoreDurabilite": "90", "certification": "GreenGlobe", "description": "Camping zéro déchet face à la mer"},
                {"nom": "Resort Durable Méditerranée", "localiseDans": "Hammamet", "type": "HotelEcologique", "scoreDurabilite": "92", "certification": "EcoTourism", "description": "Resort avec certification environnementale"},
            ],
            "activites": [
                {"nom": "Randonnée Écologique Ichkeul", "description": "Découverte de la biodiversité", "type": "Sportive", "kgCO2": "2.5", "profileRecommande": "Adventure"},
                {"nom": "Visite Artisans Médina", "description": "Immersion culturelle avec artisans locaux", "type": "Culturelle", "kgCO2": "0.8", "profileRecommande": "Culture"},
                {"nom": "Yoga au Coucher de Soleil", "description": "Séance de relaxation en nature", "type": "Detente", "kgCO2": "0.3", "profileRecommande": "BienEtre"},
                {"nom": "Excursion Famille Désert", "description": "Safari écologique en 4x4 électrique", "type": "Familiale", "kgCO2": "5.2", "profileRecommande": "Famille"},
                {"nom": "Atelier Cuisine Locale Durable", "description": "Cours de cuisine avec produits locaux bio", "type": "Educative", "kgCO2": "1.1", "profileRecommande": "Culture"},
            ],
            "certifications": [
                {"nom": "EcoTourism Certified", "description": "Certification internationale de tourisme écologique", "criteres": "Respect environnement et communautés locales"},
                {"nom": "Green Globe", "description": "Standard global pour tourisme durable", "criteres": "Performance environnementale et sociale"},
                {"nom": "Eco-Label Européen", "description": "Label UE pour tourisme responsable", "criteres": "Excellence environnementale"},
            ],
            "voyageurs": [
                {"nom": "Ahmed", "profil": "Adventure", "empreinteCarbone": "45", "avis": "5"},
                {"nom": "Fatima", "profil": "Culture", "empreinteCarbone": "28", "avis": "5"},
                {"nom": "Mohamed", "profil": "BienEtre", "empreinteCarbone": "15", "avis": "4"},
            ]
        }
    
    def query(self, sparql_query: str) -> Dict[str, Any]:
        """Mock SPARQL query execution"""
        print(f"[MOCK FUSEKI] Executing: {sparql_query[:100]}...")
        
        # Parse the query to determine what to return
        query_lower = sparql_query.lower()
        
        if "destination" in query_lower:
            results = self._format_results(self.data["destinations"])
        elif "hebergement" in query_lower:
            results = self._format_results(self.data["hebergements"])
        elif "activit" in query_lower:
            results = self._format_results(self.data["activites"])
        elif "certification" in query_lower:
            results = self._format_results(self.data["certifications"])
        elif "voyageur" in query_lower or "profile" in query_lower:
            results = self._format_results(self.data["voyageurs"])
        elif "count" in query_lower:
            results = {
                "results": {
                    "bindings": [
                        {
                            "totalVoyageurs": {"type": "literal", "value": str(len(self.data["voyageurs"]))},
                            "totalDestinations": {"type": "literal", "value": str(len(self.data["destinations"]))},
                            "totalHebergements": {"type": "literal", "value": str(len(self.data["hebergements"]))},
                            "totalActivites": {"type": "literal", "value": str(len(self.data["activites"]))}
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
