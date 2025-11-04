# Service de Recommandations Intelligentes
from typing import List, Dict, Any, Optional
from services.fuseki_client import FusekiClient
from config import ONTOLOGY_NS
import math

class RecommendationEngine:
    """Moteur de recommandations intelligentes basé sur profils et impact carbone"""
    
    def __init__(self):
        self.fuseki = FusekiClient()
        self.ns = ONTOLOGY_NS
    
    def calculate_carbon_score(self, co2_kg: float) -> Dict[str, Any]:
        """Calcule le score d'impact carbone"""
        if co2_kg <= 50:
            level = "Faible"
            score = 100
        elif co2_kg <= 150:
            level = "Moyen"
            score = max(0, 100 - ((co2_kg - 50) / 100) * 50)
        else:
            level = "Élevé"
            score = max(0, 50 - ((co2_kg - 150) / 100) * 50)
        
        return {
            "level": level,
            "score": round(score, 2),
            "kg_co2": co2_kg
        }
    
    def calculate_match_score(self, traveler_profile: str, activity_type: str) -> float:
        """Calcule la compatibilité entre profil et activité (0-100)"""
        compatibility_matrix = {
            "Adventure": {
                "ActiviteSportive": 100,
                "Randonnee": 100,
                "Plongee": 90,
                "ActiviteEducative": 40,
                "ActiviteCulturelle": 30,
                "ActiviteDetente": 20,
            },
            "Culture": {
                "ActiviteCulturelle": 100,
                "VisiteHistorique": 100,
                "Musee": 95,
                "ActiviteEducative": 80,
                "Atelier_culinaire": 70,
                "ActiviteSportive": 30,
                "Randonnee": 20,
            },
            "BienEtre": {
                "ActiviteDetente": 100,
                "Spa": 100,
                "Meditation": 95,
                "ActiviteEducative": 60,
                "ActiviteCulturelle": 50,
                "ActiviteSportive": 30,
            },
            "Famille": {
                "ActiviteEducative": 100,
                "Atelier_culinaire": 90,
                "ActiviteCulturelle": 85,
                "ActiviteDetente": 70,
                "ActiviteSportive": 60,
            }
        }
        
        profile_compat = compatibility_matrix.get(traveler_profile, {})
        return profile_compat.get(activity_type, 50)
    
    def get_activities_for_profile(self, profile: str) -> List[Dict[str, Any]]:
        """Récupère les activités recommandées pour un profil"""
        query = f"""PREFIX eco: <{self.ns}>
SELECT ?activite ?nom ?type ?description
WHERE {{
  ?activite rdf:type ?type .
  ?activite eco:nom ?nom .
  OPTIONAL {{ ?activite eco:description ?description }}
  ?type rdfs:subClassOf+ eco:ActiviteTouristique .
}}
LIMIT 50"""
        
        try:
            results_json = self.fuseki.query(query)
            activities = self.fuseki.parse_results(results_json)
            
            # Score each activity based on profile
            scored = []
            for activity in activities:
                activity_type = activity.get('type', '').split('#')[-1]
                score = self.calculate_match_score(profile, activity_type)
                activity['match_score'] = score
                scored.append(activity)
            
            # Sort by score
            scored.sort(key=lambda x: x['match_score'], reverse=True)
            return scored
        except Exception as e:
            return []
    
    def get_accommodations_for_profile(self, profile: str) -> List[Dict[str, Any]]:
        """Récupère les hébergements recommandés"""
        query = f"""PREFIX eco: <{self.ns}>
SELECT ?hebergement ?nom ?type ?description ?scoreDurabilite
WHERE {{
  ?hebergement rdf:type ?type .
  ?hebergement eco:nom ?nom .
  OPTIONAL {{ ?hebergement eco:description ?description }}
  OPTIONAL {{ ?hebergement eco:scoreDurabilite ?scoreDurabilite }}
  ?type rdfs:subClassOf+ eco:Hebergement .
}}
LIMIT 30"""
        
        try:
            results_json = self.fuseki.query(query)
            accommodations = self.fuseki.parse_results(results_json)
            
            # Filter for eco-friendly ones first
            eco_friendly = [acc for acc in accommodations 
                          if int(acc.get('scoreDurabilite', 0)) >= 70]
            return eco_friendly if eco_friendly else accommodations
        except Exception as e:
            return []
    
    def get_transport_options(self, carbon_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Récupère les options de transport, triées par impact carbone"""
        query = f"""PREFIX eco: <{self.ns}>
SELECT ?transport ?nom ?empreinte ?kgCO2
WHERE {{
  ?transport rdf:type ?type .
  ?transport eco:nom ?nom .
  OPTIONAL {{
    ?transport eco:aEmpreinte ?empreinte .
    ?empreinte eco:kgCO2 ?kgCO2 .
  }}
  ?type rdfs:subClassOf+ eco:Transport .
}}
ORDER BY ?kgCO2"""
        
        try:
            results_json = self.fuseki.query(query)
            transports = self.fuseki.parse_results(results_json)
            
            # Add carbon score to each
            scored = []
            for transport in transports:
                kg_co2 = float(transport.get('kgCO2', 100))
                carbon = self.calculate_carbon_score(kg_co2)
                transport['carbon'] = carbon
                scored.append(transport)
            
            # If carbon-sensitive, prioritize low-carbon options
            if carbon_sensitive:
                scored.sort(key=lambda x: x['carbon']['score'], reverse=True)
            
            return scored
        except Exception as e:
            return []
    
    def generate_recommendation(
        self, 
        profile: str,
        destination: str,
        budget: float = 1000,
        carbon_priority: bool = False,
        days: int = 3
    ) -> Dict[str, Any]:
        """Génère une recommandation complète de voyage"""
        
        activities = self.get_activities_for_profile(profile)
        accommodations = self.get_accommodations_for_profile(profile)
        transports = self.get_transport_options(carbon_priority)
        
        # Select best options
        best_activities = activities[:min(days, len(activities))]
        best_accommodation = accommodations[0] if accommodations else None
        best_transport = transports[0] if transports else None
        
        # Calculate total carbon footprint
        total_co2 = 0
        if best_transport:
            total_co2 += float(best_transport.get('carbon', {}).get('kg_co2', 0))
        
        # Calculate recommendation score
        rec_score = 0
        if best_activities:
            avg_activity_score = sum(a['match_score'] for a in best_activities) / len(best_activities)
            rec_score += avg_activity_score * 0.4
        
        if best_accommodation:
            acc_score = int(best_accommodation.get('scoreDurabilite', 70))
            rec_score += acc_score * 0.3
        
        if best_transport:
            transport_score = best_transport.get('carbon', {}).get('score', 50)
            rec_score += transport_score * 0.3
        
        rec_score = min(100, rec_score)
        
        return {
            "profile": profile,
            "destination": destination,
            "duration_days": days,
            "recommendation_score": round(rec_score, 2),
            "activities": best_activities,
            "accommodation": best_accommodation,
            "transport": best_transport,
            "total_carbon_kg": round(total_co2, 2),
            "budget": budget,
            "eco_friendly": carbon_priority,
            "reasons": self._generate_reasons(profile, best_activities, best_accommodation, carbon_priority)
        }
    
    def _generate_reasons(self, profile: str, activities: List, accommodation: Dict, eco: bool) -> List[str]:
        """Génère les raisons de la recommandation"""
        reasons = []
        
        reasons.append(f"Recommandation adaptée au profil '{profile}'")
        
        if activities:
            reasons.append(f"{len(activities)} activités suggérées basées sur vos préférences")
        
        if accommodation:
            score = int(accommodation.get('scoreDurabilite', 70))
            if score >= 80:
                reasons.append(f"Hébergement très respectueux de l'environnement ({score}/100)")
            elif score >= 70:
                reasons.append(f"Hébergement écologique ({score}/100)")
        
        if eco:
            reasons.append("Options de transport à faible empreinte carbone sélectionnées")
        
        return reasons
    
    def compare_packages(self, packages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare plusieurs packages de voyage"""
        comparison = {
            "packages": [],
            "best_eco": None,
            "best_value": None,
            "best_experience": None
        }
        
        for pkg in packages:
            eco_score = 100 - (pkg.get('total_carbon_kg', 100) / 5)  # Normalize
            value_score = pkg.get('recommendation_score', 50)
            exp_score = sum(a.get('match_score', 50) for a in pkg.get('activities', [])) / max(1, len(pkg.get('activities', [])))
            
            pkg_info = {
                "profile": pkg.get('profile'),
                "eco_score": round(max(0, min(100, eco_score)), 2),
                "value_score": round(value_score, 2),
                "experience_score": round(exp_score, 2),
                "total_score": round((eco_score + value_score + exp_score) / 3, 2)
            }
            
            comparison["packages"].append(pkg_info)
        
        # Find bests
        if comparison["packages"]:
            comparison["best_eco"] = max(comparison["packages"], key=lambda x: x['eco_score'])
            comparison["best_value"] = max(comparison["packages"], key=lambda x: x['value_score'])
            comparison["best_experience"] = max(comparison["packages"], key=lambda x: x['experience_score'])
        
        return comparison
