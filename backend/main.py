# FastAPI Main Application
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import json
from datetime import datetime
from services import FusekiClient, NLToSparqlConverter
from services.recommendation_engine import RecommendationEngine
from services.personality_test_service import PersonalityTestService
from config import CORS_ORIGINS, BACKEND_PORT, ONTOLOGY_NS
from example_queries import EXAMPLE_QUERIES

# Initialize FastAPI app
app = FastAPI(
    title="Tourisme Éco-responsable - NL to SPARQL API",
    description="API pour convertir des questions en langage naturel français en requêtes SPARQL pour le tourisme durable",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
# Use Real Fuseki Client with your dataset
print("🔧 Connecting to Real Fuseki Server at /tourisme-eco-2")
try:
    fuseki_client = FusekiClient()
    fuseki_client.query("SELECT * WHERE { ?s ?p ?o . } LIMIT 1")
    print("✅ Successfully connected to Fuseki!")
except Exception as e:
    print(f"⚠️  Fuseki not available, using mock client: {str(e)}")
    from services.mock_fuseki_client import MockFusekiClient
    fuseki_client = MockFusekiClient()

nl_converter = NLToSparqlConverter()
recommendation_engine = RecommendationEngine(fuseki_client=fuseki_client)
personality_test_service = PersonalityTestService(fuseki_client=fuseki_client)

# Pydantic models
class QueryRequest(BaseModel):
    question: str = Query(..., description="Question en français")
    
class QueryResponse(BaseModel):
    question: str
    sparql_query: str
    results: List[Dict[str, str]]
    execution_time: float

class AvisVoyageurRequest(BaseModel):
    voyageur: str
    attraction_id: str
    note: float = Query(..., ge=1, le=5, description="Note de 1 à 5")
    commentaire: str
    type_attraction: str = "destination"  # destination, hebergement, activite

class SignalementEcoRequest(BaseModel):
    voyageur: str
    destination: str
    type_signalement: str  # pollution, destruction, non-respect_eco
    description: str

class RecommendationRequest(BaseModel):
    profile: str = Query(..., description="Profil voyageur: Adventure, Culture, BienEtre, Famille")
    destination: str = Query(..., description="Destination")
    budget: Optional[float] = Query(1000, description="Budget en euros")
    carbon_priority: Optional[bool] = Query(False, description="Priorité à l'écologie")
    days: Optional[int] = Query(3, description="Nombre de jours")

class PersonalityTestAnswers(BaseModel):
    answers: Dict[str, str] = Query(..., description="Réponses au test de personnalité (question_id: answer_value)")

# Routes

@app.get("/health", tags=["Health"])
async def health_check():
    """Vérifier la santé de l'API"""
    try:
        # Test connection to Fuseki
        test_query = f"""PREFIX wm: <{ONTOLOGY_NS}>
SELECT (COUNT(*) as ?count)
WHERE {{
  ?s ?p ?o .
}}"""
        fuseki_client.query(test_query)
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "fuseki": "connected",
                "nl_converter": "ready"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/query", response_model=QueryResponse, tags=["NL Query"])
@app.post("/query/nl", response_model=QueryResponse, tags=["NL Query"])
async def natural_language_query(req: QueryRequest):
    """Convertit une question en langage naturel en requête SPARQL et exécute"""
    try:
        start_time = datetime.now()
        
        # Convert NL question to SPARQL
        sparql_query = nl_converter.convert_question_to_sparql(req.question)
        
        # Execute SPARQL query
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return QueryResponse(
            question=req.question,
            sparql_query=sparql_query,
            results=results,
            execution_time=execution_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/sparql", tags=["Direct SPARQL"])
async def direct_sparql_query(query: str = Form(...)):
    """Exécute une requête SPARQL directe (INSERT, SELECT, etc.)"""
    try:
        # Si c'est une requête UPDATE/INSERT
        if "INSERT" in query.upper() or "DELETE" in query.upper():
            success = fuseki_client.update(query)
            return {
                "status": "success" if success else "failed",
                "message": "Requête UPDATE exécutée",
                "query": query[:200] + "..." if len(query) > 200 else query
            }
        # Sinon c'est un SELECT
        else:
            results_json = fuseki_client.query(query)
            results = fuseki_client.parse_results(results_json)
            return {
                "query": query,
                "results": results,
                "count": len(results)
            }
    except Exception as e:
        import traceback
        error_detail = f"Erreur SPARQL: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ SPARQL Error: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)

@app.post("/avis", tags=["Community"])
async def add_avis(req: AvisVoyageurRequest):
    """Ajoute un avis sur une attraction"""
    try:
        avis_id = f"avis_{datetime.now().timestamp()}"
        sparql_update = f"""PREFIX eco: <{ONTOLOGY_NS}>
INSERT DATA {{
  eco:{avis_id} rdf:type eco:Avis ;
    eco:note {req.note} ;
    eco:voyageur "{req.voyageur}" ;
    eco:surAttraction "{req.attraction_id}" ;
    eco:typeAttraction "{req.type_attraction}" ;
    eco:commentaire "{req.commentaire}" ;
    eco:dateAvis "{datetime.now().isoformat()}"^^xsd:dateTime .
}}"""
        
        fuseki_client.update(sparql_update)
        return {
            "status": "success",
            "avis_id": avis_id,
            "message": "Avis ajouté avec succès"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/signalement-eco", tags=["Community"])
async def add_signalement(req: SignalementEcoRequest):
    """Signale un problème écologique"""
    try:
        signalement_id = f"signalement_{datetime.now().timestamp()}"
        sparql_update = f"""PREFIX eco: <{ONTOLOGY_NS}>
INSERT DATA {{
  eco:{signalement_id} rdf:type eco:SignalementEnvironnemental ;
    eco:voyageur "{req.voyageur}" ;
    eco:destination "{req.destination}" ;
    eco:typeProblem "{req.type_signalement}" ;
    eco:description "{req.description}" ;
    eco:dateSignalement "{datetime.now().isoformat()}"^^xsd:dateTime .
}}"""
        
        fuseki_client.update(sparql_update)
        return {
            "status": "success",
            "signalement_id": signalement_id,
            "message": "Signalement enregistré avec succès"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/examples", tags=["Examples"])
async def get_example_queries():
    """Retourne les requêtes d'exemple"""
    return {
        "examples": EXAMPLE_QUERIES,
        "description": "Exemples de requêtes SPARQL"
    }

@app.get("/destinations", tags=["Data"])
async def get_destinations(region: Optional[str] = None):
    """Récupère toutes les destinations éco-responsables"""
    try:
        if region:
            question = f"Quelles sont les destinations durables dans {region}?"
        else:
            question = "Quelles sont les destinations éco-responsables?"
        
        print(f"🔍 Destinations - Question: {question}")
        sparql_query = nl_converter.convert_question_to_sparql(question)
        print(f"🔍 Destinations - SPARQL: {sparql_query[:200]}...")
        results_json = fuseki_client.query(sparql_query)
        print(f"🔍 Destinations - JSON keys: {results_json.keys() if isinstance(results_json, dict) else type(results_json)}")
        results = fuseki_client.parse_results(results_json)
        print(f"✅ Destinations - Found {len(results)} results")
        
        return {
            "destinations": results,
            "count": len(results),
            "region": region
        }
    except Exception as e:
        import traceback
        error_msg = f"Erreur destinations: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/hebergements", tags=["Data"])
async def get_hebergements(eco_certified: Optional[bool] = False):
    """Récupère les hébergements écologiques"""
    try:
        if eco_certified:
            question = "Quels sont les hébergements certifiés écologiques?"
        else:
            question = "Quels sont les hébergements éco-responsables?"
        
        print(f"🔍 Hebergements - Question: {question}")
        sparql_query = nl_converter.convert_question_to_sparql(question)
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        print(f"✅ Hebergements - Found {len(results)} results")
        return {
            "hebergements": results,
            "count": len(results),
            "certified_only": eco_certified
        }
    except Exception as e:
        import traceback
        error_msg = f"Erreur hebergements: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/activites", tags=["Data"])
async def get_activites(type_activite: Optional[str] = None):
    """Récupère les activités éco-responsables"""
    try:
        if type_activite:
            question = f"Quelles sont les activités {type_activite}?"
        else:
            question = "Quelles sont les activités disponibles?"
        
        sparql_query = nl_converter.convert_question_to_sparql(question)
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        return {
            "activites": results,
            "count": len(results),
            "type": type_activite
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/certifications", tags=["Data"])
async def get_certifications():
    """Récupère les certifications écologiques"""
    try:
        sparql_query = nl_converter.convert_question_to_sparql("Quelles sont les certifications écologiques?")
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        return {
            "certifications": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/stats", tags=["Analytics"])
async def get_community_stats():
    """Récupère les statistiques du tourisme éco-responsable"""
    try:
        sparql_query = f"""PREFIX eco: <{ONTOLOGY_NS}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT (COUNT(DISTINCT ?voyageur) as ?totalVoyageurs)
       (COUNT(DISTINCT ?destination) as ?totalDestinations)
       (COUNT(DISTINCT ?hebergement) as ?totalHebergements)
       (COUNT(DISTINCT ?activite) as ?totalActivites)
WHERE {{
  OPTIONAL {{ ?voyageur rdf:type eco:Voyageur }}
  OPTIONAL {{ ?destination rdf:type eco:Destination }}
  OPTIONAL {{ ?hebergement rdf:type eco:Hebergement }}
  OPTIONAL {{ ?activite rdf:type eco:ActiviteTouristique }}
}}"""
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        return {
            "statistics": results[0] if results else {},
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/docs", include_in_schema=True)
async def get_docs():
    """Documentation OpenAPI"""
    return app.openapi()

# ================================ -->
# ENDPOINTS DE RECOMMANDATIONS  -->
# ================================ -->

@app.get("/recommendation/profiles", tags=["Recommendations"])
async def get_available_profiles():
    """Récupère les profils de voyageurs disponibles"""
    return {
        "profiles": [
            {
                "id": "Adventure",
                "name": "Aventurier",
                "description": "Préfère les activités sportives et la nature",
                "preferences": ["Randonnée", "Plongée", "Activités sportives"]
            },
            {
                "id": "Culture",
                "name": "Culturel",
                "description": "Intéressé par la culture et le patrimoine",
                "preferences": ["Musées", "Visites historiques", "Ateliers d'artisanat"]
            },
            {
                "id": "BienEtre",
                "name": "Bien-Être",
                "description": "Cherche relaxation et détente",
                "preferences": ["Spa", "Méditation", "Activités de détente"]
            },
            {
                "id": "Famille",
                "name": "Famille",
                "description": "Voyage en famille",
                "preferences": ["Activités ludiques", "Lieux adaptés aux enfants"]
            }
        ]
    }

@app.post("/recommendation/generate", tags=["Recommendations"])
async def generate_recommendation(
    profile: str = Query(..., description="Profil voyageur"),
    destination: str = Query(..., description="Destination"),
    budget: Optional[float] = Query(1000),
    carbon_priority: Optional[bool] = Query(False),
    days: Optional[int] = Query(3)
):
    """Génère une recommandation personnalisée"""
    try:
        recommendation = recommendation_engine.generate_recommendation(
            profile=profile,
            destination=destination,
            budget=budget,
            carbon_priority=carbon_priority,
            days=days
        )
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/recommendation/carbon-calculator", tags=["Recommendations"])
async def carbon_calculator(
    transport_type: str = Query("Avion"),
    distance_km: float = Query(1000)
):
    """Calcule l'empreinte carbone d'un transport"""
    # CO2 emissions (kg per km)
    emission_factors = {
        "Avion": 0.255,
        "Train": 0.041,
        "Bus": 0.089,
        "Voiture": 0.192,
        "Velo": 0.0
    }
    
    factor = emission_factors.get(transport_type, 0.2)
    total_co2 = distance_km * factor
    carbon_score = recommendation_engine.calculate_carbon_score(total_co2)
    
    return {
        "transport": transport_type,
        "distance_km": distance_km,
        "total_co2_kg": round(total_co2, 2),
        "carbon_level": carbon_score["level"],
        "carbon_score": carbon_score["score"],
        "alternatives": [
            {
                "transport": "Train",
                "co2_kg": round(distance_km * emission_factors["Train"], 2),
                "savings": round(total_co2 - (distance_km * emission_factors["Train"]), 2)
            }
        ]
    }

@app.get("/recommendation/activities", tags=["Recommendations"])
async def get_recommended_activities(profile: str = Query(...)):
    """Récupère les activités recommandées pour un profil"""
    try:
        activities = recommendation_engine.get_activities_for_profile(profile)
        return {
            "profile": profile,
            "activities": activities[:10],
            "total": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/recommendation/accommodations", tags=["Recommendations"])
async def get_recommended_accommodations(profile: str = Query(...)):
    """Récupère les hébergements recommandés"""
    try:
        accommodations = recommendation_engine.get_accommodations_for_profile(profile)
        return {
            "profile": profile,
            "accommodations": accommodations,
            "total": len(accommodations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/recommendation/transports", tags=["Recommendations"])
async def get_transport_options(carbon_sensitive: bool = Query(False)):
    """Récupère les options de transport"""
    try:
        transports = recommendation_engine.get_transport_options(carbon_sensitive)
        return {
            "carbon_sensitive": carbon_sensitive,
            "transports": transports,
            "total": len(transports)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ================================ -->
# PERSONALITY TEST & TRIP PACKAGES -->
# ================================ -->

@app.get("/personality-test/questions", tags=["Personality Test"])
async def get_personality_test_questions():
    """Récupère les questions du test de personnalité"""
    try:
        questions = personality_test_service.get_questions()
        return {
            "questions": questions,
            "total_questions": len(questions),
            "description": "Test de personnalité pour recommandations de voyage personnalisées"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/personality-test/analyze", tags=["Personality Test"])
async def analyze_personality_test(request: PersonalityTestAnswers):
    """Analyse les réponses du test de personnalité et retourne le profil"""
    try:
        # Récupérer les destinations pour informer l'IA
        places_query = """
        PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?nom ?type ?scoreDurabilite ?certifications
        WHERE {
            ?place rdf:type eco:Destination .
            ?place eco:nom ?nom .
            OPTIONAL { ?place eco:type ?type }
            OPTIONAL { ?place eco:scoreDurabilite ?scoreDurabilite }
            OPTIONAL { ?place eco:certifications ?certifications }
        }
        """
        
        try:
            places_json = fuseki_client.query(places_query)
            available_places = fuseki_client.parse_results(places_json)
        except:
            available_places = []
        
        # Analyser avec Gemini AI ou fallback
        personality_profile = personality_test_service.analyze_personality_with_ai(
            request.answers,
            available_destinations=available_places
        )
        
        return {
            "status": "success",
            "personality_profile": personality_profile,
            "message": "Profil de personnalité généré avec succès"
        }
    except Exception as e:
        import traceback
        error_msg = f"Erreur analyse personnalité: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/personality-test/generate-package", tags=["Personality Test"])
async def generate_trip_package_from_test(request: PersonalityTestAnswers):
    """Génère un package de voyage complet basé sur le test de personnalité"""
    try:
        # 1. Récupérer TOUTES les destinations disponibles avec leurs certifications via SPARQL (ONLY REAL DATA)
        print("\n" + "="*80)
        print("📍 RÉCUPÉRATION DES DESTINATIONS DEPUIS FUSEKI")
        print("="*80)
        
        places_query = """
        PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?nom ?type ?description ?scoreDurabilite ?certifications ?region
        WHERE {
            ?dest rdf:type ?type .
            FILTER(?type IN (eco:Destination, eco:Montagne, eco:Plage, eco:PatrimoineCulturel, eco:Ville))
            ?dest rdfs:label ?nom .
            OPTIONAL { ?dest eco:description ?description }
            OPTIONAL { ?dest eco:scoreDurabilite ?scoreDurabilite }
            OPTIONAL { ?dest eco:certifications ?certifications }
            OPTIONAL { ?dest eco:localiseDans ?region }
        }
        ORDER BY DESC(?scoreDurabilite) ?nom
        """
        
        print("📤 SPARQL QUERY SENT:")
        print(places_query)
        print("-"*80)
        
        try:
            places_json = fuseki_client.query(places_query)
            print("📥 FUSEKI RESPONSE (RAW JSON):")
            print(json.dumps(places_json, indent=2, ensure_ascii=False)[:1500] + "...")
            print("-"*80)
            
            available_places = fuseki_client.parse_results(places_json)
            print(f"✅ PARSED RESULTS: {len(available_places)} destinations trouvées")
            for i, place in enumerate(available_places[:3], 1):
                print(f"   {i}. {place.get('nom', 'N/A')} - {place.get('region', 'N/A')} (Score: {place.get('scoreDurabilite', 'N/A')})")
            print("="*80 + "\n")
            
            # NO MOCK DATA - Destinations are REQUIRED
            if not available_places or len(available_places) == 0:
                raise HTTPException(
                    status_code=500, 
                    detail="Aucune destination trouvée dans la base de données Fuseki. Veuillez ajouter des destinations."
                )
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ ERREUR SPARQL DESTINATIONS: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération des destinations: {str(e)}"
            )
        
        # 2. Analyser la personnalité avec les vraies destinations
        print("🧠 Analyse du profil avec Gemini AI...")
        personality_profile = personality_test_service.analyze_personality_with_ai(
            request.answers, 
            available_destinations=available_places
        )
        print(f"✅ Profil généré: {personality_profile.get('personality_type')}")
        
        # 3. Récupérer TOUS les hébergements disponibles avec leurs destinations
        print("\n" + "="*80)
        print("🏨 RÉCUPÉRATION DES HÉBERGEMENTS DEPUIS FUSEKI")
        print("="*80)
        
        accommodations_query = """
        PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?nom ?type ?scoreDurabilite ?certifications ?prix ?destination ?destNom
        WHERE {
            ?acc rdf:type ?type .
            FILTER(?type IN (eco:Hebergement, eco:HotelEcologique, eco:GiteRural, eco:CampingEcoResponsable, eco:Auberge))
            ?acc rdfs:label ?nom .
            OPTIONAL { ?acc eco:scoreDurabilite ?scoreDurabilite }
            OPTIONAL { ?acc eco:certifications ?certifications }
            OPTIONAL { ?acc eco:prixNuit ?prix }
            OPTIONAL { 
                ?acc eco:situeDans ?destination .
                ?destination rdfs:label ?destNom 
            }
        }
        ORDER BY DESC(?scoreDurabilite) ?nom
        """
        
        print("📤 SPARQL QUERY SENT:")
        print(accommodations_query)
        print("-"*80)
        
        try:
            acc_json = fuseki_client.query(accommodations_query)
            print("📥 FUSEKI RESPONSE (RAW JSON):")
            print(json.dumps(acc_json, indent=2, ensure_ascii=False)[:1500] + "...")
            print("-"*80)
            
            available_accommodations = fuseki_client.parse_results(acc_json)
            print(f"✅ PARSED RESULTS: {len(available_accommodations)} hébergements trouvés")
            for i, acc in enumerate(available_accommodations[:3], 1):
                dest = acc.get('destNom', acc.get('destination', 'Non lié'))
                print(f"   {i}. {acc.get('nom', 'N/A')} - {acc.get('prix', 'N/A')}€ (Destination: {dest})")
            print("="*80 + "\n")
            
            # Accommodations are OPTIONAL (destinations are primary)
            if not available_accommodations or len(available_accommodations) == 0:
                print("ℹ️  Aucun hébergement trouvé - Le package sera basé uniquement sur les destinations")
                available_accommodations = []
        except Exception as e:
            print(f"⚠️ ERREUR SPARQL HÉBERGEMENTS: {str(e)}")
            print("ℹ️  Continuons avec 0 hébergements - destinations sont prioritaires")
            available_accommodations = []
        
        # 4. Générer le package de voyage avec destinations et hébergements liés
        print("📦 Génération du package de voyage personnalisé...")
        trip_package = personality_test_service.generate_trip_package(
            personality_profile=personality_profile,
            available_places=available_places,
            available_accommodations=available_accommodations
        )
        
        print(f"✅ Package généré avec {len(trip_package.get('places', []))} destinations")
        
        return {
            "status": "success",
            "personality_profile": personality_profile,
            "trip_package": trip_package,
            "message": "Package de voyage généré avec succès",
            "data_sources": {
                "total_destinations_available": len(available_places),
                "total_accommodations_available": len(available_accommodations),
                "destinations_in_package": len(trip_package.get('places', [])),
                "accommodations_in_package": len(trip_package.get('accommodations', [])),
                "sparql_used": True
            }
        }
    except Exception as e:
        import traceback
        error_msg = f"Erreur génération package: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/personality-test/sample-package", tags=["Personality Test"])
async def get_sample_trip_package(personality_type: str = Query("adventure")):
    """Génère un package de voyage exemple pour tester"""
    try:
        # Créer un profil exemple
        sample_answers = {
            "1": "adventure" if personality_type == "adventure" else "culture",
            "2": "very_high",
            "3": "eco_lodge",
            "4": "medium",
            "5": "moderate",
            "6": "train",
            "7": "authentic"
        }
        
        # Analyser
        personality_profile = personality_test_service.analyze_personality_with_ai(sample_answers)
        
        # Données mock pour démo
        available_places = [
            {"nom": "Parc National des Pyrénées", "type": "Nature", "scoreDurabilite": "85", "certifications": "ISO 14001, Green Globe"},
            {"nom": "Éco-Village de Provence", "type": "Culturel", "scoreDurabilite": "90", "certifications": "Bio, Eco-Label"},
            {"nom": "Réserve Marine de Méditerranée", "type": "Nature", "scoreDurabilite": "88", "certifications": "Marine Conservation"},
            {"nom": "Centre Historique d'Avignon", "type": "Culturel", "scoreDurabilite": "75", "certifications": "UNESCO"},
            {"nom": "Sentier Écologique des Alpes", "type": "Nature", "scoreDurabilite": "92", "certifications": "Eco-Trail"},
            {"nom": "Vignoble Biodynamique", "type": "Gastronomie", "scoreDurabilite": "87", "certifications": "Bio, Demeter"}
        ]
        
        available_accommodations = [
            {"nom": "Éco-Lodge du Parc", "type": "Lodge", "scoreDurabilite": "88", "certifications": "Green Key", "prix": "120"},
            {"nom": "Maison d'Hôtes Bio", "type": "Guesthouse", "scoreDurabilite": "85", "certifications": "Bio, Ecolabel", "prix": "80"}
        ]
        
        # Générer package
        trip_package = personality_test_service.generate_trip_package(
            personality_profile=personality_profile,
            available_places=available_places,
            available_accommodations=available_accommodations
        )
        
        return {
            "status": "success",
            "personality_profile": personality_profile,
            "trip_package": trip_package,
            "note": "Ceci est un exemple de démonstration"
        }
    except Exception as e:
        import traceback
        error_msg = f"Erreur package exemple: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

# Entry point
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=True
    )
