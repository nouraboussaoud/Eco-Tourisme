# FastAPI Main Application
from fastapi import FastAPI, HTTPException, Query, File, UploadFile
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
    title="Waste Management NL to SPARQL API",
    description="API pour convertir des questions en langage naturel français en requêtes SPARQL",
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
fuseki_client = FusekiClient()
nl_converter = NLToSparqlConverter()
recommendation_engine = RecommendationEngine()

# Pydantic models
class QueryRequest(BaseModel):
    question: str = Query(..., description="Question en français")
    
class QueryResponse(BaseModel):
    question: str
    sparql_query: str
    results: List[Dict[str, str]]
    execution_time: float

class ContributionRequest(BaseModel):
    utilisateur: str
    description: str
    type: str = "contribution"
    quantite: Optional[float] = None
    unite: Optional[str] = None

class CommentRequest(BaseModel):
    contribution_id: str
    utilisateur: str
    text: str

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
async def direct_sparql_query(query: str = Query(..., description="Requête SPARQL")):
    """Exécute une requête SPARQL directe"""
    try:
        results_json = fuseki_client.query(query)
        results = fuseki_client.parse_results(results_json)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur SPARQL: {str(e)}")

@app.post("/contribution", tags=["Community"])
async def add_contribution(req: ContributionRequest):
    """Ajoute une nouvelle contribution"""
    try:
        contribution_id = f"contribution_{datetime.now().timestamp()}"
        sparql_update = f"""PREFIX wm: <{ONTOLOGY_NS}>
INSERT DATA {{
  wm:{contribution_id} rdf:type wm:Contribution ;
    wm:description "{req.description}" ;
    wm:dateCreation "{datetime.now().isoformat()}"^^xsd:dateTime ;
    wm:quantite {req.quantite or 0} ;
    wm:unite "{req.unite or 'unité'}" .
}}"""
        
        fuseki_client.update(sparql_update)
        return {
            "status": "success",
            "contribution_id": contribution_id,
            "message": "Contribution ajoutée avec succès"
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

@app.get("/collection-points", tags=["Data"])
async def get_collection_points(city: Optional[str] = None):
    """Récupère tous les points de collecte"""
    try:
        if city:
            question = f"Quels sont les points de collecte à {city}?"
        else:
            question = "Quels sont les points de collecte?"
        
        sparql_query = nl_converter.convert_question_to_sparql(question)
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        
        return {
            "collection_points": results,
            "count": len(results),
            "city": city
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/waste-types", tags=["Data"])
async def get_waste_types():
    """Récupère tous les types de déchets"""
    try:
        sparql_query = nl_converter.convert_question_to_sparql("Quels sont les types de déchets?")
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        return {
            "waste_types": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/activities", tags=["Community"])
async def get_activities():
    """Récupère toutes les activités communautaires"""
    try:
        sparql_query = nl_converter.convert_question_to_sparql("Quelles sont les activités?")
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        return {
            "activities": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/badges", tags=["Community"])
async def get_badges():
    """Récupère tous les badges disponibles"""
    try:
        sparql_query = nl_converter.convert_question_to_sparql("Quels sont les badges?")
        results_json = fuseki_client.query(sparql_query)
        results = fuseki_client.parse_results(results_json)
        return {
            "badges": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/stats", tags=["Analytics"])
async def get_community_stats():
    """Récupère les statistiques communautaires"""
    try:
        sparql_query = f"""PREFIX wm: <{ONTOLOGY_NS}>
SELECT (COUNT(DISTINCT ?utilisateur) as ?totalUsers)
       (COUNT(DISTINCT ?activite) as ?totalActivities)
       (COUNT(DISTINCT ?point) as ?totalPoints)
WHERE {{
  OPTIONAL {{ ?utilisateur rdf:type wm:Utilisateur }}
  OPTIONAL {{ ?activite rdf:type wm:Activite }}
  OPTIONAL {{ ?point rdf:type wm:PointCollecte }}
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
