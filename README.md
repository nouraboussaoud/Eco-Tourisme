# 🌍 EcoTravel - Plateforme Intelligente de Tourisme Durable

**Recommandations personnalisées pour un tourisme éco-responsable basé sur le Web Sémantique**

## 📋 Vue d'ensemble

EcoTravel est une plateforme innovante qui combine:
- **Web Sémantique** : Utilise des ontologies RDF et SPARQL pour lier destinations, activités et profils de voyageurs
- **IA Intelligente** : Convertit les questions en langage naturel français en requêtes SPARQL
- **Recommandations Personnalisées** : Suggère des voyages adaptés aux préférences et valeurs écologiques
- **Calcul d'Empreinte Carbone** : Évalue l'impact environnemental des choix de voyage

## 🎯 Objectifs Principaux

✅ **Promouvoir un tourisme durable**  
✅ **Réduire l'empreinte carbone des voyages**  
✅ **Fournir des recommandations intelligentes et personnalisées**  
✅ **Encourager les choix respectueux de l'environnement**
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Dépannage](#dépannage)

## ✨ Caractéristiques

### 🤖 **Traitement du Langage Naturel**
- Conversion automatique de questions en français vers requêtes SPARQL
- Support de Google Gemini AI ou SpaCy (local)
- Pattern matching intelligent pour les questions communes sur les voyages

### 📊 **Données Sémantiques**
- Ontologie RDF complète pour tourisme durable
- Classes : Destinations, Hébergements, Activités, Transports, Voyageurs, Profils
- Propriétés complètes avec relations SPARQL

### 🏘️ **Engagement pour le Tourisme Durable**
- Système de certifications écologiques
- Activités touristiques responsables
- Suivi des voyages éco-responsables
- Dashboard d'impact écologique

### 🗺️ **Localisation et Destinations**
- Destinations avec coordonnées GPS
- Filtrage par région et type de tourisme
- Informations sur hébergements et activités locales

### 📈 **Analytiques**
- Statistiques en temps réel
- Calcul d'empreinte carbone
- Graphiques et rapports de durabilité
- Timeline des voyages

### 🎯 **Interface Moderne**
- Interface React réactive
- Design responsive (mobile-friendly)
- Animations fluides
- Accessibilité optimale

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND (React)                       │
│  Dashboard | Query | Collecte | Communauté | Stats      │
└────────────────────┬────────────────────────────────────┘
                     │ (HTTP/JSON)
┌────────────────────▼────────────────────────────────────┐
│              BACKEND (FastAPI)                           │
│  NL→SPARQL | Fusion | Routes | CORS | OpenAPI Docs     │
└────────────────────┬────────────────────────────────────┘
                     │ (SPARQL)
┌────────────────────▼────────────────────────────────────┐
│        APACHE JENA FUSEKI (Port 3030)                   │
│    Triplestore SPARQL | Gestion RDF/OWL                 │
└────────────────────┬────────────────────────────────────┘
                     │
                ┌────▼────┐
                │ waste-  │
                │management
                │   .rdf  │
                └─────────┘
```

## 📦 Prérequis

### Logiciels Requis
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Apache Jena Fuseki** - [Download](https://jena.apache.org/download/index.cgi)
- **Git** - [Download](https://git-scm.com/download/)

### Optionnel
- **Google Gemini API Key** - [Obtenir une clé](https://makersuite.google.com/app/apikey)
- **Docker** - Pour conteneurisation

## 🚀 Installation

### 1️⃣ **Cloner/Naviguer vers le projet**

```powershell
cd "c:\Users\abous\OneDrive\Bureau\webSemantique"
```

### 2️⃣ **Télécharger Apache Jena Fuseki**

```powershell
# Télécharger depuis https://jena.apache.org/download/index.cgi
# Extraire le fichier
# Supposons que fuseki-server.jar soit dans: C:\apache-jena-fuseki-4.x.x
```

### 3️⃣ **Configuration Backend**

```powershell
# Naviguer vers le dossier backend
cd backend

# Créer un environnement virtuel Python
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# OPTIONNEL: Télécharger le modèle français de SpaCy
python -m spacy download fr_core_news_md
```

### 4️⃣ **Configuration Frontend**

```powershell
# Retourner au répertoire racine
cd ..

# Naviguer vers frontend
cd frontend

# Installer les dépendances Node
npm install
```

### 5️⃣ **Charger l'ontologie dans Fuseki**

Avant de démarrer l'application, vous devez charger l'ontologie RDF dans Fuseki.

**Option A: Via interface Fuseki UI**

1. Démarrer Fuseki (voir section Exécution)
2. Accéder à `http://localhost:3030`
3. Cliquer sur "manage datasets"
4. Sélectionner le dataset `eco-tourism`
5. Uploader le fichier `eco-toursime.rdf`

**Option B: Via ligne de commande**

```powershell
cd "C:\apache-jena-fuseki-4.x.x"
.\bin\tdbloader --loc=databases\eco-tourism "c:\Users\abous\OneDrive\Bureau\webSemantique\eco-toursime.rdf"
```

## ⚙️ Configuration

### Backend Configuration (`.env`)

Créer un fichier `.env` dans `backend/`:

```env
# Endpoint Fuseki
FUSEKI_ENDPOINT=http://localhost:3030/waste_management/sparql

# Google Gemini API Key (optionnel)
GEMINI_API_KEY=your-api-key-here

# Utiliser Gemini (true) ou SpaCy (false)
USE_GEMINI=false

# Ports et URLs
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Variables d'environnement

```powershell
# Windows PowerShell
$env:FUSEKI_ENDPOINT="http://localhost:3030/waste_management/sparql"
$env:USE_GEMINI="false"
$env:BACKEND_PORT="8000"
```

## 🏃 Exécution

Ouvrir **3 terminaux PowerShell** distincts:

### **Terminal 1️⃣: Démarrer Fuseki**

```powershell
cd "C:\apache-jena-fuseki-4.x.x"

# Démarrer le serveur
.\fuseki-server.bat --update --mem /eco-tourism

# Ou avec stockage persistant:
# .\fuseki-server.bat --update --loc=databases\eco-tourism /eco-tourism
```

✅ Fuseki démarre sur: `http://localhost:3030`

### Terminal 2️⃣: **Démarrer le Backend**

```powershell
cd "c:\Users\abous\OneDrive\Bureau\webSemantique\backend"

# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Lancer l'application
python main.py
```

✅ Backend démarre sur: `http://localhost:8000`

API Docs: `http://localhost:8000/docs` (Swagger UI)

### Terminal 3️⃣: **Démarrer le Frontend**

```powershell
cd "c:\Users\abous\OneDrive\Bureau\webSemantique\frontend"

# Démarrer le serveur de développement
npm run dev
```

✅ Frontend démarre sur: `http://localhost:3000`

## 🎯 Utilisation

### Accès à l'Application

Ouvrir le navigateur: **`http://localhost:3000`**

### 🔍 **Onglet Recherche**

Poser des questions en français:
- ✅ "Quels sont les points de collecte à Paris?"
- ✅ "Liste tous les types de déchets"
- ✅ "Quels déchets sont acceptés?"
- ✅ "Quelles sont toutes les villes?"

### 📍 **Onglet Points de Collecte**

- Voir tous les points de collecte
- Filtrer par ville
- Consulter horaires, adresses, coordonnées GPS

### 👥 **Onglet Communauté**

- Consulter les badges disponibles
- Voir les activités en cours
- Ajouter une contribution
- Participer aux défis

### 📊 **Onglet Statistiques**

- Vue d'ensemble des métriques
- Graphiques par ville
- Impact environnemental estimé
- Timeline des activités

### 🏠 **Tableau de Bord**

- Résumé des statistiques
- Caractéristiques principales
- Activités récentes

## 📁 Structure du Projet

```
webSemantique/
│
├── waste-management.rdf          # Ontologie RDF
├── eco-toursime.rdf              # Ontologie existante
│
├── backend/                      # API FastAPI
│   ├── venv/                     # Environnement virtuel Python
│   ├── services/
│   │   ├── __init__.py
│   │   ├── fuseki_client.py      # Client SPARQL
│   │   └── nl_to_sparql.py       # Conversion NL→SPARQL
│   ├── main.py                   # Application principale
│   ├── config.py                 # Configuration
│   ├── example_queries.py        # Requêtes d'exemple
│   ├── requirements.txt          # Dépendances Python
│   ├── .env                      # Variables d'environnement
│   └── .env.example              # Template .env
│
├── frontend/                     # Application React
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx        # Navigation
│   │   │   ├── Header.css
│   │   │   ├── Dashboard.jsx     # Accueil
│   │   │   ├── Dashboard.css
│   │   │   ├── QueryInterface.jsx # Recherche NL
│   │   │   ├── QueryInterface.css
│   │   │   ├── CollectionPoints.jsx # Points de collecte
│   │   │   ├── CollectionPoints.css
│   │   │   ├── Community.jsx     # Engagement
│   │   │   ├── Community.css
│   │   │   ├── Statistics.jsx    # Analytiques
│   │   │   ├── Statistics.css
│   │   ├── App.jsx               # Composant racine
│   │   ├── App.css
│   │   ├── main.jsx              # Point d'entrée
│   │   └── index.css             # Styles globaux
│   ├── index.html                # HTML template
│   ├── vite.config.js            # Configuration Vite
│   ├── package.json              # Dépendances Node
│   └── node_modules/             # Packages npm
│
└── README.md                     # Ce fichier
```

## 🔧 Dépannage

### ❌ Erreur: "Cannot connect to Fuseki"

**Solution:**
```powershell
# 1. Vérifier que Fuseki est lancé
curl http://localhost:3030

# 2. Vérifier le FUSEKI_ENDPOINT dans .env
# Défaut: http://localhost:3030/waste_management/sparql

# 3. Vérifier que le dataset existe
# Via UI: http://localhost:3030
```

### ❌ Erreur: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ Erreur: "npm: command not found"

**Solution:**
```powershell
# Réinstaller Node.js depuis https://nodejs.org/
# Fermer et réouvrir PowerShell après installation
```

### ❌ Port déjà utilisé

**Solution - Port 8000 (Backend):**
```powershell
# Changer dans .env
BACKEND_PORT=8001
```

**Solution - Port 3000 (Frontend):**
```powershell
cd frontend
npm run dev -- --port 3001
```

**Solution - Port 3030 (Fuseki):**
```powershell
.\fuseki-server.bat --port=3031 --update --mem /waste_management
# Mettre à jour FUSEKI_ENDPOINT dans .env
```

### ❌ Dataset non chargé dans Fuseki

**Solution:**
```powershell
# 1. Vérifier l'existence du dataset
# Via http://localhost:3030

# 2. Créer un nouveau dataset
# Aller à http://localhost:3030
# New dataset → waste_management

# 3. Charger l'ontologie
# Via UI ou tdbloader (voir section Installation)
```

### ❌ CORS errors

**Solution:**
```powershell
# 1. Vérifier que backend tourne sur 8000
# 2. Vérifier que frontend appelle http://localhost:8000
# 3. Vérifier CORS_ORIGINS dans backend/config.py
```

## 📝 Requêtes SPARQL Exemple

### Tous les points de collecte

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>

SELECT ?point ?nom ?adresse ?horaires
WHERE {
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:horaires ?horaires .
}
```

### Points de collecte à Paris

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>

SELECT ?point ?nom ?adresse
WHERE {
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:localiseDans ?ville .
  ?ville wm:nom "Paris" .
}
```

### Types de déchets acceptés

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>

SELECT DISTINCT ?pointNom ?typeNom
WHERE {
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?pointNom .
  ?point wm:accepte ?type .
  ?type wm:nom ?typeNom .
}
```

## 🚀 Prochaines Étapes

### Améliorations Futures
- [ ] Authentification utilisateur
- [ ] Dashboard admin
- [ ] API de prédiction (ML)
- [ ] Notifications en temps réel
- [ ] Application mobile React Native
- [ ] Intégration cartes Google Maps
- [ ] Export de rapports (PDF/CSV)
- [ ] Système de vote/notation
- [ ] Chat communautaire
- [ ] Gamification avancée

### Déploiement
- Containerisation Docker
- Deployment sur AWS/Azure/GCP
- CI/CD avec GitHub Actions
- Base de données PostgreSQL
- Cache Redis

## 📄 Licence

Ce projet est fourni à des fins éducatives et communautaires.

## 🤝 Support

Pour toute question ou problème:

1. Vérifier la section [Dépannage](#dépannage)
2. Consulter les logs:
   - Frontend: Console du navigateur (F12)
   - Backend: Terminal de démarrage
   - Fuseki: http://localhost:3030/logs
3. Vérifier les ports (3000, 8000, 3030)
4. Vérifier les fichiers `.env`

## 🎉 Prêt à démarrer!

```bash
# Terminal 1: Fuseki
.\fuseki-server.bat --update --mem /waste_management

# Terminal 2: Backend
cd backend && .\venv\Scripts\Activate.ps1 && python main.py

# Terminal 3: Frontend
cd frontend && npm run dev
```

Votre plateforme sera en ligne sur **`http://localhost:3000`** ! 🌍✨
