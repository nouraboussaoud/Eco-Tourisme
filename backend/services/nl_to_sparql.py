# NL to SPARQL Conversion Service
import re
from typing import Dict, List, Tuple
from config import ONTOLOGY_NS, USE_GEMINI
import google.generativeai as genai
from config import GEMINI_API_KEY

# Pattern matching for French NL to SPARQL conversion
QUERY_PATTERNS = {
    r"quels.*points.*collecte|points de collecte|déchèteries": "points_collecte",
    r"quels.*types.*déchets|types de déchets|déchets acceptés": "types_dechets",
    r"quels.*déchets.*acceptés": "dechets_acceptes",
    r"toutes.*villes|villes|quelles villes": "villes",
    r"quartier|quartiers": "quartiers",
    r"activités|événements|défis|engagements": "activites",
    r"utilisateur|participant|citoyen": "utilisateurs",
    r"badge|récompense": "badges",
    r"contribution|participation": "contributions",
}

class NLToSparqlConverter:
    """Convertit des questions en langage naturel français en requêtes SPARQL"""
    
    def __init__(self):
        if USE_GEMINI and GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-pro")
        else:
            self.model = None
    
    def detect_query_type(self, question: str) -> str:
        """Détecte le type de requête basée sur le contenu"""
        question_lower = question.lower()
        for pattern, query_type in QUERY_PATTERNS.items():
            if re.search(pattern, question_lower, re.IGNORECASE):
                return query_type
        return "generic"
    
    def extract_city_name(self, question: str) -> str:
        """Extrait le nom d'une ville de la question"""
        # Liste commune de villes français
        cities = ["paris", "lyon", "marseille", "toulouse", "nice", "nantes", "bordeaux"]
        question_lower = question.lower()
        for city in cities:
            if city in question_lower:
                return city.capitalize()
        return ""
    
    def build_sparql_query(self, query_type: str, params: Dict = None) -> str:
        """Construit une requête SPARQL basée sur le type"""
        ns = ONTOLOGY_NS
        
        if query_type == "points_collecte":
            city = params.get("city", "") if params else ""
            if city:
                return f"""PREFIX wm: <{ns}>
SELECT ?point ?nom ?adresse ?latitude ?longitude ?horaires
WHERE {{
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:latitude ?latitude .
  ?point wm:longitude ?longitude .
  ?point wm:horaires ?horaires .
  ?point wm:localiseDans ?ville .
  ?ville wm:nom "{city}" .
}}"""
            else:
                return f"""PREFIX wm: <{ns}>
SELECT ?point ?nom ?adresse ?horaires
WHERE {{
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:horaires ?horaires .
}}"""
        
        elif query_type == "types_dechets":
            return f"""PREFIX wm: <{ns}>
SELECT ?type ?nom ?description
WHERE {{
  ?type rdf:type wm:TypeDechet .
  ?type wm:nom ?nom .
  OPTIONAL {{ ?type wm:description ?description }}
}}"""
        
        elif query_type == "dechets_acceptes":
            return f"""PREFIX wm: <{ns}>
SELECT DISTINCT ?point ?nom ?accepte
WHERE {{
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:accepte ?accepte .
  ?accepte wm:nom ?typeName .
}}"""
        
        elif query_type == "villes":
            return f"""PREFIX wm: <{ns}>
SELECT DISTINCT ?ville ?nom
WHERE {{
  ?ville rdf:type wm:Ville .
  ?ville wm:nom ?nom .
}}"""
        
        elif query_type == "activites":
            return f"""PREFIX wm: <{ns}>
SELECT ?activite ?nom ?description ?date
WHERE {{
  ?activite rdf:type wm:Activite .
  ?activite wm:nom ?nom .
  OPTIONAL {{ ?activite wm:description ?description }}
  OPTIONAL {{ ?activite wm:dateActivite ?date }}
}}"""
        
        elif query_type == "badges":
            return f"""PREFIX wm: <{ns}>
SELECT ?badge ?nom ?description
WHERE {{
  ?badge rdf:type wm:Badge .
  ?badge wm:nom ?nom .
  OPTIONAL {{ ?badge wm:description ?description }}
}}"""
        
        elif query_type == "utilisateurs":
            return f"""PREFIX wm: <{ns}>
SELECT ?utilisateur ?nom ?email
WHERE {{
  ?utilisateur rdf:type wm:Utilisateur .
  ?utilisateur wm:nom ?nom .
  OPTIONAL {{ ?utilisateur wm:email ?email }}
}}"""
        
        elif query_type == "contributions":
            return f"""PREFIX wm: <{ns}>
SELECT ?contribution ?description ?date ?utilisateur
WHERE {{
  ?contribution rdf:type wm:Contribution .
  OPTIONAL {{ ?contribution wm:description ?description }}
  OPTIONAL {{ ?contribution wm:dateCreation ?date }}
  OPTIONAL {{ ?utilisateur wm:aContribution ?contribution }}
}}"""
        
        return ""
    
    def convert_question_to_sparql(self, question: str) -> str:
        """Convertit une question française en requête SPARQL"""
        
        # Si USE_GEMINI est activé, utiliser l'API Gemini
        if USE_GEMINI and self.model:
            return self._convert_with_gemini(question)
        
        # Sinon, utiliser pattern matching
        query_type = self.detect_query_type(question)
        params = {}
        
        # Extraire la ville si mentionnée
        city = self.extract_city_name(question)
        if city:
            params["city"] = city
        
        sparql_query = self.build_sparql_query(query_type, params)
        return sparql_query if sparql_query else self._build_generic_query(question)
    
    def _convert_with_gemini(self, question: str) -> str:
        """Utilise Gemini pour convertir la question en SPARQL"""
        prompt = f"""
Tu es un expert en SPARQL et en langage naturel. Convertis cette question française en requête SPARQL valide.
Utilise le namespace: {ONTOLOGY_NS}
Les classes principales sont: Dechet, TypeDechet, PointCollecte, Utilisateur, Activite, Evenement, Defi, Badge, Points, Contribution, Commentaire
Les propriétés includes: aType, localiseDans, accepte, participant, aContribution, aBadge, aCommentaire, aEffectue, nom, description, adresse, etc.

Question: {question}

Réponds UNIQUEMENT avec la requête SPARQL sans explications additionnelles.
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback sur pattern matching
            query_type = self.detect_query_type(question)
            return self.build_sparql_query(query_type)
    
    def _build_generic_query(self, question: str) -> str:
        """Construit une requête générique pour questions non reconnues"""
        ns = ONTOLOGY_NS
        return f"""PREFIX wm: <{ns}>
SELECT ?subject ?predicate ?object
WHERE {{
  ?subject ?predicate ?object .
}}
LIMIT 100"""
