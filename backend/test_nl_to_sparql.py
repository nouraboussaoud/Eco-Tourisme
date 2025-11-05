import sys
from services.nl_to_sparql import NLToSparqlConverter
from services.mock_fuseki_client import MockFusekiClient

def test_nl_conversion():
    """Test le convertisseur NL vers SPARQL"""
    
    converter = NLToSparqlConverter()
    mock_client = MockFusekiClient()
    
    # Questions de test pour le tourisme éco-responsable
    test_questions = [
        "Trouve toutes les destinations avec une faible empreinte carbone",
        "Quels sont les hébergements écologiques disponibles?",
        "Liste les activités de randonnée",
        "Montre-moi les destinations certifiées éco-tourisme",
        "Quels sont les voyageurs intéressés par le bien-être?",
        "Trouve les destinations en Tunisie",
        "Quelles sont les activités avec moins de 50kg CO2?",
        "Liste tous les hébergements avec certification Green Globe",
        "Quelles destinations sont durables?",
        "Où puis-je faire du tourisme écologique?"
    ]
    
    print("=" * 80)
    print("TEST: Conversion Langage Naturel → SPARQL")
    print("=" * 80)
    print(f"\n🧪 Nombre de tests: {len(test_questions)}\n")
    
    success_count = 0
    error_count = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 80}")
        print(f"Test #{i}")
        print(f"{'=' * 80}")
        print(f"❓ Question: {question}")
        print(f"{'-' * 80}")
        
        try:
            # Convertir la question en SPARQL
            sparql_query = converter.convert_question_to_sparql(question)
            print(f"✅ SPARQL généré:\n")
            print(sparql_query)
            
            # Tester l'exécution avec le mock client
            print(f"\n{'-' * 80}")
            print("🔍 Test d'exécution avec Mock Fuseki Client:")
            try:
                results = mock_client.query(sparql_query)
                parsed_results = mock_client.parse_results(results)
                print(f"✅ Résultats: {len(parsed_results)} lignes trouvées")
                
                # Afficher les 3 premiers résultats
                if parsed_results:
                    print("\n📊 Aperçu des résultats (3 premiers):")
                    for j, row in enumerate(parsed_results[:3], 1):
                        print(f"  {j}. {row}")
                
                success_count += 1
            except Exception as exec_error:
                print(f"⚠️  Erreur d'exécution: {str(exec_error)}")
                error_count += 1
            
        except Exception as e:
            print(f"❌ Erreur de conversion: {str(e)}")
            error_count += 1
    
    print(f"\n{'=' * 80}")
    print(f"📈 RÉSUMÉ DES TESTS")
    print(f"{'=' * 80}")
    print(f"✅ Succès: {success_count}/{len(test_questions)}")
    print(f"❌ Erreurs: {error_count}/{len(test_questions)}")
    print(f"📊 Taux de réussite: {(success_count/len(test_questions)*100):.1f}%")
    print(f"{'=' * 80}\n")

if __name__ == "__main__":
    test_nl_conversion()
