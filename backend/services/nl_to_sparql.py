# NL to SPARQL Conversion Service
import re
from typing import Dict, List, Tuple
from config import ONTOLOGY_NS, USE_GEMINI, GEMINI_API_KEY

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

# Pattern matching for French NL to SPARQL conversion
QUERY_PATTERNS = {
    r"destination.*durable|destinations.*éco|où aller|destination|région": "destinations",
    r"hébergement.*écolo|hotel.*éco|logement.*durable|où dormir|hébergement": "hebergements",
    r"activité|activités|que faire|loisir|sport|culture": "activites",
    r"transport.*éco|émission.*carbone|co2|carbone.*voyage": "transports_eco",
    r"certification.*éco|label.*vert|éco.*label|certification|green": "certifications",
    r"voyageur|profil.*voyageur|type.*touriste": "voyageurs",
    r"recommandation|suggestion|conseil|itinéraire": "recommandations",
    r"avis|commentaire|note|évaluation|retour": "avis",
    r"impacte?.*environnemental|impact.*écolog|pollution|durabilité": "impacts_eco",
}

class NLToSparqlConverter:
    """Convertit des questions en langage naturel français en requêtes SPARQL"""
    
    def __init__(self):
        if USE_GEMINI and GEMINI_AVAILABLE and GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel("gemini-pro")
            except Exception as e:
                print(f"⚠️  Gemini API configuration failed: {e}")
                self.model = None
        else:
            self.model = None
            if USE_GEMINI and not GEMINI_AVAILABLE:
                print("⚠️  google-generativeai not installed. Install with: pip install google-generativeai")
    
    def detect_query_type(self, question: str) -> str:
        """Détecte le type de requête basée sur le contenu"""
        question_lower = question.lower()
        for pattern, query_type in QUERY_PATTERNS.items():
            if re.search(pattern, question_lower, re.IGNORECASE):
                return query_type
        return "generic"
    
    def extract_city_name(self, question: str) -> str:
        """Extrait le nom d'une région/destination de la question"""
        # Liste commune de destinations touristiques
        destinations = ["paris", "lyon", "marseille", "côte d'azur", "alpes", "périgord", "bretagne", "provence", "corsica"]
        question_lower = question.lower()
        for dest in destinations:
            if dest in question_lower:
                return dest.capitalize()
        return ""
    
    def build_sparql_query(self, query_type: str, params: Dict = None) -> str:
        """Construit une requête SPARQL basée sur le type détecté"""
        ns = ONTOLOGY_NS
        params = params or {}
        
        # Préfixes standards pour toutes les requêtes
        prefixes = f"""PREFIX eco: <{ns}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

"""
        
        if query_type == "destinations":
            if params.get("city"):
                return prefixes + f"""SELECT DISTINCT ?destination ?nom ?description ?region ?certification
WHERE {{
  {{
    {{ ?destination rdf:type eco:Destination }}
    UNION {{ ?destination rdf:type eco:Montagne }}
    UNION {{ ?destination rdf:type eco:Plage }}
    UNION {{ ?destination rdf:type eco:PatrimoineCulturel }}
    UNION {{ ?destination rdf:type eco:Ville }}
  }}
  OPTIONAL {{ ?destination rdfs:label ?nom }}
  OPTIONAL {{ ?destination rdfs:comment ?description }}
  OPTIONAL {{ ?destination eco:localiseDans ?region }}
  OPTIONAL {{ ?destination eco:aCertification ?certification }}
}}"""
            else:
                return prefixes + f"""SELECT DISTINCT ?destination ?nom ?description ?region
WHERE {{
  {{
    {{ ?destination rdf:type eco:Destination }}
    UNION {{ ?destination rdf:type eco:Montagne }}
    UNION {{ ?destination rdf:type eco:Plage }}
    UNION {{ ?destination rdf:type eco:PatrimoineCulturel }}
    UNION {{ ?destination rdf:type eco:Ville }}
  }}
  OPTIONAL {{ ?destination rdfs:label ?nom }}
  OPTIONAL {{ ?destination rdfs:comment ?description }}
  OPTIONAL {{ ?destination eco:localiseDans ?region }}
}}"""
        
        elif query_type == "hebergements":
            return prefixes + f"""SELECT DISTINCT ?hebergement ?nom ?description ?prix ?capacite ?certification
WHERE {{
  {{
    {{ ?hebergement rdf:type eco:Hebergement }}
    UNION {{ ?hebergement rdf:type eco:HotelEcologique }}
    UNION {{ ?hebergement rdf:type eco:GiteRural }}
    UNION {{ ?hebergement rdf:type eco:CampingEcoResponsable }}
    UNION {{ ?hebergement rdf:type eco:Auberge }}
  }}
  OPTIONAL {{ ?hebergement rdfs:label ?nom }}
  OPTIONAL {{ ?hebergement rdfs:comment ?description }}
  OPTIONAL {{ ?hebergement eco:prixNuit ?prix }}
  OPTIONAL {{ ?hebergement eco:capacite ?capacite }}
  OPTIONAL {{ ?hebergement eco:aCertification ?certification }}
}}"""
        
        elif query_type == "activites":
            return prefixes + f"""SELECT DISTINCT ?activite ?nom ?description ?duree ?prix
WHERE {{
  {{
    {{ ?activite rdf:type eco:ActiviteTouristique }}
    UNION {{ ?activite rdf:type eco:Randonnee }}
    UNION {{ ?activite rdf:type eco:Plongee }}
    UNION {{ ?activite rdf:type eco:VisiteHistorique }}
    UNION {{ ?activite rdf:type eco:ActiviteEducative }}
    UNION {{ ?activite rdf:type eco:ActiviteCulturelle }}
    UNION {{ ?activite rdf:type eco:ActiviteSportive }}
    UNION {{ ?activite rdf:type eco:ActiviteDetente }}
    UNION {{ ?activite rdf:type eco:Meditation }}
    UNION {{ ?activite rdf:type eco:Spa }}
    UNION {{ ?activite rdf:type eco:Musee }}
    UNION {{ ?activite rdf:type eco:Atelier_culinaire }}
  }}
  OPTIONAL {{ ?activite rdfs:label ?nom }}
  OPTIONAL {{ ?activite rdfs:comment ?description }}
  OPTIONAL {{ ?activite eco:duree ?duree }}
  OPTIONAL {{ ?activite eco:cout ?prix }}
}}"""
        
        elif query_type == "transports_eco":
            return prefixes + f"""SELECT ?transport ?nom
WHERE {{
  ?transport rdf:type eco:Transport .
  OPTIONAL {{ ?transport rdfs:label ?nom }}
}}"""
        
        elif query_type == "certifications":
            return prefixes + f"""SELECT DISTINCT ?cert ?nom ?description ?organisme
WHERE {{
  {{
    {{ ?cert rdf:type eco:CertificatEco }}
    UNION {{ ?cert rdf:type eco:LabelInternational }}
    UNION {{ ?cert rdf:type eco:LabelNational }}
    UNION {{ ?cert rdf:type eco:GreenGlobe }}
    UNION {{ ?cert rdf:type eco:EcoTourism }}
  }}
  OPTIONAL {{ ?cert rdfs:label ?nom }}
  OPTIONAL {{ ?cert rdfs:comment ?description }}
  OPTIONAL {{ ?cert eco:organismeEmetteur ?organisme }}
}}"""
        
        elif query_type == "voyageurs":
            return prefixes + f"""SELECT ?voyageur ?nom
WHERE {{
  ?voyageur rdf:type eco:Voyageur .
  OPTIONAL {{ ?voyageur rdfs:label ?nom }}
}}"""
        
        elif query_type == "recommandations":
            return prefixes + f"""SELECT ?recommandation ?destination
WHERE {{
  ?recommandation rdf:type eco:Recommandation .
  OPTIONAL {{ ?recommandation eco:recommande ?destination }}
}}"""
        
        elif query_type == "impacts_eco":
            return prefixes + f"""SELECT ?element ?impact
WHERE {{
  ?element eco:aImpact ?impact .
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
Tu es un expert en SPARQL pour le tourisme éco-responsable. Convertis cette question française en requête SPARQL valide.
Utilise le namespace: {ONTOLOGY_NS}
Les classes principales sont: Destination, Hebergement, ActiviteTouristique, Voyageur, Transport, Certifications, EmpreinteCarbone, Recommandation, Avis
Les propriétés includes: aProfil, aEmpreinte, aCertification, recommande, pourVoyageur, nom, description, budget, kgCO2, scoreDurabilite, etc.

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
        return f"""PREFIX eco: <{ns}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?subject ?predicate ?object
WHERE {{
  ?subject ?predicate ?object .
}}
LIMIT 100"""
