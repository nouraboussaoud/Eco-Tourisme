#!/usr/bin/env python3
"""Script de diagnostic pour tester la connexion Fuseki"""

import requests
import sys
from config import FUSEKI_ENDPOINT, ONTOLOGY_NS

def test_fuseki_connection():
    """Teste la connexion au serveur Fuseki"""
    print("=" * 60)
    print("🔍 DIAGNOSTIC DE CONNEXION FUSEKI")
    print("=" * 60)
    
    # 1. Test de connexion au serveur
    print("\n1️⃣ Test de connexion au serveur Fuseki...")
    try:
        base_url = FUSEKI_ENDPOINT.replace("/sparql", "")
        fuseki_root = base_url.rsplit("/", 1)[0]
        
        response = requests.get(fuseki_root, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Serveur Fuseki accessible sur {fuseki_root}")
        else:
            print(f"   ⚠️  Serveur répond mais statut: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ ERREUR: Fuseki n'est pas démarré sur {fuseki_root}")
        print(f"   💡 Solution: Démarrez Fuseki avec:")
        print(f"      cd C:\\apache-jena-fuseki-5.6.0")
        print(f"      .\\fuseki-server.bat")
        return False
    except Exception as e:
        print(f"   ❌ Erreur inattendue: {e}")
        return False
    
    # 2. Test de l'endpoint SPARQL
    print(f"\n2️⃣ Test de l'endpoint SPARQL...")
    print(f"   Endpoint: {FUSEKI_ENDPOINT}")
    try:
        test_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 1"
        response = requests.post(
            FUSEKI_ENDPOINT,
            data=test_query,
            headers={
                "Accept": "application/sparql-results+json",
                "Content-Type": "application/sparql-query"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            bindings = results.get("results", {}).get("bindings", [])
            print(f"   ✅ Endpoint SPARQL fonctionnel")
            print(f"   📊 Nombre de triplets retournés: {len(bindings)}")
            
            if len(bindings) == 0:
                print(f"\n   ⚠️  WARNING: Le dataset est VIDE!")
                print(f"   💡 Solution: Uploadez votre fichier RDF dans Fuseki:")
                print(f"      1. Ouvrir http://localhost:3030")
                print(f"      2. Sélectionner votre dataset")
                print(f"      3. Onglet 'upload data'")
                print(f"      4. Uploader votre fichier eco-toursime.rdf")
            else:
                print(f"\n   ✅ Dataset contient des données!")
                print(f"   Premier triplet:")
                if bindings:
                    for key, val in bindings[0].items():
                        print(f"      {key}: {val.get('value', 'N/A')}")
        else:
            print(f"   ❌ Erreur: Statut HTTP {response.status_code}")
            print(f"   Réponse: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur requête SPARQL: {e}")
        return False
    
    # 3. Test des classes de l'ontologie
    print(f"\n3️⃣ Test des classes de l'ontologie...")
    print(f"   Namespace: {ONTOLOGY_NS}")
    try:
        classes_query = f"""
        PREFIX eco: <{ONTOLOGY_NS}>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?class
        WHERE {{
            ?class a owl:Class .
        }}
        LIMIT 10
        """
        
        response = requests.post(
            FUSEKI_ENDPOINT,
            data=classes_query,
            headers={
                "Accept": "application/sparql-results+json",
                "Content-Type": "application/sparql-query"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            bindings = results.get("results", {}).get("bindings", [])
            print(f"   ✅ Trouvé {len(bindings)} classes dans l'ontologie")
            
            if bindings:
                print(f"\n   Classes détectées:")
                for binding in bindings[:5]:
                    class_uri = binding.get("class", {}).get("value", "")
                    class_name = class_uri.split("#")[-1].split("/")[-1]
                    print(f"      • {class_name}")
                    
                if len(bindings) > 5:
                    print(f"      ... et {len(bindings) - 5} autres")
        else:
            print(f"   ⚠️  Impossible de lister les classes (statut {response.status_code})")
            
    except Exception as e:
        print(f"   ⚠️  Erreur lors du test des classes: {e}")
    
    # 4. Test d'une requête de destination
    print(f"\n4️⃣ Test d'une requête réelle (destinations)...")
    try:
        destination_query = f"""
        PREFIX eco: <{ONTOLOGY_NS}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?destination ?nom ?description
        WHERE {{
            ?destination a eco:Destination .
            OPTIONAL {{ ?destination rdfs:label ?nom }}
            OPTIONAL {{ ?destination rdfs:comment ?description }}
        }}
        LIMIT 5
        """
        
        response = requests.post(
            FUSEKI_ENDPOINT,
            data=destination_query,
            headers={
                "Accept": "application/sparql-results+json",
                "Content-Type": "application/sparql-query"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            bindings = results.get("results", {}).get("bindings", [])
            print(f"   ✅ Trouvé {len(bindings)} destination(s)")
            
            if bindings:
                print(f"\n   Destinations trouvées:")
                for binding in bindings:
                    nom = binding.get("nom", {}).get("value", "Sans nom")
                    print(f"      • {nom}")
            else:
                print(f"\n   ⚠️  Aucune destination trouvée")
                print(f"   💡 Vérifiez que votre fichier RDF contient des instances de la classe Destination")
        else:
            print(f"   ❌ Erreur requête destinations (statut {response.status_code})")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        test_fuseki_connection()
    except KeyboardInterrupt:
        print("\n\n❌ Diagnostic interrompu par l'utilisateur")
        sys.exit(1)
