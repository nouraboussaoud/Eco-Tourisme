"""
Test script to show SPARQL queries and responses for personality test
"""
import sys
sys.path.append('./backend')

from services.fuseki_client import FusekiClient
import json

def test_destinations_query():
    """Test destinations SPARQL query"""
    print("\n" + "="*80)
    print("📍 TEST: RÉCUPÉRATION DES DESTINATIONS")
    print("="*80)
    
    fuseki = FusekiClient()
    
    query = """
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
    
    print("\n📤 SPARQL QUERY:")
    print(query)
    print("\n" + "-"*80)
    
    try:
        response = fuseki.query(query)
        print("\n📥 FUSEKI RESPONSE (JSON):")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print("\n" + "-"*80)
        
        results = fuseki.parse_results(response)
        print(f"\n✅ PARSED: {len(results)} destinations trouvées\n")
        
        for i, dest in enumerate(results, 1):
            print(f"{i}. {dest.get('nom', 'N/A')}")
            print(f"   Région: {dest.get('region', 'N/A')}")
            print(f"   Score Durabilité: {dest.get('scoreDurabilite', 'N/A')}")
            print(f"   Certifications: {dest.get('certifications', 'N/A')}")
            print()
        
        print("="*80)
        return results
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def test_accommodations_query():
    """Test accommodations SPARQL query"""
    print("\n" + "="*80)
    print("🏨 TEST: RÉCUPÉRATION DES HÉBERGEMENTS")
    print("="*80)
    
    fuseki = FusekiClient()
    
    query = """
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
    
    print("\n📤 SPARQL QUERY:")
    print(query)
    print("\n" + "-"*80)
    
    try:
        response = fuseki.query(query)
        print("\n📥 FUSEKI RESPONSE (JSON):")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print("\n" + "-"*80)
        
        results = fuseki.parse_results(response)
        print(f"\n✅ PARSED: {len(results)} hébergements trouvés\n")
        
        for i, acc in enumerate(results, 1):
            print(f"{i}. {acc.get('nom', 'N/A')}")
            print(f"   Prix: {acc.get('prix', 'N/A')}€")
            print(f"   Score Durabilité: {acc.get('scoreDurabilite', 'N/A')}")
            print(f"   Destination: {acc.get('destNom', acc.get('destination', 'Non lié'))}")
            print()
        
        print("="*80)
        return results
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    print("\n🧪 TEST DES REQUÊTES SPARQL POUR LE TEST DE PERSONNALITÉ\n")
    
    destinations = test_destinations_query()
    accommodations = test_accommodations_query()
    
    print("\n" + "="*80)
    print("📊 RÉSUMÉ")
    print("="*80)
    print(f"✅ Destinations trouvées: {len(destinations)}")
    print(f"🏨 Hébergements trouvés: {len(accommodations)}")
    print("\n✅ Tests terminés!")
    print("="*80 + "\n")
