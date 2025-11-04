# 🚀 Comment Lancer EcoTravel Platform

## ⚡ Démarrage Ultra-Rapide (2 minutes)

### Étape 1: Ouvrez 3 Terminaux PowerShell

**Terminal 1 - Fuseki (SPARQL Database)**
```powershell
# Si vous avez Apache Jena Fuseki installé:
cd C:\apache-jena-fuseki
.\fuseki-server.bat --update --mem /eco-tourism

# Résultat attendu: "Fuseki Server running on http://localhost:3030"
```

**Terminal 2 - Backend (API)**
```powershell
cd c:\Users\abous\OneDrive\Bureau\webSemantique\backend

# Activer environnement Python
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installer dépendances (première fois seulement)
pip install -r requirements.txt

# Lancer le serveur
python main.py

# Résultat attendu: "Uvicorn running on http://127.0.0.1:8000"
```

**Terminal 3 - Frontend (Interface Web)**
```powershell
cd c:\Users\abous\OneDrive\Bureau\webSemantique\frontend

# Installer dépendances (première fois seulement)
npm install

# Lancer l'interface
npm run dev

# Résultat attendu: "Local:   http://localhost:3000/"
```

### Étape 2: Accédez à l'Application
```
Ouvrez votre navigateur: http://localhost:3000
```

---

## ✅ Vérifier que Tout Fonctionne

| Service | URL | Résultat Attendu |
|---------|-----|------------------|
| **Fuseki** | http://localhost:3030 | Page noire avec menu |
| **API** | http://localhost:8000/health | `{"status":"healthy"}` |
| **Docs API** | http://localhost:8000/docs | Page interactive |
| **Frontend** | http://localhost:3000 | Application web |

---

## 🆘 Problèmes Courants

### ❌ "Python not found"
```powershell
# Vérifier si Python est installé
python --version

# Si erreur: télécharger https://www.python.org/downloads/
# ✅ Cocher "Add Python to PATH" pendant l'installation
```

### ❌ "npm command not found"
```powershell
# Vérifier si Node.js est installé
node --version

# Si erreur: télécharger https://nodejs.org/
```

### ❌ "Fuseki not found"
```powershell
# Télécharger Apache Jena Fuseki
# https://jena.apache.org/download/index.cgi

# Extraire dans: C:\apache-jena-fuseki

# Ou installer via Chocolatey:
choco install apache-jena-fuseki
```

### ❌ Port déjà utilisé (3000, 8000, ou 3030)
```powershell
# Trouver le processus
netstat -ano | findstr :3000

# Tuer le processus
taskkill /PID <PID> /F

# Ou utiliser des ports différents dans:
# - Backend: config.py → PORT = 8001
# - Frontend: vite.config.js → port: 3001
```

### ❌ "Module not found" (Backend)
```powershell
# Vérifier que venv est activé (voir "(venv)" dans le prompt)
cd backend
.\venv\Scripts\Activate.ps1

# Réinstaller:
pip install --upgrade -r requirements.txt
```

### ❌ "npm ERR" (Frontend)
```powershell
cd frontend

# Nettoyer et réinstaller
npm cache clean --force
rmdir node_modules -r -force
rm package-lock.json
npm install
npm run dev
```

---

## 🎯 Tests Rapides (Une Fois Lancé)

### Test 1: Vérifier API
```powershell
curl http://localhost:8000/health
```

Résultat attendu:
```json
{"status":"healthy"}
```

### Test 2: Récupérer Profils
```powershell
curl http://localhost:8000/recommendation/profiles
```

### Test 3: Générer Recommandation
```powershell
curl "http://localhost:8000/recommendation/generate?profile=Adventure&destination=Maroc&budget=2000&days=5"
```

### Test 4: Calculer Carbone
```powershell
curl "http://localhost:8000/recommendation/carbon-calculator?transport_type=avion&distance_km=1000"
```

---

## 📊 Structure de l'Application

```
webSemantique/
├── backend/                 # API FastAPI
│   ├── main.py             # Point d'entrée
│   ├── config.py           # Configuration
│   ├── requirements.txt     # Dépendances Python
│   └── services/           # Services (RecommendationEngine, etc)
│
├── frontend/               # Interface React
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── App.jsx         # App principal
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Dépendances npm
│   └── vite.config.js      # Config Vite
│
├── eco-toursime.rdf        # Ontologie RDF
├── start-all.ps1           # Script lancement automatisé
└── RUN.md                  # Ce fichier
```

---

## 🔄 Lancement Automatisé (Optionnel)

Si vous avez créé `start-all.ps1`, exécutez simplement:

```powershell
cd c:\Users\abous\OneDrive\Bureau\webSemantique
.\start-all.ps1
```

Cela lancera les 3 terminaux automatiquement.

---

## 📚 Fichiers de Documentation

- **README.md** - Vue d'ensemble du projet
- **API_DOCUMENTATION.md** - Documentation des endpoints
- **QUICK_START.md** - Guide rapide
- **CONFIGURATION_AVANCEE.md** - Configuration avancée
- **ONTOLOGY_DOCUMENTATION.md** - Documentation de l'ontologie RDF

---

## 🎉 Résumé

1. ✅ Ouvrir 3 terminaux PowerShell
2. ✅ Terminal 1: `cd C:\apache-jena-fuseki && .\fuseki-server.bat --update --mem /eco-tourism`
3. ✅ Terminal 2: `cd backend && python -m venv venv && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt && python main.py`
4. ✅ Terminal 3: `cd frontend && npm install && npm run dev`
5. ✅ Accéder à: http://localhost:3000

**Voilà! L'application est lancée! 🚀**

---

## 📞 Besoin d'Aide?

- Vérifier que Python 3.8+ est installé
- Vérifier que Node.js 16+ est installé
- Vérifier que Fuseki est téléchargé
- Voir les "Problèmes Courants" ci-dessus
- Consulter les fichiers de documentation

Bon développement! 🌟
