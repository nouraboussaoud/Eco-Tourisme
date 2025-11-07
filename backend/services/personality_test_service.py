# Service de Test de Personnalité et Génération de Packages de Voyage
from typing import List, Dict, Any, Optional
import json
import os
import google.generativeai as genai

class PersonalityTestService:
    """Service pour gérer les tests de personnalité et générer des recommandations via OpenAI"""
    
    # Questions du test de personnalité (5-7 questions)
    PERSONALITY_QUESTIONS = [
        {
            "id": 1,
            "question": "Quel type d'activité vous attire le plus pendant vos vacances ?",
            "options": [
                {"value": "adventure", "label": "Sports extrêmes et randonnées aventureuses"},
                {"value": "culture", "label": "Visites de musées et sites historiques"},
                {"value": "relaxation", "label": "Spa, méditation et détente"},
                {"value": "nature", "label": "Observation de la faune et promenades en nature"}
            ]
        },
        {
            "id": 2,
            "question": "Quel est votre niveau de préoccupation environnementale ?",
            "options": [
                {"value": "very_high", "label": "Très élevé - Je choisis toujours l'option la plus écologique"},
                {"value": "high", "label": "Élevé - L'environnement est important pour moi"},
                {"value": "moderate", "label": "Modéré - J'essaie de faire attention quand c'est possible"},
                {"value": "low", "label": "Faible - Ce n'est pas ma priorité principale"}
            ]
        },
        {
            "id": 3,
            "question": "Quel type d'hébergement préférez-vous ?",
            "options": [
                {"value": "eco_lodge", "label": "Éco-lodge ou hébergement durable"},
                {"value": "local_guesthouse", "label": "Maison d'hôtes locale ou chambre chez l'habitant"},
                {"value": "hotel", "label": "Hôtel confortable avec certifications vertes"},
                {"value": "camping", "label": "Camping ou glamping en pleine nature"}
            ]
        },
        {
            "id": 4,
            "question": "Quelle durée de séjour préférez-vous ?",
            "options": [
                {"value": "short", "label": "Court séjour (2-3 jours)"},
                {"value": "medium", "label": "Séjour moyen (4-7 jours)"},
                {"value": "long", "label": "Long séjour (8+ jours)"},
                {"value": "flexible", "label": "Flexible selon les opportunités"}
            ]
        },
        {
            "id": 5,
            "question": "Quel budget envisagez-vous pour votre voyage ?",
            "options": [
                {"value": "budget", "label": "Économique (moins de 500€)"},
                {"value": "moderate", "label": "Modéré (500-1500€)"},
                {"value": "comfortable", "label": "Confortable (1500-3000€)"},
                {"value": "luxury", "label": "Luxueux (3000€+)"}
            ]
        },
        {
            "id": 6,
            "question": "Comment préférez-vous vous déplacer en voyage ?",
            "options": [
                {"value": "train", "label": "Train - écologique et confortable"},
                {"value": "bike", "label": "Vélo - actif et sans émissions"},
                {"value": "car", "label": "Voiture électrique/partagée"},
                {"value": "mixed", "label": "Combinaison de moyens de transport"}
            ]
        },
        {
            "id": 7,
            "question": "Qu'est-ce qui est le plus important pour vous dans un voyage ?",
            "options": [
                {"value": "authentic", "label": "Authenticité et contact avec les locaux"},
                {"value": "comfort", "label": "Confort et services de qualité"},
                {"value": "adventure", "label": "Aventure et nouvelles expériences"},
                {"value": "learning", "label": "Apprendre et découvrir de nouvelles cultures"}
            ]
        }
    ]
    
    def __init__(self, fuseki_client=None):
        self.fuseki = fuseki_client
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini API configured successfully")
        else:
            self.model = None
            print("⚠️  Gemini API Key not found. Using fallback recommendations.")
    
    def get_questions(self) -> List[Dict[str, Any]]:
        """Retourne les questions du test de personnalité"""
        return self.PERSONALITY_QUESTIONS
    
    def analyze_personality_with_ai(self, answers: Dict[str, str], available_destinations: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyse les réponses du test avec Gemini AI"""
        if not self.model:
            return self._fallback_personality_analysis(answers)
        
        try:
            # Construire le prompt pour Gemini avec les vraies destinations
            prompt = self._build_personality_prompt(answers, available_destinations)
            
            # Appeler Gemini
            response = self.model.generate_content(prompt)
            ai_response = response.text
            
            # Parser la réponse de Gemini
            return self._parse_ai_response(ai_response, answers)
            
        except Exception as e:
            print(f"Erreur Gemini AI: {e}")
            return self._fallback_personality_analysis(answers)
    
    def _build_personality_prompt(self, answers: Dict[str, str], available_destinations: List[Dict[str, Any]] = None) -> str:
        """Construit le prompt pour Gemini AI basé sur les réponses"""
        prompt = """Tu es un expert en tourisme éco-responsable. Analyse ce profil de voyageur basé sur un test de personnalité:

Réponses du test:
"""
        for q_id, answer_value in answers.items():
            question = next((q for q in self.PERSONALITY_QUESTIONS if str(q['id']) == str(q_id)), None)
            if question:
                option = next((opt for opt in question['options'] if opt['value'] == answer_value), None)
                if option:
                    prompt += f"\n- {question['question']}: {option['label']}"
        
        # Ajouter les destinations disponibles
        if available_destinations and len(available_destinations) > 0:
            prompt += "\n\nDestinations éco-responsables disponibles dans notre système:\n"
            for dest in available_destinations[:20]:  # Limiter à 20 pour ne pas surcharger le prompt
                dest_name = dest.get('nom', 'Inconnu')
                dest_type = dest.get('type', '')
                dest_score = dest.get('scoreDurabilite', 'N/A')
                dest_cert = dest.get('certifications', '')
                
                prompt += f"- {dest_name}"
                if dest_type:
                    prompt += f" ({dest_type})"
                if dest_score and dest_score != 'N/A':
                    prompt += f" - Score durabilité: {dest_score}/100"
                if dest_cert:
                    prompt += f" - Certifications: {dest_cert}"
                prompt += "\n"
        
        prompt += """

Réponds UNIQUEMENT avec un objet JSON valide (sans markdown, sans ```json) avec cette structure exacte:
{
  "personality_type": "Un type parmi: Aventurier Écologique, Explorateur Culturel, Voyageur Zen, Famille Nature",
  "profile_description": "Description détaillée du profil (2-3 phrases)",
  "preferences": {
    "activity_level": "low/medium/high",
    "eco_priority": "low/medium/high/very_high",
    "accommodation_style": "description",
    "transport_preference": "description"
  },
  "recommended_destinations": ["destination1 depuis la liste ci-dessus", "destination2", "destination3"],
  "recommended_activities": ["activité1", "activité2", "activité3", "activité4"],
  "eco_score": 85,
  "trip_duration_days": 5
}

IMPORTANT: Les recommended_destinations DOIVENT être choisis UNIQUEMENT parmi les destinations listées ci-dessus.
Réponds uniquement avec le JSON, sans texte avant ou après.
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str, answers: Dict[str, str]) -> Dict[str, Any]:
        """Parse la réponse JSON de Gemini AI"""
        try:
            # Nettoyer la réponse (enlever les markdown code blocks si présents)
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Extraire le JSON de la réponse
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                parsed = json.loads(json_text)
                parsed['raw_answers'] = answers
                return parsed
            else:
                return self._fallback_personality_analysis(answers)
        except json.JSONDecodeError as e:
            print(f"Erreur parsing JSON Gemini: {e}")
            print(f"Réponse reçue: {response_text[:200]}...")
            return self._fallback_personality_analysis(answers)
    
    def _fallback_personality_analysis(self, answers: Dict[str, str]) -> Dict[str, Any]:
        """Analyse de repli si OpenAI n'est pas disponible"""
        # Analyser les réponses pour déterminer le profil
        activity_pref = answers.get('1', 'nature')
        eco_concern = answers.get('2', 'moderate')
        accommodation = answers.get('3', 'hotel')
        duration = answers.get('4', 'medium')
        budget = answers.get('5', 'moderate')
        transport = answers.get('6', 'mixed')
        priority = answers.get('7', 'learning')
        
        # Déterminer le type de personnalité
        if activity_pref == 'adventure' and eco_concern in ['high', 'very_high']:
            personality_type = "Aventurier Écologique"
            profile_desc = "Vous aimez l'aventure tout en respectant l'environnement. Vous recherchez des expériences actives dans la nature avec un impact minimal."
            activities = ["Randonnée", "Escalade", "VTT", "Kayak écologique"]
        elif activity_pref == 'culture' and priority == 'learning':
            personality_type = "Explorateur Culturel"
            profile_desc = "Vous êtes passionné par la découverte de nouvelles cultures et l'apprentissage. Vous privilégiez l'authenticité et les rencontres locales."
            activities = ["Visite guidée", "Musée", "Atelier culinaire", "Visite historique"]
        elif activity_pref == 'relaxation':
            personality_type = "Voyageur Zen"
            profile_desc = "Vous recherchez la détente et le bien-être. Vos vacances sont un moment de ressourcement dans un environnement paisible."
            activities = ["Yoga", "Spa", "Méditation", "Promenade nature"]
        else:
            personality_type = "Nature Conscient"
            profile_desc = "Vous appréciez la nature et cherchez un équilibre entre découverte et respect de l'environnement."
            activities = ["Observation faune", "Randonnée douce", "Visite éco-ferme", "Atelier environnement"]
        
        # Mapper le budget
        budget_map = {
            'budget': 500,
            'moderate': 1200,
            'comfortable': 2500,
            'luxury': 4000
        }
        
        # Mapper la durée
        duration_map = {
            'short': 3,
            'medium': 5,
            'long': 10,
            'flexible': 5
        }
        
        # Mapper l'eco score
        eco_score_map = {
            'very_high': 95,
            'high': 80,
            'moderate': 65,
            'low': 50
        }
        
        return {
            "personality_type": personality_type,
            "profile_description": profile_desc,
            "preferences": {
                "activity_level": "high" if activity_pref == 'adventure' else "medium" if activity_pref in ['culture', 'nature'] else "low",
                "eco_priority": eco_concern,
                "accommodation_style": accommodation,
                "transport_preference": transport,
                "budget_range": budget_map.get(budget, 1200),
                "duration_days": duration_map.get(duration, 5)
            },
            "recommended_activities": activities,
            "eco_score": eco_score_map.get(eco_concern, 65),
            "trip_duration_days": duration_map.get(duration, 5),
            "raw_answers": answers
        }
    
    def generate_trip_package(
        self, 
        personality_profile: Dict[str, Any],
        available_places: List[Dict[str, Any]],
        available_accommodations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Génère un package de voyage complet basé sur le profil et les données SPARQL"""
        
        # PRIORITÉ 1: DESTINATIONS - OBLIGATOIRES (NO MOCK DATA ALLOWED)
        if not available_places or len(available_places) == 0:
            raise ValueError("❌ Aucune destination disponible dans Fuseki. Veuillez ajouter des destinations à la base de données.")
        
        preferences = personality_profile.get('preferences', {})
        eco_priority = preferences.get('eco_priority', 'moderate')
        duration = preferences.get('duration_days', 5)
        budget = preferences.get('budget_range', 1200)
        
        # Filtrer et scorer les lieux selon les certifications écologiques
        scored_places = self._score_places_by_certification(available_places, eco_priority)
        
        # Sélectionner les meilleurs lieux (TOUJOURS au moins duration lieux)
        num_places = min(duration + 2, len(scored_places))
        if num_places < duration:
            num_places = min(duration, len(scored_places))
        selected_places = scored_places[:max(num_places, 3)]  # Au moins 3 places
        
        # Vérifier qu'on a bien des destinations
        if not selected_places:
            raise ValueError("❌ Aucune destination correspondante trouvée dans Fuseki.")
        
        print(f"✅ {len(selected_places)} destinations sélectionnées pour le package (source: Fuseki)")
        
        # PRIORITÉ 2: HÉBERGEMENTS - OPTIONNELS (peuvent être vides)
        if not available_accommodations or len(available_accommodations) == 0:
            print("ℹ️  Aucun hébergement trouvé - Le package sera basé uniquement sur les destinations")
            available_accommodations = []
        
        # Filtrer les hébergements selon budget et certification (ONLY IF ANY AVAILABLE)
        if available_accommodations and len(available_accommodations) > 0:
            suitable_accommodations = self._filter_accommodations(
                available_accommodations, 
                budget, 
                eco_priority
            )
            
            # Si pas d'hébergements appropriés après filtrage, prendre les meilleurs disponibles
            if not suitable_accommodations:
                print("ℹ️  Aucun hébergement après filtrage budget/eco - utilisation des meilleurs disponibles")
                suitable_accommodations = available_accommodations[:3]
            
            print(f"✅ {len(suitable_accommodations)} hébergements sélectionnés pour le package")
        else:
            suitable_accommodations = []
            print("ℹ️  0 hébergements - package basé uniquement sur les destinations")
        
        # Générer l'itinéraire jour par jour BASÉ SUR LES DESTINATIONS
        itinerary = self._generate_itinerary(selected_places, duration)
        
        # Calculer les coûts
        costs = self._calculate_package_costs(
            selected_places, 
            suitable_accommodations[:1] if suitable_accommodations else [], 
            duration,
            preferences.get('transport_preference', 'mixed')
        )
        
        return {
            "package_name": f"Package {personality_profile['personality_type']}",
            "personality_type": personality_profile['personality_type'],
            "description": personality_profile['profile_description'],
            "duration_days": duration,
            "total_budget": costs['total'],
            "breakdown": costs,
            "eco_score": personality_profile['eco_score'],
            "itinerary": itinerary,
            "places": selected_places,  # TOUJOURS présent avec vraies données Fuseki
            "accommodations": suitable_accommodations[:2] if suitable_accommodations else [],  # Optionnel
            "transport_recommendations": self._get_transport_recommendations(
                preferences.get('transport_preference', 'mixed'),
                eco_priority
            ),
            "sustainability_highlights": self._get_sustainability_highlights(selected_places, suitable_accommodations[:2] if suitable_accommodations else [])
        }
    
    def _score_places_by_certification(
        self, 
        places: List[Dict[str, Any]], 
        eco_priority: str
    ) -> List[Dict[str, Any]]:
        """Score les lieux selon leurs certifications écologiques"""
        
        # Définir les poids selon la priorité écologique
        weights = {
            'very_high': {'certification': 0.6, 'rating': 0.2, 'activities': 0.2},
            'high': {'certification': 0.5, 'rating': 0.3, 'activities': 0.2},
            'moderate': {'certification': 0.3, 'rating': 0.4, 'activities': 0.3},
            'low': {'certification': 0.2, 'rating': 0.5, 'activities': 0.3}
        }
        
        weight = weights.get(eco_priority, weights['moderate'])
        
        scored = []
        for place in places:
            score = 0
            
            # Score de certification
            cert_score = 0
            certifications = place.get('certifications', place.get('certification', ''))
            if isinstance(certifications, str):
                if any(cert in certifications for cert in ['ISO', 'Green', 'Eco', 'Bio']):
                    cert_score = 90
                elif certifications:
                    cert_score = 70
            
            # Score de durabilité
            sustainability = float(place.get('scoreDurabilite', place.get('scoreDurabilité', 50)))
            
            # Score final
            score = (cert_score * weight['certification'] + 
                    sustainability * weight['rating'] + 
                    50 * weight['activities'])  # Base activity score
            
            place['eco_match_score'] = round(score, 2)
            scored.append(place)
        
        # Trier par score
        scored.sort(key=lambda x: x.get('eco_match_score', 0), reverse=True)
        return scored
    
    def _filter_accommodations(
        self, 
        accommodations: List[Dict[str, Any]], 
        budget: float,
        eco_priority: str
    ) -> List[Dict[str, Any]]:
        """Filtre les hébergements selon budget et priorité écologique"""
        
        min_eco_score = {
            'very_high': 85,
            'high': 70,
            'moderate': 60,
            'low': 50
        }.get(eco_priority, 60)
        
        # Estimer le coût par nuit (à ajuster selon vos données)
        daily_budget = budget / 5  # Budget approximatif par jour
        max_accommodation_cost = daily_budget * 0.4  # 40% du budget journalier
        
        suitable = []
        for acc in accommodations:
            eco_score = float(acc.get('scoreDurabilite', acc.get('scoreDurabilité', 50)))
            # Prix estimé (à adapter selon vos données)
            est_price = float(acc.get('price', acc.get('prix', 80)))
            
            if eco_score >= min_eco_score and est_price <= max_accommodation_cost:
                suitable.append(acc)
        
        # Trier par score écologique
        suitable.sort(key=lambda x: float(x.get('scoreDurabilite', x.get('scoreDurabilité', 50))), reverse=True)
        return suitable
    
    def _generate_itinerary(self, places: List[Dict[str, Any]], duration: int) -> List[Dict[str, Any]]:
        """Génère un itinéraire jour par jour"""
        itinerary = []
        
        for day in range(1, min(duration + 1, len(places) + 1)):
            if day - 1 < len(places):
                place = places[day - 1]
                itinerary.append({
                    "day": day,
                    "title": f"Jour {day}: {place.get('nom', 'Activité')}",
                    "place": place.get('nom', 'Lieu'),
                    "activities": place.get('activities', [place.get('type', 'Visite')]),
                    "description": place.get('description', f"Découverte de {place.get('nom', 'ce lieu')}"),
                    "eco_highlights": self._get_place_eco_highlights(place)
                })
        
        return itinerary
    
    def _calculate_package_costs(
        self, 
        places: List[Dict[str, Any]], 
        accommodations: List[Dict[str, Any]],
        duration: int,
        transport_pref: str
    ) -> Dict[str, Any]:
        """Calcule les coûts du package"""
        
        # Coûts hébergements (peut être 0 si pas d'hébergements)
        if accommodations and len(accommodations) > 0:
            accommodation_cost = sum(float(acc.get('prix', acc.get('price', 80))) for acc in accommodations) * duration
        else:
            # Si pas d'hébergements, estimer un coût moyen
            accommodation_cost = duration * 100  # 100€ par nuit en moyenne
        
        # Coûts activités (BASÉ SUR LES DESTINATIONS)
        activity_cost = len(places) * 25  # Moyenne 25€ par activité/destination
        
        # Coûts transport
        transport_costs = {
            'train': 150,
            'bike': 50,
            'car': 200,
            'mixed': 180
        }
        transport_cost = transport_costs.get(transport_pref, 180)
        
        # Coûts repas
        meals_cost = duration * 35  # Moyenne 35€ par jour
        
        total = accommodation_cost + activity_cost + transport_cost + meals_cost
        
        return {
            'accommodation': round(accommodation_cost, 2),
            'activities': round(activity_cost, 2),
            'transport': round(transport_cost, 2),
            'meals': round(meals_cost, 2),
            'total': round(total, 2)
        }
    
    def _get_transport_recommendations(self, preference: str, eco_priority: str) -> List[Dict[str, Any]]:
        """Retourne des recommandations de transport"""
        recommendations = [
            {"type": "Train", "eco_score": 95, "description": "Le plus écologique pour les longues distances"},
            {"type": "Vélo", "eco_score": 100, "description": "Zéro émission, parfait pour les courtes distances"},
            {"type": "Voiture électrique partagée", "eco_score": 80, "description": "Flexible avec impact réduit"},
            {"type": "Bus électrique", "eco_score": 85, "description": "Économique et écologique"}
        ]
        
        if eco_priority in ['high', 'very_high']:
            return [r for r in recommendations if r['eco_score'] >= 85]
        return recommendations
    
    def _get_sustainability_highlights(self, places: List[Dict[str, Any]], accommodations: List[Dict[str, Any]]) -> List[str]:
        """Génère les points forts de durabilité du package"""
        highlights = []
        
        # Certifications des lieux
        total_certifications = sum(
            1 for place in places 
            if place.get('certifications') or place.get('certification')
        )
        if total_certifications > 0:
            highlights.append(f"{total_certifications} lieux avec certifications écologiques")
        
        # Score moyen de durabilité
        if places:
            avg_score = sum(float(p.get('scoreDurabilite', p.get('scoreDurabilité', 50))) for p in places) / len(places)
            if avg_score >= 80:
                highlights.append(f"Score de durabilité moyen excellent: {round(avg_score, 1)}/100")
            elif avg_score >= 70:
                highlights.append(f"Bon score de durabilité moyen: {round(avg_score, 1)}/100")
        
        # Hébergements écologiques
        if accommodations:
            eco_accs = [a for a in accommodations if float(a.get('scoreDurabilite', a.get('scoreDurabilité', 0))) >= 75]
            if eco_accs:
                highlights.append(f"{len(eco_accs)} hébergement(s) hautement écologique(s)")
        
        if not highlights:
            highlights.append("Package conçu avec attention à l'environnement")
        
        return highlights
    
    def _get_place_eco_highlights(self, place: Dict[str, Any]) -> List[str]:
        """Extrait les points forts écologiques d'un lieu"""
        highlights = []
        
        cert = place.get('certifications', place.get('certification', ''))
        if cert:
            highlights.append(f"Certification: {cert}")
        
        score = float(place.get('scoreDurabilite', place.get('scoreDurabilité', 0)))
        if score >= 80:
            highlights.append(f"Très haute durabilité ({score}/100)")
        elif score >= 70:
            highlights.append(f"Haute durabilité ({score}/100)")
        
        return highlights if highlights else ["Engagé dans le tourisme durable"]
    
    def _get_mock_destinations(self) -> List[Dict[str, Any]]:
        """Retourne des destinations mock pour démonstration"""
        return [
            {
                "nom": "Parc National de la Forêt Verte",
                "type": "Nature",
                "description": "Parc naturel avec sentiers écologiques et faune protégée",
                "scoreDurabilite": "88",
                "certifications": "ISO 14001, Green Globe",
                "region": "Montagnes"
            },
            {
                "nom": "Éco-Village des Collines",
                "type": "Culturel",
                "description": "Village traditionnel avec architecture durable et artisanat local",
                "scoreDurabilite": "92",
                "certifications": "Bio, Eco-Label Européen",
                "region": "Campagne"
            },
            {
                "nom": "Réserve Marine Côtière",
                "type": "Nature",
                "description": "Réserve marine protégée avec plages écologiques",
                "scoreDurabilite": "85",
                "certifications": "Marine Conservation, Blue Flag",
                "region": "Côte"
            },
            {
                "nom": "Centre Historique Restauré",
                "type": "Culturel",
                "description": "Centre ville historique avec bâtiments éco-rénovés",
                "scoreDurabilite": "78",
                "certifications": "UNESCO, Green Building",
                "region": "Urbain"
            },
            {
                "nom": "Sentier Écologique des Cascades",
                "type": "Nature",
                "description": "Randonnée écologique le long de cascades naturelles",
                "scoreDurabilite": "95",
                "certifications": "Eco-Trail, Protected Area",
                "region": "Forêt"
            },
            {
                "nom": "Vignoble Biodynamique",
                "type": "Gastronomie",
                "description": "Vignoble certifié bio avec dégustation locale",
                "scoreDurabilite": "87",
                "certifications": "Bio, Demeter, Agriculture Durable",
                "region": "Vignoble"
            },
            {
                "nom": "Lac Écologique des Montagnes",
                "type": "Nature",
                "description": "Lac de montagne avec activités nautiques durables",
                "scoreDurabilite": "90",
                "certifications": "Clean Water, Eco-Tourism",
                "region": "Montagnes"
            }
        ]
    
    def _get_mock_accommodations(self) -> List[Dict[str, Any]]:
        """Retourne des hébergements mock pour démonstration"""
        return [
            {
                "nom": "Éco-Lodge du Parc",
                "type": "Lodge",
                "description": "Lodge écologique au cœur de la nature",
                "scoreDurabilite": "89",
                "certifications": "Green Key, Eco-Lodge Certified",
                "prix": "120",
                "destination": "Parc National de la Forêt Verte"
            },
            {
                "nom": "Maison d'Hôtes Bio",
                "type": "Guesthouse",
                "description": "Chambres chez l'habitant avec petit-déjeuner bio",
                "scoreDurabilite": "86",
                "certifications": "Bio, Ecolabel",
                "prix": "75",
                "destination": "Éco-Village des Collines"
            },
            {
                "nom": "Hôtel Durable Centre-Ville",
                "type": "Hotel",
                "description": "Hôtel moderne avec certification environnementale",
                "scoreDurabilite": "82",
                "certifications": "ISO 14001, Green Building",
                "prix": "140",
                "destination": "Centre Historique Restauré"
            },
            {
                "nom": "Cabane Écologique en Forêt",
                "type": "Cabane",
                "description": "Hébergement insolite en harmonie avec la nature",
                "scoreDurabilite": "94",
                "certifications": "Eco-Lodging, Carbon Neutral",
                "prix": "95",
                "destination": "Sentier Écologique des Cascades"
            },
            {
                "nom": "Gîte du Vignoble",
                "type": "Guesthouse",
                "description": "Gîte confortable au milieu des vignes bio",
                "scoreDurabilite": "88",
                "certifications": "Bio, Sustainable Tourism",
                "prix": "110",
                "destination": "Vignoble Biodynamique"
            }
        ]

