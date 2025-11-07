"""
Verify data in Fuseki - Simple and direct queries
"""

import requests
import json

FUSEKI_URL = "http://localhost:3030"
DATASET_NAME = "tourisme-eco-2"
SPARQL_QUERY_ENDPOINT = f"{FUSEKI_URL}/{DATASET_NAME}/query"

def run_query(query, description):
    """Run a SPARQL query and display results"""
    print(f"\n🔍 {description}")
    try:
        response = requests.post(
            SPARQL_QUERY_ENDPOINT,
            data={'query': query},
            headers={'Accept': 'application/sparql-results+json'}
        )
        
        if response.status_code == 200:
            results = response.json()
            bindings = results['results']['bindings']
            
            if bindings:
                for binding in bindings:
                    for var, value in binding.items():
                        print(f"  {var}: {value['value']}")
                return len(bindings)
            else:
                print("  No results")
                return 0
        else:
            print(f"  ❌ Query failed: {response.status_code}")
            return 0
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return 0

def main():
    print("="*60)
    print("  📊 FUSEKI DATA VERIFICATION")
    print("="*60)
    
    # Total triples
    total_query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
    run_query(total_query, "Total Triples in Database")
    
    # Count destinations
    dest_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (COUNT(?s) as ?count) 
    WHERE { 
        ?s rdf:type eco:Destination 
    }
    """
    run_query(dest_query, "Destinations (direct type)")
    
    # Count destinations with subtypes
    dest_sub_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (COUNT(DISTINCT ?s) as ?count) 
    WHERE { 
        { ?s rdf:type eco:Destination }
        UNION { ?s rdf:type eco:Montagne }
        UNION { ?s rdf:type eco:Plage }
        UNION { ?s rdf:type eco:PatrimoineCulturel }
        UNION { ?s rdf:type eco:Ville }
    }
    """
    run_query(dest_sub_query, "All Destinations (including subtypes)")
    
    # Count accommodations
    heb_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (COUNT(DISTINCT ?s) as ?count) 
    WHERE { 
        { ?s rdf:type eco:Hebergement }
        UNION { ?s rdf:type eco:HotelEcologique }
        UNION { ?s rdf:type eco:GiteRural }
        UNION { ?s rdf:type eco:CampingEcoResponsable }
        UNION { ?s rdf:type eco:Auberge }
    }
    """
    run_query(heb_query, "Accommodations")
    
    # Count activities
    act_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (COUNT(DISTINCT ?s) as ?count) 
    WHERE { 
        { ?s rdf:type eco:ActiviteTouristique }
        UNION { ?s rdf:type eco:Randonnee }
        UNION { ?s rdf:type eco:Plongee }
        UNION { ?s rdf:type eco:VisiteHistorique }
        UNION { ?s rdf:type eco:ActiviteEducative }
        UNION { ?s rdf:type eco:Meditation }
        UNION { ?s rdf:type eco:Spa }
        UNION { ?s rdf:type eco:Musee }
        UNION { ?s rdf:type eco:ActiviteSportive }
    }
    """
    run_query(act_query, "Activities")
    
    # Count certifications
    cert_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (COUNT(DISTINCT ?s) as ?count) 
    WHERE { 
        { ?s rdf:type eco:CertificatEco }
        UNION { ?s rdf:type eco:LabelInternational }
        UNION { ?s rdf:type eco:LabelNational }
        UNION { ?s rdf:type eco:GreenGlobe }
        UNION { ?s rdf:type eco:EcoTourism }
    }
    """
    run_query(cert_query, "Certifications")
    
    # List all destinations
    print("\n" + "="*60)
    print("  📍 ALL DESTINATIONS:")
    print("="*60)
    list_dest_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?nom ?region
    WHERE { 
        ?s rdf:type ?type .
        ?s rdfs:label ?nom .
        OPTIONAL { ?s eco:localiseDans ?region }
        FILTER(?type IN (eco:Destination, eco:Montagne, eco:Plage, eco:PatrimoineCulturel, eco:Ville))
    }
    ORDER BY ?nom
    """
    run_query(list_dest_query, "Listing destinations...")
    
    # List all accommodations
    print("\n" + "="*60)
    print("  🏨 ALL ACCOMMODATIONS:")
    print("="*60)
    list_heb_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?nom ?prix
    WHERE { 
        ?s rdf:type ?type .
        ?s rdfs:label ?nom .
        OPTIONAL { ?s eco:prixNuit ?prix }
        FILTER(?type IN (eco:Hebergement, eco:HotelEcologique, eco:GiteRural, eco:CampingEcoResponsable, eco:Auberge))
    }
    ORDER BY ?nom
    """
    run_query(list_heb_query, "Listing accommodations...")
    
    # List all activities
    print("\n" + "="*60)
    print("  🎯 ALL ACTIVITIES:")
    print("="*60)
    list_act_query = """
    PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?nom ?duree ?prix
    WHERE { 
        ?s rdfs:label ?nom .
        OPTIONAL { ?s eco:duree ?duree }
        OPTIONAL { ?s eco:cout ?prix }
        ?s rdf:type ?type .
        FILTER(?type IN (eco:ActiviteTouristique, eco:Randonnee, eco:Plongee, eco:VisiteHistorique, 
                         eco:ActiviteEducative, eco:Meditation, eco:Spa, eco:Musee, eco:ActiviteSportive))
    }
    ORDER BY ?nom
    """
    run_query(list_act_query, "Listing activities...")
    
    print("\n" + "="*60)
    print("  ✅ VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
