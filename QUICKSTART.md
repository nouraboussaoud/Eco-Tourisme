# 🚀 QUICK START - Démarrage Rapide

## ⚡ 5 minutes pour démarrer

### Prérequis Installer
- ✅ Python 3.9+
- ✅ Node.js 18+
- ✅ Apache Jena Fuseki (téléchargé et extrait)

### Étape 1: Installer les dépendances (2 min)

```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique"

# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
npm install
cd ..
```

### Étape 2: Configurer (1 min)

```powershell
# Éditer backend/.env
notepad backend\.env
```

Contenu minimum:
```
FUSEKI_ENDPOINT=http://localhost:3030/waste_management/sparql
USE_GEMINI=false
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Étape 3: Démarrer les services (1 min)

**Option A: Script automatisé**
```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique"
.\start-all.ps1
```

**Option B: 3 terminaux manuels**

Terminal 1:
```powershell
cd "C:\apache-jena-fuseki-4.10.0"
.\fuseki-server.bat --update --mem /waste_management
```

Terminal 2:
```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique\backend"
.\venv\Scripts\Activate.ps1
python main.py
```

Terminal 3:
```powershell
cd "C:\Users\abous\OneDrive\Bureau\webSemantique\frontend"
npm run dev
```

### Étape 4: Vérifier (1 min)

```powershell
# Terminal 4: Test des endpoints
curl http://localhost:8000/health
curl http://localhost:3000
curl http://localhost:3030
```

## 📱 Accès à l'Application

- **Interface:** http://localhost:3000
- **API:** http://localhost:8000 (docs: http://localhost:8000/docs)
- **Fuseki:** http://localhost:3030

## 🎯 Premiers Pas

### 1️⃣ Charger l'ontologie dans Fuseki

Via http://localhost:3030:
1. "Manage datasets" → "waste_management"
2. Upload "waste-management.rdf"

### 2️⃣ Tester la recherche (Onglet "Recherche")

Poser une question:
```
"Quels sont les points de collecte?"
```

### 3️⃣ Explorer les données

- 📍 Points de collecte (avec filtres)
- 👥 Communauté (badges & activités)
- 📊 Statistiques (graphiques & analytiques)

## 🔧 Troubleshooting Express

| Problème | Solution |
|----------|----------|
| `Port 8000 déjà utilisé` | Changer `BACKEND_PORT` dans .env |
| `npm not found` | Réinstaller Node.js |
| `Python venv error` | Recréer: `python -m venv venv` |
| `Fuseki ne charge pas` | Via http://localhost:3030 upload le RDF |
| `CORS error` | Vérifier backend sur 8000 et frontend sur 3000 |

## 📚 Documentation Complète

- **README.md** - Vue d'ensemble complète
- **INSTALLATION.md** - Installation détaillée
- **ONTOLOGY_DOCUMENTATION.md** - Ontologie RDF

## ✨ Fonctionnalités Principales

- 🤖 **Recherche IA** - Langage naturel → SPARQL
- 🗺️ **Localisation** - Points avec GPS
- 👥 **Engagement** - Badges & récompenses
- 📊 **Analytics** - Statistiques en temps réel

## 🎓 Exemples de Requêtes

```
"Quels sont les points de collecte à Paris?"
"Liste tous les types de déchets"
"Quels déchets sont acceptés?"
"Quelles sont les activités?"
"Qui a les badges?"
```

## 🚨 Logs & Debugging

```powershell
# Backend: Terminal 2 (stdout/stderr)
# Frontend: Console du navigateur (F12)
# Fuseki: http://localhost:3030/logs

# Vérifier les services
netstat -ano | findstr ":3000"
netstat -ano | findstr ":8000"
netstat -ano | findstr ":3030"
```

## 💾 Sauvegarder les données

### Optionnel - Utiliser stockage persistant Fuseki

```powershell
# Éditer backend/.env ou au démarrage Fuseki:
cd "C:\apache-jena-fuseki-4.10.0"
mkdir databases\waste_management
.\fuseki-server.bat --update --loc=databases\waste_management /waste_management
```

## 📞 Besoin d'aide?

1. Consulter **README.md**
2. Vérifier **INSTALLATION.md**
3. Lire **ONTOLOGY_DOCUMENTATION.md**
4. Vérifier les logs des services

---

**🎉 C'est tout! Votre plateforme est prête! 🎉**

Accéder à: **http://localhost:3000**
