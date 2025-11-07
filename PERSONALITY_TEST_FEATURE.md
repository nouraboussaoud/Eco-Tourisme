# 🧭 Test de Personnalité & Packages de Voyage Personnalisés

## 📋 Vue d'ensemble

Cette fonctionnalité permet aux utilisateurs de passer un test de personnalité de 5-7 questions pour découvrir leur profil de voyageur et recevoir des recommandations personnalisées de packages de voyage basées sur :

- Les réponses au test de personnalité
- L'analyse IA (Google Gemini)
- Les données SPARQL (lieux, hébergements avec certifications écologiques)
- Les préférences environnementales

## 🎯 Fonctionnalités

### 1. Test de Personnalité (7 Questions)

Le test comprend des questions sur :
- Type d'activité préférée
- Préoccupation environnementale
- Type d'hébergement
- Durée de séjour
- Budget
- Moyen de transport
- Priorités de voyage

### 2. Analyse IA avec Google Gemini

- Utilise Gemini Pro pour analyser les réponses
- Génère un profil de personnalité détaillé
- Fournit des recommandations basées sur le profil
- Fallback intelligent si Gemini n'est pas disponible

### 3. Intégration SPARQL

- Récupère les destinations avec leurs certifications écologiques
- Filtre les hébergements selon le score de durabilité
- Analyse les certifications (ISO 14001, Green Globe, Bio, etc.)
- Score les lieux selon leur compatibilité avec le profil

### 4. Génération de Package de Voyage

Chaque package inclut :
- **Profil de personnalité** : Type, description, préférences
- **Itinéraire détaillé** : Jour par jour avec activités
- **Lieux recommandés** : Avec scores de correspondance et certifications
- **Hébergements** : Filtrés par durabilité et budget
- **Options de transport** : Selon priorité écologique
- **Détail des coûts** : Hébergement, activités, transport, repas
- **Points forts de durabilité** : Certifications, scores écologiques

## 🚀 Utilisation

### Configuration

1. **La clé API Gemini est déjà configurée** dans votre fichier `.env` :

```env
GEMINI_API_KEY=AIzaSyAvMIn3rIX1eaTgSuOoejjLI4vf5d909GM
```

2. **Les dépendances sont déjà installées** :

La dépendance `google-generativeai>=0.3.0` est déjà incluse dans `requirements.txt`.

### API Endpoints

#### 1. Récupérer les questions du test

```http
GET /personality-test/questions
```

**Réponse** :
```json
{
  "questions": [
    {
      "id": 1,
      "question": "Quel type d'activité vous attire le plus...",
      "options": [
        {"value": "adventure", "label": "Sports extrêmes..."},
        ...
      ]
    },
    ...
  ],
  "total_questions": 7
}
```

#### 2. Analyser les réponses (profil uniquement)

```http
POST /personality-test/analyze
Content-Type: application/json

{
  "answers": {
    "1": "adventure",
    "2": "very_high",
    "3": "eco_lodge",
    ...
  }
}
```

**Réponse** :
```json
{
  "status": "success",
  "personality_profile": {
    "personality_type": "Aventurier Écologique",
    "profile_description": "Vous aimez l'aventure...",
    "preferences": {
      "activity_level": "high",
      "eco_priority": "very_high",
      "accommodation_style": "eco_lodge",
      "transport_preference": "train",
      "budget_range": 1200,
      "duration_days": 5
    },
    "eco_score": 95
  }
}
```

#### 3. Générer un package complet de voyage

```http
POST /personality-test/generate-package
Content-Type: application/json

{
  "answers": {
    "1": "adventure",
    "2": "very_high",
    "3": "eco_lodge",
    "4": "medium",
    "5": "moderate",
    "6": "train",
    "7": "authentic"
  }
}
```

**Réponse** :
```json
{
  "status": "success",
  "personality_profile": { ... },
  "trip_package": {
    "package_name": "Package Aventurier Écologique",
    "duration_days": 5,
    "total_budget": 1250.50,
    "eco_score": 88,
    "breakdown": {
      "accommodation": 600,
      "activities": 175,
      "transport": 150,
      "meals": 325.50,
      "total": 1250.50
    },
    "itinerary": [
      {
        "day": 1,
        "title": "Jour 1: Parc National",
        "place": "Parc National",
        "activities": ["Randonnée", "Observation faune"],
        "description": "Découverte de...",
        "eco_highlights": ["Certification: ISO 14001"]
      },
      ...
    ],
    "places": [
      {
        "nom": "Parc National",
        "type": "Nature",
        "scoreDurabilite": "85",
        "certifications": "ISO 14001, Green Globe",
        "eco_match_score": 92.5
      },
      ...
    ],
    "accommodations": [
      {
        "nom": "Éco-Lodge du Parc",
        "type": "Lodge",
        "scoreDurabilite": "88",
        "certifications": "Green Key",
        "prix": "120"
      }
    ],
    "transport_recommendations": [
      {
        "type": "Train",
        "eco_score": 95,
        "description": "Le plus écologique..."
      }
    ],
    "sustainability_highlights": [
      "5 lieux avec certifications écologiques",
      "Score de durabilité moyen excellent: 87.2/100",
      "2 hébergement(s) hautement écologique(s)"
    ]
  }
}
```

#### 4. Package exemple (pour tester)

```http
GET /personality-test/sample-package?personality_type=adventure
```

Génère un package de démonstration avec des données mock.

## 🎨 Interface Frontend

### Composant PersonalityTest

Situé dans : `frontend/src/components/PersonalityTest.jsx`

**Fonctionnalités** :
- Navigation entre les questions
- Suivi de progression avec barre visuelle
- Sélection des réponses avec interface intuitive
- Affichage complet des résultats avec :
  - Profil de personnalité
  - Score écologique
  - Itinéraire détaillé
  - Cartes de lieux et hébergements
  - Détail des coûts
  - Options de transport
  - Points forts de durabilité
- Options d'impression et de recommencement

**Accès** :
- Menu principal : "Test Personnalité"
- Icône : 🧭

## 🔧 Architecture Technique

### Backend

#### `services/personality_test_service.py`

**Classe principale** : `PersonalityTestService`

**Méthodes clés** :
- `get_questions()` : Retourne les 7 questions du test
- `analyze_personality_with_ai(answers)` : Analyse avec Gemini Pro
- `_fallback_personality_analysis(answers)` : Analyse sans IA
- `generate_trip_package(profile, places, accommodations)` : Crée le package
- `_score_places_by_certification(places, eco_priority)` : Score les lieux
- `_filter_accommodations(accommodations, budget, eco_priority)` : Filtre hébergements
- `_generate_itinerary(places, duration)` : Crée l'itinéraire
- `_calculate_package_costs(...)` : Calcule les coûts

#### Intégration SPARQL

Requêtes pour récupérer :

**Destinations** :
```sparql
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
SELECT ?nom ?type ?description ?scoreDurabilite ?certifications
WHERE {
    ?place rdf:type eco:Destination .
    ?place eco:nom ?nom .
    OPTIONAL { ?place eco:certifications ?certifications }
    ...
}
```

**Hébergements** :
```sparql
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
SELECT ?nom ?type ?scoreDurabilite ?certifications ?prix
WHERE {
    ?acc rdf:type eco:Hebergement .
    ...
}
```

### Frontend

#### Composants
- `PersonalityTest.jsx` : Composant principal
- `PersonalityTest.css` : Styles dédiés

#### États React
- `questions` : Questions du test
- `currentQuestionIndex` : Navigation
- `answers` : Réponses utilisateur
- `personalityProfile` : Profil généré
- `tripPackage` : Package de voyage
- `loading` / `error` : États UI

## 📊 Système de Scoring

### Score de Correspondance Écologique

Les lieux sont scorés selon :

1. **Certification** (20-60% selon priorité écologique) :
   - ISO 14001, Green Globe, Eco-Label : 90 points
   - Autres certifications : 70 points
   - Pas de certification : 0 points

2. **Score de durabilité** (20-50%) :
   - Score direct du lieu (0-100)

3. **Activités** (20-30%) :
   - Score de base : 50 points

### Filtrage des Hébergements

- **Score minimum** selon priorité :
  - Très élevé : 85/100
  - Élevé : 70/100
  - Modéré : 60/100
  - Faible : 50/100

- **Budget** : 40% du budget journalier

## 🌱 Types de Personnalité

### Profils générés

1. **Aventurier Écologique**
   - Activités : Randonnée, escalade, VTT, kayak
   - Priorité : Nature + Sport + Écologie

2. **Explorateur Culturel**
   - Activités : Musées, visites guidées, ateliers
   - Priorité : Culture + Authenticité

3. **Voyageur Zen**
   - Activités : Yoga, spa, méditation
   - Priorité : Détente + Bien-être

4. **Nature Conscient**
   - Activités : Observation faune, randonnées douces
   - Priorité : Nature + Équilibre

## 🔄 Mode Fallback

Si Gemini n'est pas disponible :
- Analyse locale des réponses
- Mapping des réponses vers profils prédéfinis
- Génération de package avec logique locale
- Fonctionnalité complète maintenue

## 📝 Exemple d'utilisation complète

```javascript
// Frontend
const handleSubmitTest = async () => {
  const answers = {
    "1": "adventure",
    "2": "very_high",
    "3": "eco_lodge",
    "4": "medium",
    "5": "moderate",
    "6": "train",
    "7": "authentic"
  };

  const response = await fetch('http://localhost:8000/personality-test/generate-package', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answers })
  });

  const data = await response.json();
  
  console.log(data.personality_profile.personality_type);
  // => "Aventurier Écologique"
  
  console.log(data.trip_package.itinerary.length);
  // => 5 (jours)
  
  console.log(data.trip_package.total_budget);
  // => 1250.50 (euros)
};
```

## 🎯 Améliorations Futures

- [ ] Support de plus de modèles IA (GPT-4, Claude)
- [ ] Comparaison de plusieurs packages
- [ ] Sauvegarde des profils utilisateur
- [ ] Partage social des packages
- [ ] Réservation intégrée
- [ ] Suivi de l'empreinte carbone réelle
- [ ] Recommandations basées sur la saison
- [ ] Intégration météo
- [ ] Avis communautaires sur les packages

## 🐛 Dépannage

### Gemini ne répond pas
- Vérifier la clé API dans `.env`
- Le système bascule automatiquement en mode fallback

### Pas de données SPARQL
- Vérifier que Fuseki est lancé
- Des données mock sont utilisées en fallback

### Erreur de parsing Gemini
- Le format JSON de la réponse est attendu
- Fallback automatique en cas d'erreur

## 📚 Ressources

- Documentation Gemini : https://ai.google.dev/docs
- SPARQL Tutorial : https://www.w3.org/TR/sparql11-query/
- React Hooks : https://react.dev/reference/react

## 👥 Contribution

Pour ajouter de nouvelles questions au test, modifiez `PERSONALITY_QUESTIONS` dans `personality_test_service.py`.

Pour personnaliser les profils, ajustez la méthode `_fallback_personality_analysis()`.
