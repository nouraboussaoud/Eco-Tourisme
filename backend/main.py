# FastAPI Main Application
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from datetime import datetime
from services import FusekiClient, NLToSparqlConverter
from services.recommendation_engine import RecommendationEngine
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

# Entry point
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=True
    )
