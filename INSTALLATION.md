# Guide d'Installation Détaillé - EcoWaste Manager

## 🖥️ Configurations Testées

- ✅ Windows 10/11 (PowerShell)
- ✅ Python 3.9 - 3.11
- ✅ Node.js 18+
- ✅ Apache Jena Fuseki 4.x

## 📋 Étapes Installation Complète

### Étape 1: Télécharger les Prérequis

#### Python
```powershell
# Télécharger Python 3.10+
# https://www.python.org/downloads/

# Vérifier l'installation
python --version
pip --version
```

#### Node.js
```powershell
# Télécharger Node.js 18+
# https://nodejs.org/

# Vérifier l'installation
node --version
npm --version
```

#### Apache Jena Fuseki
```powershell
# Télécharger Fuseki
# https://jena.apache.org/download/index.cgi

# Extraire dans C:\apache-jena-fuseki-4.10.0
# (ou autre version récente)

# Vérifier l'installation
cd "C:\apache-jena-fuseki-4.10.0"
.\fuseki-server.bat --version
```

### Étape 2: Configuration Backend

```powershell
# Naviguer au projet
cd "C:\Users\abous\OneDrive\Bureau\webSemantique"

# Naviguer au backend
cd backend

# Créer environnement virtuel
python -m venv venv

# Activer environnement (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Installer dépendances
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Télécharger modèle SpaCy français (optionnel)
python -m spacy download fr_core_news_md

# Vérifier installation
pip list
```

**Contenu de requirements.txt:**
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0
- python-dotenv==1.0.0
- requests==2.31.0
- spacy==3.7.2
- google-generativeai==0.3.0

### Étape 3: Configuration Frontend

```powershell
# Retourner au répertoire racine
cd ..

# Naviguer au frontend
cd frontend

# Installer dépendances
npm install

# Vérifier installation
npm list

# Build de production (optionnel)
npm run build
```

### Étape 4: Configuration Fuseki

#### Option A: In-Memory (Développement)

```powershell
cd "C:\apache-jena-fuseki-4.10.0"

# Lancer Fuseki en mémoire
.\fuseki-server.bat --update --mem /waste_management

# OU utiliser l'alias
.\fuseki-server.bat --port 3030 --update --mem /waste_management
```

#### Option B: Persistent Storage (Production)

```powershell
cd "C:\apache-jena-fuseki-4.10.0"

# Créer répertoire de base de données
mkdir databases\waste_management

# Lancer avec stockage persistant
.\fuseki-server.bat --update --loc=databases\waste_management /waste_management
```

#### Option C: Chargement du Fichier RDF

**Via Interface Web:**
1. Accéder à http://localhost:3030
2. Aller dans "Manage datasets"
3. Créer dataset "waste_management"
4. Upload "waste-management.rdf"

**Via Command Line:**
```powershell
cd "C:\apache-jena-fuseki-4.10.0"

# Charger le RDF
.\bin\tdbloader --loc=databases\waste_management ^
  "C:\Users\abous\OneDrive\Bureau\webSemantique\waste-management.rdf"
```

### Étape 5: Configuration Variables d'Environnement

#### Backend .env

```powershell
cd backend

# Créer le fichier .env
New-Item -Path ".env" -ItemType "File"

# Éditer avec Notepad
notepad .env
```

**Contenu du fichier .env:**
```
# API Fuseki
FUSEKI_ENDPOINT=http://localhost:3030/waste_management/sparql

# Google Gemini (optionnel)
GEMINI_API_KEY=

# Configuration
USE_GEMINI=false
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

#### Frontend Configuration

```powershell
cd frontend

# Vérifier vite.config.js
# Le proxy est configuré pour rediriger /api vers http://localhost:8000
```

## 🚀 Démarrage

### Méthode 1: Trois Terminaux Séparés

**Terminal 1 - Fuseki:**
```powershell
cd "C:\apache-jena-fuseki-4.10.0"
.\fuseki-server.bat --update --mem /waste_management
```

**Terminal 2 - Backend:**
```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique\backend"
.\venv\Scripts\Activate.ps1
python main.py
```

**Terminal 3 - Frontend:**
```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique\frontend"
npm run dev
```

### Méthode 2: Script Batch

```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique"
.\start-all.bat
```

### Méthode 3: Script PowerShell Interactif

```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique"
.\start-all.ps1
```

## ✅ Vérification de l'Installation

### Vérifier Fuseki

```powershell
# Test dans PowerShell
curl http://localhost:3030

# Réponse attendue:
# Welcome to Jena Fuseki Server
```

### Vérifier Backend

```powershell
# Vérification de santé
curl http://localhost:8000/health

# Réponse attendue:
# {
#   "status": "healthy",
#   "timestamp": "...",
#   "services": {"fuseki": "connected", "nl_converter": "ready"}
# }

# API Documentation
# http://localhost:8000/docs
```

### Vérifier Frontend

```
http://localhost:3000
# Page d'accueil du dashboard
```

## 🔧 Dépannage Avancé

### Problème: Module Python non trouvé

```powershell
# Solution 1: Réactiver l'environnement
cd backend
.\venv\Scripts\Activate.ps1

# Solution 2: Réinstaller les packages
pip install --force-reinstall -r requirements.txt

# Solution 3: Créer un nouvel environnement
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problème: Port 3030 en usage

```powershell
# Trouver le processus utilisant le port
netstat -ano | findstr ":3030"

# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F

# Ou utiliser un autre port
cd "C:\apache-jena-fuseki-4.10.0"
.\fuseki-server.bat --port=3031 --update --mem /waste_management

# Mettre à jour .env
FUSEKI_ENDPOINT=http://localhost:3031/waste_management/sparql
```

### Problème: npm install échoue

```powershell
# Effacer le cache npm
npm cache clean --force

# Réessayer
npm install

# Si problème persiste, réinstaller Node.js
```

### Problème: CORS errors

```powershell
# Vérifier que le backend tourne sur 8000
curl http://localhost:8000

# Vérifier CORS_ORIGINS dans config.py
# Assurer que "http://localhost:3000" y est présent

# Redémarrer le backend pour appliquer les changements
```

### Problème: Fuseki ne charge pas l'ontologie

```powershell
# Vérifier que le fichier existe
Test-Path "C:\Users\abous\OneDrive\Bureau\webSemantique\waste-management.rdf"

# Vérifier que le dataset existe
# Via http://localhost:3030

# Charger manuellement via tdbloader
cd "C:\apache-jena-fuseki-4.10.0"
.\bin\tdbloader --loc=databases\waste_management ^
  "C:\Users\abous\OneDrive\Bureau\webSemantique\waste-management.rdf"

# Redémarrer Fuseki
```

## 📦 Structure Complète

```
C:\Users\abous\OneDrive\Bureau\webSemantique\
│
├── waste-management.rdf                    # Ontologie RDF
├── eco-toursime.rdf                        # Ontologie existante
├── README.md                               # Documentation
├── ONTOLOGY_DOCUMENTATION.md               # Docs ontologie
├── INSTALLATION.md                         # Ce fichier
├── start-all.bat                           # Script démarrage batch
├── start-all.ps1                           # Script démarrage PowerShell
│
├── backend/
│   ├── venv/                               # Environnement virtuel
│   │   ├── Scripts/
│   │   ├── Lib/
│   │   └── pyvenv.cfg
│   ├── services/
│   │   ├── __init__.py
│   │   ├── fuseki_client.py               # Client SPARQL
│   │   └── nl_to_sparql.py                # Conversion NL↔SPARQL
│   ├── main.py                            # Application FastAPI
│   ├── config.py                          # Configuration
│   ├── example_queries.py                 # Exemples SPARQL
│   ├── requirements.txt                   # Dépendances Python
│   ├── .env                               # Variables d'environnement
│   └── .env.example                       # Template .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Header.css
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Dashboard.css
│   │   │   ├── QueryInterface.jsx
│   │   │   ├── QueryInterface.css
│   │   │   ├── CollectionPoints.jsx
│   │   │   ├── CollectionPoints.css
│   │   │   ├── Community.jsx
│   │   │   ├── Community.css
│   │   │   ├── Statistics.jsx
│   │   │   ├── Statistics.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── node_modules/                      # Packages npm
│   ├── index.html                         # Page HTML
│   ├── vite.config.js                     # Configuration Vite
│   ├── package.json                       # Dépendances Node
│   └── package-lock.json                  # Lock file npm
│
└── C:\apache-jena-fuseki-4.10.0\          # Installation Fuseki
    ├── fuseki-server.bat
    ├── bin/
    ├── lib/
    └── databases/
        └── waste_management/              # BD persistante
```

## 🌐 Ports Réseau

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| Fuseki | 3030 | http://localhost:3030 |

## 🔐 Sécurité en Développement

### Backend - CORS

Les origines autorisées:
- http://localhost:3000
- http://127.0.0.1:3000

À modifier dans `config.py` pour la production.

### Frontend - API Calls

Les appels API sont proxifiés via Vite:
- `/api/*` → `http://localhost:8000/*`

## 📝 Fichiers de Log

```powershell
# Backend logs (dans le terminal)
# Fuseki logs (dans le terminal)
# Frontend logs (dans la console du navigateur - F12)

# Accéder aux logs Fuseki via web
# http://localhost:3030/logs
```

## 🚀 Prochaines Étapes Après Installation

1. ✅ Vérifier que tous les services tournent
2. ✅ Charger des données dans l'ontologie
3. ✅ Tester les requêtes SPARQL
4. ✅ Créer des utilisateurs et activités
5. ✅ Explorer le dashboard complet

## 📚 Commandes Utiles

```powershell
# Python/Backend
python --version
pip list
pip show <package-name>
pip freeze > requirements.txt

# Node/Frontend
node --version
npm --version
npm list
npm outdated
npm update

# Processus
Get-Process | findstr python
Get-Process | findstr node
tasklist | findstr java

# Ports
netstat -ano | findstr ":3000"
netstat -ano | findstr ":8000"
netstat -ano | findstr ":3030"
```

## 📞 Support

Pour des problèmes:
1. Consulter le README.md principal
2. Vérifier les ports avec netstat
3. Consulter les logs des services
4. Vérifier les fichiers .env
5. Réinstaller les dépendances si nécessaire

---

**Dernière mise à jour:** 2025-01-04
