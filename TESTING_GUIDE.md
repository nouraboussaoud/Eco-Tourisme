# 🧪 Guide Complet de Testing - EcoTravel Platform

## Table des Matières
1. [Setup Environnement](#setup)
2. [Tests Unitaires](#tests-unitaires)
3. [Tests API](#tests-api)
4. [Tests Frontend](#tests-frontend)
5. [Tests Intégration](#tests-intégration)
6. [Troubleshooting](#troubleshooting)

---

## Setup Environnement {#setup}

### Prérequis
- ✅ Python 3.8+
- ✅ Node.js 16+
- ✅ Apache Jena Fuseki 4.0+
- ✅ Git

### Installation Rapide

**Étape 1: Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Étape 2: Frontend Setup**
```bash
cd frontend
npm install
```

**Étape 3: Fuseki Setup**
```bash
# Télécharger Apache Jena Fuseki
# https://jena.apache.org/download/

# Créer dataset "eco-tourism"
# Aller sur http://localhost:3030/
# Clic "New Dataset" → Name: eco-tourism → Persistent
```

---

## Tests Unitaires {#tests-unitaires}

### 1️⃣ Test RecommendationEngine

Créer fichier: `backend/tests/test_recommendation_engine.py`

```python
import sys
sys.path.insert(0, '../')

from services.recommendation_engine import RecommendationEngine
import json

print("🧪 Testing RecommendationEngine\n")

# Initialiser le service
engine = RecommendationEngine()

# TEST 1: Carbon Score Calculation
print("TEST 1: calculate_carbon_score()")
print("-" * 50)

test_cases = [
    (30, "Faible"),
    (100, "Moyen"),
    (200, "Élevé"),
]

for co2, expected_level in test_cases:
    result = engine.calculate_carbon_score(co2)
    status = "✅" if result["level"] == expected_level else "❌"
    print(f"{status} CO2: {co2}kg → Level: {result['level']}, Score: {result['score']}")

# TEST 2: Match Score
print("\n\nTEST 2: calculate_match_score()")
print("-" * 50)

match_cases = [
    ("Adventure", "ActiviteSportive", 100),
    ("Culture", "ActiviteCulturelle", 100),
    ("BienEtre", "Spa", 100),
    ("Famille", "ActiviteEducative", 100),
    ("Adventure", "Musée", 0),  # Bad match
]

for profile, activity, expected_score in match_cases:
    result = engine.calculate_match_score(profile, activity)
    status = "✅" if result == expected_score else "❌"
    print(f"{status} {profile} + {activity} = {result} (expected {expected_score})")

# TEST 3: Profile Activity Filtering
print("\n\nTEST 3: get_activities_for_profile()")
print("-" * 50)

profiles = ["Adventure", "Culture", "BienEtre", "Famille"]
for profile in profiles:
    print(f"\n👤 Profile: {profile}")
    try:
        activities = engine.get_activities_for_profile(profile)
        print(f"   ✅ Retrieved {len(activities) if activities else 0} activities")
        if activities:
            print(f"   Sample: {activities[0]}")
    except Exception as e:
        print(f"   ⚠️  Error: {str(e)}")

# TEST 4: Carbon Calculator
print("\n\nTEST 4: Carbon Calculator")
print("-" * 50)

transports = [
    ("avion", 1000),
    ("train", 500),
    ("bus", 200),
    ("voiture", 800),
]

for transport, distance in transports:
    try:
        result = engine.calculate_carbon_score(engine.transport_carbon_per_km.get(transport, 0.15) * distance)
        print(f"✅ {transport.capitalize()} ({distance}km): {result['kg_co2']}kg CO2 - {result['level']}")
    except Exception as e:
        print(f"❌ Error calculating {transport}: {str(e)}")

print("\n" + "="*50)
print("Tests unitaires terminés!")
```

**Exécuter:**
```bash
cd backend
python tests/test_recommendation_engine.py
```

---

## Tests API {#tests-api}

### 2️⃣ Test Endpoints via cURL

**Pré-requis:** Backend actif sur `http://localhost:8000`

#### Test A: Health Check
```bash
curl -X GET "http://localhost:8000/health" -H "Content-Type: application/json"
```

**Résultat attendu:**
```json
{"status": "ok", "timestamp": "2025-11-04T..."}
```

#### Test B: Récupérer Profils
```bash
curl -X GET "http://localhost:8000/recommendation/profiles" \
  -H "Content-Type: application/json"
```

**Résultat attendu:**
```json
{
  "profiles": [
    {"id": "Adventure", "description": "Voyageur aventurier..."},
    {"id": "Culture", "description": "Passionné par la culture..."},
    ...
  ]
}
```

#### Test C: Générer Recommandation
```bash
curl -X GET "http://localhost:8000/recommendation/generate?profile=Adventure&destination=Maroc&budget=2000&carbon_priority=false&days=5" \
  -H "Content-Type: application/json"
```

**Résultat attendu:**
```json
{
  "profile": "Adventure",
  "destination": "Maroc",
  "recommendation_score": 85.5,
  "activities": [
    {
      "name": "Randonnée",
      "match_score": 100,
      "carbon_level": "Faible"
    }
  ],
  "total_carbon_kg": 255,
  "reasons": ["Bon match profil", "Destination ensoleillée"]
}
```

#### Test D: Calcul Empreinte Carbone
```bash
curl -X GET "http://localhost:8000/recommendation/carbon-calculator?transport_type=avion&distance_km=1000" \
  -H "Content-Type: application/json"
```

**Résultat attendu:**
```json
{
  "transport": "avion",
  "distance_km": 1000,
  "kg_co2": 255,
  "carbon_level": "Élevé",
  "score": 25,
  "alternatives": [
    {"transport": "train", "kg_co2": 15, "score": 100}
  ]
}
```

#### Test E: Activités par Profil
```bash
curl -X GET "http://localhost:8000/recommendation/activities?profile=Culture" \
  -H "Content-Type: application/json"
```

#### Test F: Hébergements Eco
```bash
curl -X GET "http://localhost:8000/recommendation/accommodations?profile=Famille" \
  -H "Content-Type: application/json"
```

#### Test G: Transports Disponibles
```bash
curl -X GET "http://localhost:8000/recommendation/transports?carbon_sensitive=true" \
  -H "Content-Type: application/json"
```

### Script Batch Testing

Créer fichier: `backend/test_api.ps1`

```powershell
# Script de test batch pour tous les endpoints

$baseUrl = "http://localhost:8000"
$profiles = @("Adventure", "Culture", "BienEste", "Famille")

Write-Host "🧪 Testing EcoTravel API" -ForegroundColor Green
Write-Host "=" * 60

# Test 1: Health Check
Write-Host "`n1️⃣ Health Check" -ForegroundColor Yellow
$response = curl -s "$baseUrl/health"
Write-Host "✅ Response: $response"

# Test 2: Profiles
Write-Host "`n2️⃣ Get Profiles" -ForegroundColor Yellow
$response = curl -s "$baseUrl/recommendation/profiles"
Write-Host "✅ Response: $response" | ConvertFrom-Json | Out-String

# Test 3: Generate Recommendations for Each Profile
Write-Host "`n3️⃣ Generate Recommendations" -ForegroundColor Yellow
foreach ($profile in $profiles) {
    Write-Host "   Testing profile: $profile" -ForegroundColor Cyan
    $url = "$baseUrl/recommendation/generate?profile=$profile&destination=Maroc&budget=2000&days=5"
    $response = curl -s "$url"
    $json = $response | ConvertFrom-Json
    Write-Host "   ✅ Score: $($json.recommendation_score)" -ForegroundColor Green
}

# Test 4: Carbon Calculator
Write-Host "`n4️⃣ Carbon Calculator" -ForegroundColor Yellow
$transports = @("avion", "train", "bus")
foreach ($transport in $transports) {
    $url = "$baseUrl/recommendation/carbon-calculator?transport_type=$transport&distance_km=500"
    $response = curl -s "$url"
    $json = $response | ConvertFrom-Json
    Write-Host "   $transport → $($json.kg_co2)kg CO2 ($($json.carbon_level))" -ForegroundColor Green
}

Write-Host "`n" + "=" * 60
Write-Host "✅ All tests completed!" -ForegroundColor Green
```

**Exécuter:**
```powershell
cd backend
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

---

## Tests Frontend {#tests-frontend}

### 3️⃣ Test Composant Recommandations

Créer fichier: `frontend/src/components/__tests__/Recommendations.test.jsx`

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Recommendations from '../Recommendations';
import axios from 'axios';

jest.mock('axios');

describe('Recommendations Component', () => {
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('✅ Component renders with form', () => {
    render(<Recommendations apiUrl="http://localhost:8000" />);
    
    expect(screen.getByText(/Générateur de Recommandations/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Profil du Voyageur/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Destination/i)).toBeInTheDocument();
  });

  test('✅ Fetches profiles on mount', async () => {
    const mockProfiles = {
      data: {
        profiles: [
          { id: "Adventure", description: "Aventurier" },
          { id: "Culture", description: "Culturel" }
        ]
      }
    };

    axios.get.mockResolvedValue(mockProfiles);

    render(<Recommendations apiUrl="http://localhost:8000" />);

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        'http://localhost:8000/recommendation/profiles'
      );
    });
  });

  test('✅ Generates recommendation on submit', async () => {
    const mockRecommendation = {
      data: {
        profile: "Adventure",
        recommendation_score: 85.5,
        activities: [
          { name: "Randonnée", match_score: 100 }
        ],
        total_carbon_kg: 255
      }
    };

    axios.get.mockResolvedValueOnce({
      data: { profiles: [{ id: "Adventure" }] }
    });
    axios.get.mockResolvedValueOnce(mockRecommendation);

    render(<Recommendations apiUrl="http://localhost:8000" />);

    const generateBtn = await screen.findByText(/Générer Recommandation/i);
    fireEvent.click(generateBtn);

    await waitFor(() => {
      expect(screen.getByText(/Adventure/)).toBeInTheDocument();
    });
  });

  test('✅ Displays error message on API failure', async () => {
    axios.get.mockRejectedValue(
      new Error('API Error')
    );

    render(<Recommendations apiUrl="http://localhost:8000" />);

    const generateBtn = await screen.findByText(/Générer Recommandation/i);
    fireEvent.click(generateBtn);

    await waitFor(() => {
      expect(screen.getByText(/Erreur lors/i)).toBeInTheDocument();
    });
  });
});
```

**Setup Testing Library:**
```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

**Exécuter:**
```bash
cd frontend
npm test -- Recommendations.test.jsx
```

---

## Tests Intégration {#tests-intégration}

### 4️⃣ Test End-to-End (E2E)

Créer fichier: `backend/tests/test_integration.py`

```python
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("🧪 Integration Tests - EcoTravel Platform\n")
print("=" * 60)

# TEST 1: Complete User Journey - Adventure Profile
print("\n1️⃣ User Journey: Adventure Profile")
print("-" * 60)

try:
    # Step 1: Fetch profiles
    print("Step 1: Fetching profiles...")
    response = requests.get(f"{BASE_URL}/recommendation/profiles")
    assert response.status_code == 200, f"Failed: {response.status_code}"
    profiles = response.json()['profiles']
    print(f"✅ Found {len(profiles)} profiles")

    # Step 2: Generate recommendation for Adventure
    print("\nStep 2: Generating Adventure recommendation...")
    params = {
        'profile': 'Adventure',
        'destination': 'Maroc',
        'budget': 2000,
        'carbon_priority': False,
        'days': 5
    }
    response = requests.get(f"{BASE_URL}/recommendation/generate", params=params)
    assert response.status_code == 200, f"Failed: {response.status_code}"
    recommendation = response.json()
    print(f"✅ Got recommendation score: {recommendation.get('recommendation_score')}")
    assert recommendation['profile'] == 'Adventure'

    # Step 3: Carbon calculation for transport
    print("\nStep 3: Calculating carbon for chosen transport...")
    response = requests.get(f"{BASE_URL}/recommendation/carbon-calculator", 
                           params={'transport_type': 'avion', 'distance_km': 1000})
    assert response.status_code == 200
    carbon_data = response.json()
    print(f"✅ Carbon: {carbon_data['kg_co2']}kg CO2 ({carbon_data['carbon_level']})")

    print("\n✅ Adventure journey PASSED")

except Exception as e:
    print(f"\n❌ Adventure journey FAILED: {str(e)}")

# TEST 2: Complete User Journey - Family Profile
print("\n\n2️⃣ User Journey: Family Profile")
print("-" * 60)

try:
    print("Step 1: Generating Family recommendation...")
    params = {
        'profile': 'Famille',
        'destination': 'France',
        'budget': 1500,
        'carbon_priority': True,
        'days': 3
    }
    response = requests.get(f"{BASE_URL}/recommendation/generate", params=params)
    assert response.status_code == 200
    recommendation = response.json()
    print(f"✅ Got recommendation score: {recommendation.get('recommendation_score')}")

    # Get eco accommodations
    print("\nStep 2: Fetching eco accommodations...")
    response = requests.get(f"{BASE_URL}/recommendation/accommodations", 
                           params={'profile': 'Famille'})
    assert response.status_code == 200
    accommodations = response.json()
    print(f"✅ Found eco accommodations")

    print("\n✅ Family journey PASSED")

except Exception as e:
    print(f"\n❌ Family journey FAILED: {str(e)}")

# TEST 3: Carbon Priority Filtering
print("\n\n3️⃣ Carbon Priority Filtering")
print("-" * 60)

try:
    # Without carbon priority
    print("Request 1: Without carbon priority...")
    response1 = requests.get(f"{BASE_URL}/recommendation/transports", 
                            params={'carbon_sensitive': False})
    assert response1.status_code == 200
    transports1 = response1.json()
    print(f"✅ Got transports list (length: {len(transports1) if isinstance(transports1, list) else 'dict'})")

    # With carbon priority
    print("Request 2: With carbon priority...")
    response2 = requests.get(f"{BASE_URL}/recommendation/transports", 
                            params={'carbon_sensitive': True})
    assert response2.status_code == 200
    transports2 = response2.json()
    print(f"✅ Got eco-sorted transports list")

    print("\n✅ Carbon filtering PASSED")

except Exception as e:
    print(f"\n❌ Carbon filtering FAILED: {str(e)}")

# TEST 4: Error Handling
print("\n\n4️⃣ Error Handling")
print("-" * 60)

try:
    # Invalid profile
    print("Test 1: Invalid profile...")
    response = requests.get(f"{BASE_URL}/recommendation/generate", 
                           params={'profile': 'InvalidProfile', 'destination': 'Test'})
    print(f"   Status: {response.status_code}")
    if response.status_code != 200:
        print(f"   ✅ Correctly rejected invalid profile")
    
    # Missing parameters
    print("Test 2: Missing required parameters...")
    response = requests.get(f"{BASE_URL}/recommendation/generate")
    print(f"   Status: {response.status_code}")
    if response.status_code != 200:
        print(f"   ✅ Correctly rejected incomplete request")

except Exception as e:
    print(f"⚠️  Error test: {str(e)}")

print("\n" + "=" * 60)
print("✅ Integration tests completed!")
```

**Exécuter:**
```bash
cd backend
python -m pip install requests
python tests/test_integration.py
```

---

## Test Checklist {#checklist}

### ✅ Pre-Launch Verification

- [ ] **Backend Startup**
  ```bash
  python main.py  # Should output "Uvicorn running on http://127.0.0.1:8000"
  ```

- [ ] **Frontend Startup**
  ```bash
  npm run dev  # Should output "VITE v4.x.x ready"
  ```

- [ ] **Fuseki Connection**
  ```bash
  curl http://localhost:3030/  # Should return HTML page
  ```

- [ ] **All Endpoints Accessible**
  ```bash
  # Run test_api.ps1 or test_integration.py
  ```

- [ ] **Frontend Loads**
  ```bash
  # Navigate to http://localhost:3000
  # Should see "Recommendations" tab in header
  ```

---

## Performance Testing {#performance}

### Load Test avec Apache Bench

```bash
# Installer Apache Bench (inclus avec Apache)
# ou utiliser: npm install -g autocannon

# Test 100 requêtes, 10 concurrentes
ab -n 100 -c 10 http://localhost:8000/recommendation/profiles

# Résultat attendu: <100ms/requête
```

---

## Troubleshooting {#troubleshooting}

### ❌ Backend ne démarre pas

```bash
# Vérifier port 8000
netstat -ano | findstr :8000

# Si occupé, tuer le processus
taskkill /PID <PID> /F

# Redémarrer backend
python main.py
```

### ❌ Fuseki inaccessible

```bash
# Vérifier Fuseki tourne
curl http://localhost:3030/

# Redémarrer Fuseki
# Dans dossier Fuseki:
fuseki-server --port 3030
```

### ❌ Erreur CORS

```python
# Vérifier CORS config dans backend/main.py
# Doit avoir:
app.add_middleware(CORSMiddleware, ...)
```

### ❌ Modules Python manquants

```bash
cd backend
pip install -r requirements.txt

# Si requirements.txt manquant:
pip install fastapi uvicorn requests pydantic
```

---

## Résumé des Tests

| Test | Commande | Durée | Résultat |
|------|----------|-------|----------|
| **Unit** | `python tests/test_recommendation_engine.py` | ~5s | ✅ Algos |
| **API** | `powershell test_api.ps1` | ~10s | ✅ Endpoints |
| **Integration** | `python tests/test_integration.py` | ~15s | ✅ E2E |
| **Frontend** | `npm test` | ~20s | ✅ Components |
| **Performance** | `ab -n 100` | ~30s | ✅ <100ms |

**Temps total: ~2 minutes pour validation complète**

---

## Liens Utiles

- 📖 [FastAPI Testing Docs](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- 📖 [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- 📖 [cURL Guide](https://curl.se/docs/manual.html)

