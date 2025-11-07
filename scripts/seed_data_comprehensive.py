"""
Comprehensive Seed Data Script for Eco-Tourism Ontology
Creates rich sample data with destinations, accommodations, activities, and certifications
"""

import requests
import sys
from datetime import datetime

# Configuration
FUSEKI_URL = "http://localhost:3030"
DATASET_NAME = "tourisme-eco-2"
SPARQL_UPDATE_ENDPOINT = f"{FUSEKI_URL}/{DATASET_NAME}/update"
SPARQL_QUERY_ENDPOINT = f"{FUSEKI_URL}/{DATASET_NAME}/query"

# Namespace
BASE_URI = "http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#"

def clear_dataset():
    """Clear all existing data in the dataset"""
    print("🗑️  Clearing existing data...")
    delete_query = """
    DELETE WHERE {
        ?s ?p ?o .
    }
    """
    
    try:
        response = requests.post(
            SPARQL_UPDATE_ENDPOINT,
            data={'update': delete_query},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if response.status_code == 200 or response.status_code == 204:
            print("✅ Dataset cleared successfully")
            return True
        else:
            print(f"⚠️  Warning: Clear returned status {response.status_code}")
            return True
    except Exception as e:
        print(f"❌ Error clearing dataset: {e}")
        return False

def insert_data(sparql_insert):
    """Insert data using SPARQL INSERT"""
    try:
        response = requests.post(
            SPARQL_UPDATE_ENDPOINT,
            data={'update': sparql_insert},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code == 200 or response.status_code == 204:
            return True
        else:
            print(f"❌ Insert failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False

def seed_certifications():
    """Seed eco certifications"""
    print("\n🏆 Seeding Certifications...")
    
    certifications = """
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

INSERT DATA {
    # Green Key Certification
    eco:cert_green_key rdf:type eco:LabelInternational ;
        rdfs:label "Green Key" ;
        rdfs:comment "Label international pour l'environnement décerné aux hébergements touristiques respectueux de l'environnement" ;
        eco:organismeEmetteur "Foundation for Environmental Education" ;
        eco:scoreDurabilite 95 .
    
    # EcoLabel Certification
    eco:cert_ecolabel rdf:type eco:LabelInternational ;
        rdfs:label "EU Ecolabel" ;
        rdfs:comment "Label écologique européen garantissant des pratiques durables" ;
        eco:organismeEmetteur "Commission Européenne" ;
        eco:scoreDurabilite 90 .
    
    # Clef Verte
    eco:cert_clef_verte rdf:type eco:LabelNational ;
        rdfs:label "Clef Verte Tunisie" ;
        rdfs:comment "Premier label de tourisme durable en Tunisie" ;
        eco:organismeEmetteur "Fondation Mohammed VI" ;
        eco:scoreDurabilite 85 .
    
    # Green Globe
    eco:cert_green_globe rdf:type eco:GreenGlobe ;
        rdfs:label "Green Globe Certification" ;
        rdfs:comment "Certification mondiale pour le tourisme durable" ;
        eco:organismeEmetteur "Green Globe International" ;
        eco:scoreDurabilite 92 .
    
    # Eco Tourism Tunisia
    eco:cert_eco_tunisia rdf:type eco:EcoTourism ;
        rdfs:label "Eco Tourism Tunisia" ;
        rdfs:comment "Label national tunisien pour le tourisme écologique" ;
        eco:organismeEmetteur "Office National du Tourisme Tunisien" ;
        eco:scoreDurabilite 80 .
}
"""
    
    if insert_data(certifications):
        print("✅ Certifications seeded successfully")
    else:
        print("❌ Failed to seed certifications")

def seed_destinations():
    """Seed tourist destinations"""
    print("\n🗺️  Seeding Destinations...")
    
    destinations = """
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

INSERT DATA {
    # Parc National Ichkeul
    eco:dest_ichkeul rdf:type eco:Montagne ;
        rdfs:label "Parc National Ichkeul" ;
        rdfs:comment "Réserve naturelle classée UNESCO, sanctuaire pour oiseaux migrateurs et faune sauvage" ;
        eco:localiseDans "Bizerte" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 98 ;
        eco:aCertification eco:cert_green_key .
    
    # Djerba Island
    eco:dest_djerba rdf:type eco:Plage ;
        rdfs:label "Île de Djerba" ;
        rdfs:comment "Île paradisiaque méditerranéenne avec plages préservées et patrimoine culturel riche" ;
        eco:localiseDans "Medenine" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 88 ;
        eco:aCertification eco:cert_clef_verte .
    
    # Sidi Bou Said
    eco:dest_sidi_bou_said rdf:type eco:PatrimoineCulturel ;
        rdfs:label "Sidi Bou Saïd" ;
        rdfs:comment "Village pittoresque aux maisons bleues et blanches, symbole du patrimoine tunisien" ;
        eco:localiseDans "Tunis" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 85 .
    
    # Chott El Jerid
    eco:dest_chott_jerid rdf:type eco:Destination ;
        rdfs:label "Chott El Jérid" ;
        rdfs:comment "Lac salé spectaculaire dans le désert, paysages lunaires uniques" ;
        eco:localiseDans "Tozeur" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 92 .
    
    # Ksar Ghilane
    eco:dest_ksar_ghilane rdf:type eco:Destination ;
        rdfs:label "Ksar Ghilane" ;
        rdfs:comment "Oasis au milieu du désert du Sahara avec sources chaudes naturelles" ;
        eco:localiseDans "Tataouine" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 90 .
    
    # Carthage
    eco:dest_carthage rdf:type eco:PatrimoineCulturel ;
        rdfs:label "Site Archéologique de Carthage" ;
        rdfs:comment "Ancienne cité punique et romaine, site UNESCO majeur" ;
        eco:localiseDans "Tunis" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 87 .
    
    # Douz
    eco:dest_douz rdf:type eco:Destination ;
        rdfs:label "Douz - Porte du Sahara" ;
        rdfs:comment "Gateway du désert avec culture bédouine authentique" ;
        eco:localiseDans "Kébili" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 89 .
    
    # Tabarka
    eco:dest_tabarka rdf:type eco:Montagne ;
        rdfs:label "Tabarka" ;
        rdfs:comment "Station balnéaire avec forêts de chênes-lièges et récifs coralliens" ;
        eco:localiseDans "Jendouba" ;
        eco:pays "Tunisie" ;
        eco:scoreDurabilite 91 ;
        eco:aCertification eco:cert_ecolabel .
}
"""
    
    if insert_data(destinations):
        print("✅ Destinations seeded successfully")
    else:
        print("❌ Failed to seed destinations")

def seed_accommodations():
    """Seed eco-friendly accommodations"""
    print("\n🏨 Seeding Accommodations...")
    
    accommodations = """
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

INSERT DATA {
    # Eco-Lodge Dar Bhar
    eco:heb_dar_bhar rdf:type eco:HotelEcologique ;
        rdfs:label "Eco-Lodge Dar Bhar" ;
        rdfs:comment "Hébergement écologique luxueux avec vue sur mer, panneaux solaires et gestion durable de l'eau" ;
        eco:localiseDans "Djerba" ;
        eco:prixNuit 120 ;
        eco:capacite 8 ;
        eco:scoreDurabilite 95 ;
        eco:aCertification eco:cert_green_key .
    
    # Gîte Rural Toujane
    eco:heb_toujane rdf:type eco:GiteRural ;
        rdfs:label "Gîte Rural de Toujane" ;
        rdfs:comment "Gîte berbère traditionnel dans les montagnes avec architecture écologique" ;
        eco:localiseDans "Matmata" ;
        eco:prixNuit 45 ;
        eco:capacite 6 ;
        eco:scoreDurabilite 92 ;
        eco:aCertification eco:cert_clef_verte .
    
    # Camping Eco-Responsable Ichkeul
    eco:heb_camping_ichkeul rdf:type eco:CampingEcoResponsable ;
        rdfs:label "Camping Ichkeul Nature" ;
        rdfs:comment "Camping écologique au cœur du parc national avec toilettes sèches et énergie solaire" ;
        eco:localiseDans "Bizerte" ;
        eco:prixNuit 25 ;
        eco:capacite 4 ;
        eco:scoreDurabilite 88 ;
        eco:aCertification eco:cert_eco_tunisia .
    
    # Auberge Dar Zaghouan
    eco:heb_zaghouan rdf:type eco:Auberge ;
        rdfs:label "Auberge Dar Zaghouan" ;
        rdfs:comment "Auberge familiale avec cuisine bio locale et pratiques zéro déchet" ;
        eco:localiseDans "Zaghouan" ;
        eco:prixNuit 35 ;
        eco:capacite 12 ;
        eco:scoreDurabilite 85 .
    
    # Hotel Eco-Sidi Bou
    eco:heb_sidi_bou rdf:type eco:HotelEcologique ;
        rdfs:label "Hôtel Dar El Jeld" ;
        rdfs:comment "Hôtel boutique dans palais restauré, récupération eau de pluie et matériaux locaux" ;
        eco:localiseDans "Sidi Bou Saïd" ;
        eco:prixNuit 95 ;
        eco:capacite 5 ;
        eco:scoreDurabilite 90 ;
        eco:aCertification eco:cert_ecolabel .
    
    # Ksar Ghilane Camp
    eco:heb_ksar_camp rdf:type eco:CampingEcoResponsable ;
        rdfs:label "Ksar Ghilane Eco-Camp" ;
        rdfs:comment "Camp désertique authentique avec tentes traditionnelles et respect de l'environnement" ;
        eco:localiseDans "Ksar Ghilane" ;
        eco:prixNuit 60 ;
        eco:capacite 3 ;
        eco:scoreDurabilite 86 .
    
    # Dar Tabarka
    eco:heb_tabarka rdf:type eco:GiteRural ;
        rdfs:label "Maison d'Hôtes Coral" ;
        rdfs:comment "Maison d'hôtes éco-responsable près des récifs coralliens" ;
        eco:localiseDans "Tabarka" ;
        eco:prixNuit 75 ;
        eco:capacite 10 ;
        eco:scoreDurabilite 87 ;
        eco:aCertification eco:cert_green_globe .
}
"""
    
    if insert_data(accommodations):
        print("✅ Accommodations seeded successfully")
    else:
        print("❌ Failed to seed accommodations")

def seed_activities():
    """Seed tourist activities"""
    print("\n🥾 Seeding Activities...")
    
    activities = """
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

INSERT DATA {
    # Randonnée Ichkeul
    eco:act_rando_ichkeul rdf:type eco:Randonnee ;
        rdfs:label "Randonnée Guidée Parc Ichkeul" ;
        rdfs:comment "Découverte de la faune et flore du parc national avec guide naturaliste certifié" ;
        eco:duree "4 heures" ;
        eco:cout 25 ;
        eco:scoreDurabilite 98 ;
        eco:localiseDans "Ichkeul" .
    
    # Plongée Tabarka
    eco:act_plongee_tabarka rdf:type eco:Plongee ;
        rdfs:label "Plongée Récifs Coralliens Tabarka" ;
        rdfs:comment "Exploration des récifs coralliens avec respect des écosystèmes marins" ;
        eco:duree "3 heures" ;
        eco:cout 45 ;
        eco:scoreDurabilite 92 ;
        eco:localiseDans "Tabarka" .
    
    # Visite Historique Carthage
    eco:act_visite_carthage rdf:type eco:VisiteHistorique ;
        rdfs:label "Circuit Archéologique Carthage" ;
        rdfs:comment "Visite guidée des sites puniques et romains avec archéologue professionnel" ;
        eco:duree "5 heures" ;
        eco:cout 35 ;
        eco:scoreDurabilite 85 ;
        eco:localiseDans "Carthage" .
    
    # Atelier Poterie
    eco:act_poterie_djerba rdf:type eco:ActiviteEducative ;
        rdfs:label "Atelier Poterie Traditionnelle" ;
        rdfs:comment "Apprentissage de la poterie berbère avec artisans locaux à Djerba" ;
        eco:duree "2 heures" ;
        eco:cout 20 ;
        eco:scoreDurabilite 90 ;
        eco:localiseDans "Djerba" .
    
    # Cuisine Bio
    eco:act_cuisine_bio rdf:type eco:Atelier_culinaire ;
        rdfs:label "Cours de Cuisine Méditerranéenne Bio" ;
        rdfs:comment "Atelier culinaire avec produits bio locaux et recettes traditionnelles" ;
        eco:duree "3 heures" ;
        eco:cout 30 ;
        eco:scoreDurabilite 94 ;
        eco:localiseDans "Sidi Bou Saïd" .
    
    # Meditation Desert
    eco:act_meditation_desert rdf:type eco:Meditation ;
        rdfs:label "Séance Méditation Désert" ;
        rdfs:comment "Méditation au lever du soleil dans le Sahara avec instructeur certifié" ;
        eco:duree "2 heures" ;
        eco:cout 15 ;
        eco:scoreDurabilite 96 ;
        eco:localiseDans "Ksar Ghilane" .
    
    # Spa Naturel
    eco:act_spa_ksar rdf:type eco:Spa ;
        rdfs:label "Bain Thermal Naturel" ;
        rdfs:comment "Relaxation dans les sources chaudes naturelles du désert" ;
        eco:duree "1.5 heures" ;
        eco:cout 18 ;
        eco:scoreDurabilite 88 ;
        eco:localiseDans "Ksar Ghilane" .
    
    # Randonnée Chamelière
    eco:act_trek_chameau rdf:type eco:Randonnee ;
        rdfs:label "Trek à Dos de Chameau" ;
        rdfs:comment "Randonnée chamelière traditionnelle dans le désert avec guide bédouin" ;
        eco:duree "6 heures" ;
        eco:cout 50 ;
        eco:scoreDurabilite 93 ;
        eco:localiseDans "Douz" .
    
    # Visite Musée Bardo
    eco:act_musee_bardo rdf:type eco:Musee ;
        rdfs:label "Visite Musée du Bardo" ;
        rdfs:comment "Découverte de la plus grande collection de mosaïques romaines au monde" ;
        eco:duree "2.5 heures" ;
        eco:cout 12 ;
        eco:scoreDurabilite 82 ;
        eco:localiseDans "Tunis" .
    
    # Randonnée Montagnes
    eco:act_rando_montagne rdf:type eco:Randonnee ;
        rdfs:label "Trekking Djebel Zaghouan" ;
        rdfs:comment "Randonnée en montagne avec vues panoramiques et découverte flore locale" ;
        eco:duree "5 heures" ;
        eco:cout 28 ;
        eco:scoreDurabilite 95 ;
        eco:localiseDans "Zaghouan" .
    
    # Observation Oiseaux
    eco:act_bird_watching rdf:type eco:ActiviteSportive ;
        rdfs:label "Observation Oiseaux Migrateurs" ;
        rdfs:comment "Session d'observation ornithologique au lac Ichkeul avec expert" ;
        eco:duree "3 heures" ;
        eco:cout 22 ;
        eco:scoreDurabilite 97 ;
        eco:localiseDans "Ichkeul" .
    
    # Balade Vélo
    eco:act_velo_djerba rdf:type eco:ActiviteSportive ;
        rdfs:label "Circuit Vélo Électrique Djerba" ;
        rdfs:comment "Tour guidé en vélo électrique autour de l'île avec arrêts patrimoniaux" ;
        eco:duree "4 heures" ;
        eco:cout 32 ;
        eco:scoreDurabilite 91 ;
        eco:localiseDans "Djerba" .
}
"""
    
    if insert_data(activities):
        print("✅ Activities seeded successfully")
    else:
        print("❌ Failed to seed activities")

def verify_data():
    """Verify that data was inserted correctly"""
    print("\n🔍 Verifying inserted data...")
    
    count_query = """
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT 
    (COUNT(?dest) as ?destinations)
    (COUNT(?heb) as ?hebergements)
    (COUNT(?act) as ?activites)
    (COUNT(?cert) as ?certifications)
WHERE {
    OPTIONAL { ?dest rdf:type/rdfs:subClassOf* eco:Destination }
    OPTIONAL { ?heb rdf:type/rdfs:subClassOf* eco:Hebergement }
    OPTIONAL { ?act rdf:type/rdfs:subClassOf* eco:ActiviteTouristique }
    OPTIONAL { ?cert rdf:type/rdfs:subClassOf* eco:CertificatEco }
}
"""
    
    try:
        response = requests.post(
            SPARQL_QUERY_ENDPOINT,
            data={'query': count_query},
            headers={'Accept': 'application/sparql-results+json'}
        )
        
        if response.status_code == 200:
            results = response.json()
            if 'results' in results and 'bindings' in results['results']:
                bindings = results['results']['bindings'][0]
                print(f"  📍 Destinations: {bindings.get('destinations', {}).get('value', 0)}")
                print(f"  🏨 Hébergements: {bindings.get('hebergements', {}).get('value', 0)}")
                print(f"  🎯 Activités: {bindings.get('activites', {}).get('value', 0)}")
                print(f"  🏆 Certifications: {bindings.get('certifications', {}).get('value', 0)}")
                return True
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
    
    return False

def main():
    print("\n" + "="*60)
    print("  🌍 ECO-TOURISM DATA SEEDING SCRIPT")
    print("="*60)
    print(f"\n📡 Fuseki Endpoint: {FUSEKI_URL}")
    print(f"📦 Dataset: {DATASET_NAME}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if Fuseki is running
    try:
        response = requests.get(f"{FUSEKI_URL}/$/ping")
        if response.status_code != 200:
            print("\n❌ Error: Fuseki server is not responding!")
            print("   Please start Fuseki first with: fuseki-server.bat --update --mem /tourisme-eco-2")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: Cannot connect to Fuseki at {FUSEKI_URL}")
        print(f"   {e}")
        print("\n   Please start Fuseki first with: fuseki-server.bat --update --mem /tourisme-eco-2")
        sys.exit(1)
    
    print("\n✅ Fuseki server is running")
    
    # Clear existing data
    if not clear_dataset():
        print("\n⚠️  Warning: Could not clear existing data, continuing anyway...")
    
    # Seed all data
    seed_certifications()
    seed_destinations()
    seed_accommodations()
    seed_activities()
    
    # Verify
    verify_data()
    
    print("\n" + "="*60)
    print("  ✅ DATA SEEDING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📊 You can now query the data at:")
    print(f"   {FUSEKI_URL}/{DATASET_NAME}/sparql")
    print("\n🔗 Or use the web interface at:")
    print(f"   {FUSEKI_URL}")
    print("\n")

if __name__ == "__main__":
    main()
