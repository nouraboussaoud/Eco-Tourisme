# 🎯 GUIDE DE DÉMARRAGE - EcoTravel Platform

## Option 1: Démarrage Automatisé (Recommandé)

### Windows PowerShell
```powershell
cd c:\Users\abous\OneDrive\Bureau\webSemantique
.\start-all.ps1
```

### Windows Command Prompt
```cmd
cd c:\Users\abous\OneDrive\Bureau\webSemantique
start-all.bat
```

Cela lancera automatiquement les 3 services dans des terminaux séparés.

---

## Option 2: Démarrage Manuel (3 Terminaux)

### ✅ PRÉ-REQUIS

Avant de démarrer, installez:

1. **Python 3.8+** - https://www.python.org/downloads/
   - ✅ Cocher "Add Python to PATH" pendant l'installation
   - Vérifier: `python --version`

2. **Node.js 16+** - https://nodejs.org/
   - Vérifier: `node --version` et `npm --version`

3. **Apache Jena Fuseki** - https://jena.apache.org/download/index.cgi
   - Extraire à: `C:\apache-jena-fuseki`
   - Vérifier: `java -version`

---

### Terminal 1️⃣: Fuseki (SPARQL Database)

```powershell
# Naviguer à Fuseki
cd C:\apache-jena-fuseki

# Lancer le serveur
.\fuseki-server.bat --update --mem /eco-tourism

# ✅ Vous verrez:
# [main] INFO ... Fuseki Server running on http://localhost:3030
```

**Accéder à:** http://localhost:3030

---

### Terminal 2️⃣: Backend (API FastAPI)

```powershell
# Naviguer au backend
cd c:\Users\abous\OneDrive\Bureau\webSemantique\backend

# Créer et activer environnement virtuel Python
python -m venv venv
.\venv\Scripts\Activate.ps1

# Vous devriez voir "(venv)" au début du prompt

# Installer dépendances (première fois seulement)
pip install -r requirements.txt

# Lancer le backend
python main.py

# ✅ Vous verrez:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Accéder à:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

---

### Terminal 3️⃣: Frontend (React Web UI)

```powershell
# Naviguer au frontend
cd c:\Users\abous\OneDrive\Bureau\webSemantique\frontend

# Installer dépendances (première fois seulement)
npm install

# Lancer l'interface
npm run dev

# ✅ Vous verrez:
# ➜  Local:   http://localhost:3000/
```

**Accéder à:** http://localhost:3000

---

## 📱 Utilisation

Une fois tout lancé, ouvrez votre navigateur et allez à:

```
http://localhost:3000
```

Vous verrez l'interface EcoTravel avec:
- ✅ Dashboard
- ✅ Recommendations (Recommandations personnalisées)
- ✅ Query Interface (Requêtes SPARQL)
- ✅ Collection Points (Points de collecte)
- ✅ Community (Communauté)
- ✅ Statistics (Statistiques)

---

## ✅ Vérification Rapide

### Test 1: Health Check
```powershell
curl http://localhost:8000/health
```

Résultat attendu:
```json
{"status":"healthy"}
```

### Test 2: Récupérer Profils Voyageurs
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

## 🆘 Dépannage

### ❌ Problème: "Python not found"

**Solution:**
```powershell
# Vérifier
python --version

# Si erreur, installer: https://www.python.org/downloads/
# ✅ Cocher "Add Python to PATH"
```

---

### ❌ Problème: "npm: command not found"

**Solution:**
```powershell
# Vérifier
node --version

# Si erreur, installer: https://nodejs.org/
```

---

### ❌ Problème: "ModuleNotFoundError" (Backend)

**Solution:**
```powershell
cd backend

# Vérifier que venv est activé (voir "(venv)" dans le prompt)
.\venv\Scripts\Activate.ps1

# Réinstaller
pip install --upgrade -r requirements.txt
```

---

### ❌ Problème: "Port already in use"

**Solution:**
```powershell
# Trouver le processus occupant le port
netstat -ano | findstr :3000
netstat -ano | findstr :8000
netstat -ano | findstr :3030

# Tuer le processus
taskkill /PID <PID> /F

# Exemple: taskkill /PID 1234 /F
```

---

### ❌ Problème: Fuseki ne démarre pas

**Solution:**
```powershell
# Vérifier Java
java -version

# Si erreur: installer Java https://www.oracle.com/java/technologies/downloads/

# Vérifier chemin Fuseki
cd C:\apache-jena-fuseki
.\fuseki-server.bat --version

# Si pas de fichier fuseki-server.bat:
# Télécharger depuis https://jena.apache.org/download/index.cgi
```

---

### ❌ Problème: Frontend ne charge pas

**Solution:**
```powershell
cd frontend

# Vérifier npm
npm --version

# Réinstaller
npm cache clean --force
rm node_modules -r -force
rm package-lock.json
npm install
npm run dev
```

---

### ❌ Problème: "Fuseki.PermissionDenied"

**Solution:**
```powershell
# Exécuter PowerShell en administrateur
# Clic droit sur PowerShell > Exécuter en tant qu'administrateur

# Puis lancer: .\start-all.ps1
```

---

## 📊 Architecture

```
Frontend (React)              Backend (FastAPI)          Fuseki (SPARQL)
http://localhost:3000         http://localhost:8000      http://localhost:3030
├─ Recommandations           ├─ /health                 └─ SPARQL Endpoint
├─ Dashboard                 ├─ /recommendation/*
├─ Query Interface           ├─ /sparql
├─ Collection Points         ├─ /query
├─ Community                 └─ /carbon-calculator
└─ Statistics
```

---

## 📚 Documentation

| Fichier | Description |
|---------|-------------|
| **RUN.md** | Ce fichier (comment lancer) |
| **README.md** | Vue d'ensemble du projet |
| **API_DOCUMENTATION.md** | Documentation API détaillée |
| **QUICK_START.md** | Guide rapide |
| **CONFIGURATION_AVANCEE.md** | Configuration avancée |

---

## 🎉 Résumé Rapide

### Première Fois:
```powershell
# 1. Installer: Python, Node.js, Fuseki
# 2. Lancer: .\start-all.ps1
# 3. Accéder: http://localhost:3000
```

### Autres Fois:
```powershell
# Lancer: .\start-all.ps1
# Accéder: http://localhost:3000
```

### Arrêter:
```powershell
# Fermer les 3 terminaux (Ctrl+C dans chaque) 
# Ou fermer les fenêtres
```

---

## 💡 Conseils

- 🔴 **Ne pas fermer les terminaux** - Les services continueront de tourner
- 📝 **Lire les logs** - Utiles pour déboguer
- 🌐 **Accéder à http://localhost:3000** - Interface principale
- 📚 **Consulter http://localhost:8000/docs** - Documentation API interactive
- 🔍 **Utiliser http://localhost:3030** - Interface Fuseki

---

## 🚀 Vous êtes Prêt!

L'application est lancée et prête à être utilisée. Amusez-vous bien! 🎉

Besoin d'aide? Consultez les fichiers de documentation ou les commentaires dans le code.
