# 📁 STRUCTURE DU PROJET

## Vue d'ensemble complète

```
webSemantique/
│
├─ 📄 Documentation & Configuration
│  ├─ README.md (12 KB)                      # Documentation principale
│  ├─ QUICKSTART.md (3 KB)                   # Démarrage rapide (5 min)
│  ├─ INSTALLATION.md (15 KB)                # Installation détaillée
│  ├─ ONTOLOGY_DOCUMENTATION.md (12 KB)      # Documentation ontologie
│  ├─ PROJECT_SUMMARY.md (10 KB)             # Résumé du projet
│  ├─ CONFIGURATION_CHECKLIST.md (8 KB)      # Checklist de configuration
│  ├─ PROJECT_STRUCTURE.md                   # Ce fichier
│  └─ .gitignore (recommandé)                # Pour Git
│
├─ 🚀 Scripts de Démarrage
│  ├─ start-all.bat                          # Script Batch (Windows)
│  ├─ start-all.ps1                          # Script PowerShell
│  └─ start-services.sh (optionnel)          # Script Bash (Linux/Mac)
│
├─ 🌐 Ontologie RDF
│  ├─ waste-management.rdf (20 KB)           # ⭐ Ontologie PRINCIPALE
│  └─ eco-toursime.rdf (existant)            # Ontologie écotourisme
│
├─ 🔙 BACKEND (Python/FastAPI)
│  │
│  ├─ venv/                                  # Environnement virtuel Python
│  │  ├─ Scripts/
│  │  │  ├─ Activate.ps1                    # Activation PowerShell
│  │  │  ├─ python.exe
│  │  │  └─ pip.exe
│  │  ├─ Lib/
│  │  │  └─ site-packages/                  # Packages installés
│  │  └─ pyvenv.cfg
│  │
│  ├─ services/                              # Services métier
│  │  ├─ __init__.py
│  │  ├─ fuseki_client.py (300 lignes)      # Client SPARQL
│  │  │  ├─ FusekiClient class
│  │  │  ├─ query() method
│  │  │  ├─ update() method
│  │  │  └─ parse_results() method
│  │  └─ nl_to_sparql.py (400 lignes)       # Conversion NL→SPARQL
│  │     ├─ NLToSparqlConverter class
│  │     ├─ detect_query_type()
│  │     ├─ build_sparql_query()
│  │     ├─ convert_question_to_sparql()
│  │     └─ _convert_with_gemini()
│  │
│  ├─ main.py (400 lignes)                   # Application FastAPI
│  │  ├─ FastAPI app init
│  │  ├─ CORS middleware
│  │  ├─ @app.get("/health")
│  │  ├─ @app.post("/query") - NL→SPARQL
│  │  ├─ @app.post("/sparql") - SPARQL direct
│  │  ├─ @app.post("/contribution")
│  │  ├─ @app.get("/collection-points")
│  │  ├─ @app.get("/waste-types")
│  │  ├─ @app.get("/activities")
│  │  ├─ @app.get("/badges")
│  │  ├─ @app.get("/stats")
│  │  └─ Pydantic models (QueryRequest, QueryResponse)
│  │
│  ├─ config.py (30 lignes)                  # Configuration centralisée
│  │  ├─ FUSEKI_ENDPOINT
│  │  ├─ GEMINI_API_KEY
│  │  ├─ USE_GEMINI
│  │  ├─ CORS_ORIGINS
│  │  └─ ONTOLOGY_NS
│  │
│  ├─ example_queries.py (200 lignes)        # Requêtes SPARQL d'exemple
│  │  ├─ all_collection_points
│  │  ├─ collection_points_in_paris
│  │  ├─ all_waste_types
│  │  ├─ accepted_waste_types
│  │  ├─ all_cities
│  │  ├─ all_activities
│  │  ├─ all_badges
│  │  ├─ user_contributions
│  │  └─ community_stats
│  │
│  ├─ requirements.txt (10 dépendances)      # Dependencies Python
│  │  ├─ fastapi==0.104.1
│  │  ├─ uvicorn==0.24.0
│  │  ├─ pydantic==2.5.0
│  │  ├─ python-dotenv==1.0.0
│  │  ├─ requests==2.31.0
│  │  ├─ spacy==3.7.2
│  │  ├─ google-generativeai==0.3.0
│  │  └─ ...
│  │
│  ├─ .env                                   # ⭐ Variables d'environnement
│  │  ├─ FUSEKI_ENDPOINT
│  │  ├─ GEMINI_API_KEY
│  │  ├─ USE_GEMINI
│  │  ├─ BACKEND_PORT
│  │  └─ FRONTEND_URL
│  │
│  ├─ .env.example (template)                # Template pour .env
│  │
│  └─ __pycache__/                           # Cache Python (auto-généré)
│
├─ 🎨 FRONTEND (React/Vite)
│  │
│  ├─ src/                                   # Code source React
│  │
│  ├─ ├─ components/                         # Composants réutilisables
│  │  │
│  │  ├─ Header.jsx (80 lignes)              # Navigation principale
│  │  │  ├─ Logo + titre
│  │  │  ├─ Nav buttons (5 onglets)
│  │  │  └─ Responsive design
│  │  ├─ Header.css
│  │  │
│  │  ├─ Dashboard.jsx (100 lignes)          # Page d'accueil
│  │  │  ├─ Welcome section
│  │  │  ├─ Stat cards (4 métriques)
│  │  │  ├─ Features grid (4 features)
│  │  │  └─ Recent activities
│  │  ├─ Dashboard.css
│  │  │
│  │  ├─ QueryInterface.jsx (150 lignes)     # Recherche NL→SPARQL
│  │  │  ├─ Input question
│  │  │  ├─ Example questions
│  │  │  ├─ SPARQL query display
│  │  │  ├─ Results table
│  │  │  └─ Error handling
│  │  ├─ QueryInterface.css
│  │  │
│  │  ├─ CollectionPoints.jsx (150 lignes)   # Points de collecte
│  │  │  ├─ Filter par ville
│  │  │  ├─ Grid de points
│  │  │  ├─ Point details panel
│  │  │  ├─ Types acceptés
│  │  │  └─ GPS coordinates
│  │  ├─ CollectionPoints.css
│  │  │
│  │  ├─ Community.jsx (120 lignes)          # Engagement communautaire
│  │  │  ├─ Badges section (grid)
│  │  │  ├─ Activities section (list)
│  │  │  ├─ Badge modal
│  │  │  ├─ Contribution form
│  │  │  └─ Participation buttons
│  │  ├─ Community.css
│  │  │
│  │  └─ Statistics.jsx (150 lignes)         # Analytiques & Rapports
│  │     ├─ Stat cards (4 KPIs)
│  │     ├─ Bar chart (points par ville)
│  │     ├─ Pie chart (types activités)
│  │     ├─ Impact cards (4 impacts)
│  │     ├─ Timeline (activités)
│  │     └─ Impact section
│  │  └─ Statistics.css
│  │
│  ├─ App.jsx (100 lignes)                   # Composant principal
│  │  ├─ State management
│  │  ├─ Data fetching (useEffect)
│  │  ├─ Tab routing
│  │  ├─ Error handling
│  │  ├─ Loading state
│  │  └─ Component rendering
│  │
│  ├─ App.css                                # Styles App
│  │  ├─ Layout main
│  │  ├─ Loading spinner
│  │  └─ Error banner
│  │
│  ├─ main.jsx (15 lignes)                   # Point d'entrée React
│  │  └─ ReactDOM.render(App)
│  │
│  ├─ index.css                              # Styles globaux
│  │  ├─ Reset CSS
│  │  ├─ Fonts
│  │  ├─ Scrollbar style
│  │  └─ Root styling
│  │
│  ├─ index.html (20 lignes)                 # Template HTML
│  │  ├─ Meta tags
│  │  ├─ Font Awesome CDN
│  │  ├─ #root div
│  │  └─ Script src/main.jsx
│  │
│  ├─ vite.config.js                         # Configuration Vite
│  │  ├─ React plugin
│  │  ├─ Dev server (3000)
│  │  ├─ API proxy (/api → :8000)
│  │  └─ Build config
│  │
│  ├─ package.json                           # Dépendances Node
│  │  ├─ Scripts (dev, build)
│  │  ├─ Dependencies (react, axios, etc)
│  │  └─ DevDependencies (vite, eslint)
│  │
│  ├─ package-lock.json                      # Lock file npm
│  │
│  ├─ node_modules/                          # Packages npm (auto-généré)
│  │  ├─ react/
│  │  ├─ vite/
│  │  ├─ axios/
│  │  └─ ... (800+ packages)
│  │
│  └─ .eslintrc.json (optionnel)             # Config linter
│
└─ 📦 Apache Jena Fuseki (Externe)
   │
   └─ C:\apache-jena-fuseki-4.10.0\          # Installation Fuseki
      ├─ fuseki-server.bat                   # Démarrage Windows
      ├─ bin/
      │  ├─ tdbloader.bat                    # RDF loader
      │  ├─ sparql.bat                       # SPARQL query tool
      │  └─ ... autres outils
      ├─ lib/                                # Libraries Java
      │  └─ ... JAR files
      ├─ databases/
      │  └─ waste_management/                # Triplestore persistant
      │     ├─ tdb.lock
      │     └─ ... DB files
      └─ logs/                               # Logs Fuseki

```

## 📊 Statistiques du Projet

### Code
- **Backend:** ~1200 lignes Python
- **Frontend:** ~1300 lignes JSX/CSS
- **Ontologie:** ~500 lignes XML/RDF
- **Documentation:** ~2000 lignes Markdown
- **Total:** ~5000+ lignes

### Fichiers
- **Backend:** 9 fichiers Python
- **Frontend:** 16 fichiers (JSX + CSS)
- **Documentation:** 7 fichiers Markdown
- **Configuration:** 4 fichiers
- **Total:** 36+ fichiers

### Dépendances
- **Python:** 8 packages (+ SpaCy, Gemini optionnels)
- **Node.js:** 50+ packages (incluant dependencies)
- **System:** Fuseki, Python, Node

## 🗂️ Organisation Logique

### Par Responsabilité
```
ONTOLOGIE
├─ waste-management.rdf (données sémantiques)
│
BACKEND
├─ main.py (routes API)
├─ services/ (logique métier)
├─ config.py (configuration)
└─ requirements.txt (dépendances)

FRONTEND
├─ components/ (UI réutilisable)
├─ App.jsx (orchestration)
├─ vite.config.js (build)
└─ package.json (dépendances)

DOCUMENTATION
├─ README.md (vue d'ensemble)
├─ INSTALLATION.md (setup)
├─ ONTOLOGY_DOCUMENTATION.md (schéma)
└─ CONFIGURATION_CHECKLIST.md (validation)
```

### Par Matérialité
```
DONNÉES
└─ waste-management.rdf

API & SERVICES
├─ main.py
└─ services/

UI & UX
└─ src/components/

INFRASTRUCTURE
├─ vite.config.js
└─ fuseki-server

DOCUMENTATION
└─ *.md files
```

## 🔄 Flux de Données

```
UTILISATEUR
    │
    ▼
┌─────────────────┐
│ React Frontend  │
│  - Dashboard    │
│  - Query input  │
│  - Results      │
└────────┬────────┘
         │ HTTP/JSON
         ▼
┌─────────────────┐
│  FastAPI Backend│
│ - NL→SPARQL     │
│ - Validation    │
│ - Orchestration │
└────────┬────────┘
         │ SPARQL
         ▼
┌─────────────────┐
│  Fuseki SPARQL  │
│  - Triplestore  │
│  - Reasoning    │
│  - Query exec   │
└────────┬────────┘
         │ JSON Results
         ▼
┌─────────────────┐
│   RDF Ontology  │
│  - Déchets      │
│  - Points       │
│  - Engagement   │
└─────────────────┘
```

## 🧩 Composants Clés

### Backend
1. **FusekiClient** - Communication SPARQL
2. **NLToSparqlConverter** - Conversion NL
3. **FastAPI Routes** - Endpoints REST
4. **Pydantic Models** - Validation

### Frontend
1. **Header** - Navigation
2. **Dashboard** - Vue d'ensemble
3. **QueryInterface** - Recherche
4. **CollectionPoints** - Localisation
5. **Community** - Engagement
6. **Statistics** - Analytiques

## 📈 Couches d'Application

```
┌─────────────────────────────────┐
│   PRESENTATION LAYER            │
│   React Components (UI)         │
└─────────────────────────────────┘
            │
┌─────────────────────────────────┐
│   APPLICATION LAYER             │
│   FastAPI Routes & Logic        │
└─────────────────────────────────┘
            │
┌─────────────────────────────────┐
│   SERVICE LAYER                 │
│   NL-SPARQL, Fuseki Client      │
└─────────────────────────────────┘
            │
┌─────────────────────────────────┐
│   DATA LAYER                    │
│   SPARQL Triplestore (Fuseki)   │
└─────────────────────────────────┘
            │
┌─────────────────────────────────┐
│   SEMANTIC LAYER                │
│   RDF Ontology (waste-mgmt.rdf) │
└─────────────────────────────────┘
```

## 🚀 Cycle de Vie Requête

```
1. USER INPUT
   Question: "Quels points de collecte à Paris?"
   
2. FRONTEND
   Form.onSubmit → Api.post(/query)
   
3. HTTP REQUEST
   POST http://localhost:8000/query
   Body: {"question": "..."}
   
4. BACKEND PROCESSING
   main.py:/query endpoint
   nl_to_sparql.convert()
   Generate SPARQL query
   
5. FUSEKI QUERY
   fuseki_client.query(sparql)
   POST /waste_management/sparql
   
6. ONTOLOGY REASONING
   RDF matching
   Query execution
   Result generation
   
7. RESPONSE
   JSON results with bindings
   
8. FRONTEND RENDERING
   Parse JSON results
   Display in table/cards
   Show query details
```

---

**Structure Finalisée:** ✅
**Fichiers:** 36+
**Lignes de Code:** 5000+
**Prêt pour Production:** ✅
