# 📚 Documentation Complète des Endpoints API

## Base URL
```
http://localhost:8000
```

## Authentication
Aucune authentication requise pour la version actuelle.

---

## 1. Health Check

### GET `/health`
Vérifie l'état de l'application

**Réponse (200):**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-04T10:30:00",
  "services": {
    "fuseki": "connected",
    "nl_converter": "ready"
  }
}
```

---

## 2. Recommandations

### GET `/recommendation/profiles`
Liste les profils de voyageurs disponibles

**Réponse (200):**
```json
{
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
```

---

### GET `/recommendation/generate`
Génère une recommandation personnalisée complète

**Paramètres Query:**
| Paramètre | Type | Requis | Description | Exemple |
|-----------|------|--------|-------------|---------|
| profile | string | ✅ | Profil voyageur | `Adventure` |
| destination | string | ✅ | Destination | `Paris` |
| budget | float | ❌ | Budget en € | `1000` |
| carbon_priority | boolean | ❌ | Priorité écologie | `true` |
| days | integer | ❌ | Nombre de jours | `3` |

**Exemple de requête:**
```bash
GET /recommendation/generate?profile=Adventure&destination=Alpes&budget=1500&carbon_priority=true&days=5
```

**Réponse (200):**
```json
{
  "profile": "Adventure",
  "destination": "Alpes",
  "duration_days": 5,
  "recommendation_score": 87.5,
  "activities": [
    {
      "nom": "Randonnée Chamonix",
      "description": "Ascension du Mont-Blanc",
      "match_score": 95
    }
  ],
  "accommodation": {
    "nom": "Gîte Écologique Chamonix",
    "description": "Petit gîte respectueux de l'environnement",
    "scoreDurabilite": 85
  },
  "transport": {
    "nom": "TGV Éco",
    "carbon": {
      "level": "Faible",
      "score": 92,
      "kg_co2": 20
    }
  },
  "total_carbon_kg": 45.5,
  "budget": 1500,
  "eco_friendly": true,
  "reasons": [
    "Recommandation adaptée au profil 'Adventure'",
    "2 activités suggérées basées sur vos préférences",
    "Hébergement très respectueux de l'environnement (85/100)",
    "Options de transport à faible empreinte carbone sélectionnées"
  ]
}
```

---

### GET `/recommendation/carbon-calculator`
Calcule l'empreinte carbone d'un transport

**Paramètres Query:**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| transport_type | string | ✅ | Type de transport |
| distance_km | float | ✅ | Distance en km |

**Types supportés:**
- `Avion`
- `Train`
- `Bus`
- `Voiture`
- `Velo`

**Exemple:**
```bash
GET /recommendation/carbon-calculator?transport_type=Avion&distance_km=1000
```

**Réponse (200):**
```json
{
  "transport": "Avion",
  "distance_km": 1000,
  "total_co2_kg": 255,
  "carbon_level": "Élevée",
  "carbon_score": 45.5,
  "alternatives": [
    {
      "transport": "Train",
      "co2_kg": 41,
      "savings": 214
    }
  ]
}
```

---

### GET `/recommendation/activities`
Récupère les activités recommandées pour un profil

**Paramètres Query:**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| profile | string | ✅ | Profil voyageur |

**Réponse (200):**
```json
{
  "profile": "Adventure",
  "activities": [
    {
      "nom": "Randonnée",
      "match_score": 100
    },
    {
      "nom": "Plongée",
      "match_score": 90
    }
  ],
  "total": 12
}
```

---

### GET `/recommendation/accommodations`
Hébergements recommandés pour un profil

**Réponse (200):**
```json
{
  "profile": "Adventure",
  "accommodations": [
    {
      "nom": "Camping Éco",
      "scoreDurabilite": 88
    }
  ],
  "total": 5
}
```

---

### GET `/recommendation/transports`
Options de transport disponibles

**Paramètres Query:**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| carbon_sensitive | boolean | ❌ | Trier par CO2 |

**Réponse (200):**
```json
{
  "carbon_sensitive": true,
  "transports": [
    {
      "nom": "Vélo Électrique",
      "carbon": {
        "level": "Faible",
        "score": 100,
        "kg_co2": 0
      }
    }
  ],
  "total": 6
}
```

---

## 3. Recherche SPARQL

### POST `/query`
Convertit une question en langage naturel français en SPARQL et exécute

**Body:**
```json
{
  "question": "Quels sont les hébergements écologiques à Paris ?"
}
```

**Réponse (200):**
```json
{
  "question": "Quels sont les hébergements écologiques à Paris ?",
  "sparql_query": "PREFIX eco: <...> SELECT ?hebergement ...",
  "results": [
    {
      "hebergement": "Hotel Eco Paris 1",
      "nom": "Hotel Écologique Central",
      "scoreDurabilite": "85"
    }
  ],
  "execution_time": 0.245
}
```

**Erreurs possibles:**
- 400: Question vide
- 500: Erreur de conversion ou exécution

---

### GET `/sparql`
Exécute une requête SPARQL directe

**Paramètres Query:**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| query | string | ✅ | Requête SPARQL |

**Exemple:**
```bash
GET /sparql?query=SELECT%20%3Factivite%20%3Fnom%20WHERE%20%7B%0A%20%20%3Factivite%20rdf%3Atype%20eco%3AActiviteSportive%20%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20eco%3Anom%20%3Fnom%20.%0A%7D
```

**Réponse (200):**
```json
{
  "query": "SELECT ?activite ?nom WHERE {...}",
  "results": [
    {
      "activite": "http://example.org/randonnee",
      "nom": "Randonnée"
    }
  ],
  "count": 1
}
```

---

## 4. Données

### GET `/collection-points`
Récupère tous les points de collecte

**Paramètres Query:**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| city | string | ❌ | Filtrer par ville |

**Réponse (200):**
```json
{
  "collection_points": [
    {
      "nom": "Point 1",
      "adresse": "123 Rue de la Paix"
    }
  ],
  "count": 5,
  "city": "Paris"
}
```

---

### GET `/waste-types`
Types de déchets disponibles

**Réponse (200):**
```json
{
  "waste_types": [
    {
      "nom": "Déchets Organiques",
      "description": "Résidus alimentaires"
    }
  ],
  "count": 4
}
```

---

### GET `/activities`
Toutes les activités communautaires

**Réponse (200):**
```json
{
  "activities": [
    {
      "nom": "Nettoyage Plage",
      "description": "Activité de sensibilisation"
    }
  ],
  "count": 8
}
```

---

### GET `/badges`
Badges disponibles

**Réponse (200):**
```json
{
  "badges": [
    {
      "nom": "Éco-Citoyen",
      "description": "Première participation"
    }
  ],
  "count": 6
}
```

---

## 5. Community

### POST `/contribution`
Ajoute une nouvelle contribution

**Body:**
```json
{
  "utilisateur": "jean_dupont",
  "description": "Collecte de 50kg de déchets",
  "type": "contribution",
  "quantite": 50,
  "unite": "kg"
}
```

**Réponse (200):**
```json
{
  "status": "success",
  "contribution_id": "contribution_1730688600",
  "message": "Contribution ajoutée avec succès"
}
```

---

## 6. Analytics

### GET `/stats`
Statistiques communautaires

**Réponse (200):**
```json
{
  "statistics": {
    "totalUsers": "42",
    "totalActivities": "15",
    "totalPoints": "8"
  },
  "timestamp": "2025-11-04T10:30:00"
}
```

---

## 7. Documentation

### GET `/examples`
Requêtes d'exemple

**Réponse (200):**
```json
{
  "examples": {
    "all_collection_points": "SELECT ?point ...",
    "collection_points_in_paris": "SELECT ?point ...",
    ...
  },
  "description": "Exemples de requêtes SPARQL"
}
```

---

## Codes de Réponse HTTP

| Code | Signification |
|------|--------------|
| 200 | Succès |
| 400 | Paramètres invalides |
| 404 | Resource non trouvée |
| 500 | Erreur serveur |

---

## Formats

### Query String (GET)
```
/endpoint?param1=value1&param2=value2
```

### JSON Body (POST)
```json
{
  "key": "value"
}
```

### Réponses
Toutes les réponses sont en JSON.

---

## Rate Limiting

Aucune limite de requêtes configurée actuellement.

---

## Exemples cURL

### 1. Générer une recommandation
```bash
curl -X GET "http://localhost:8000/recommendation/generate?profile=Adventure&destination=Paris&budget=1000&carbon_priority=true&days=3"
```

### 2. Question en langage naturel
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"Quelles activités sportives à Paris?"}'
```

### 3. Calculer empreinte carbone
```bash
curl -X GET "http://localhost:8000/recommendation/carbon-calculator?transport_type=Avion&distance_km=500"
```

### 4. Vérifier santé
```bash
curl -X GET "http://localhost:8000/health"
```

---

## Notes Importantes

1. **Fuseki doit être en cours d'exécution** pour que les requêtes SPARQL fonctionnent
2. **L'ontologie RDF** doit être chargée dans Fuseki
3. **CORS est activé** pour `http://localhost:3000`
4. Les **questions en français** sont supportées pour NL to SPARQL

---

**Documentation mise à jour le 04 novembre 2025**
