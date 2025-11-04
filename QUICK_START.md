# ⚡ Guide Démarrage Rapide

## 🎯 Objectif
Avoir une plateforme EcoTravel complètement fonctionnelle en 15 minutes.

## 📋 Checklist Préalable

- [ ] Python 3.9+ installé (`python --version`)
- [ ] Node.js 18+ installé (`node --version`)
- [ ] Apache Jena Fuseki téléchargé et décompressé
- [ ] Éditeur de code (VS Code recommandé)

## ⏱️ Étapes (15 min)

### 1️⃣ Lancez Fuseki (2 min)

```bash
cd chemin\vers\apache-jena-fuseki

# Windows
fuseki-server --update --mem /waste_management

# Linux/Mac
./fuseki-server --update --mem /waste_management
```

✅ Vous verrez: `[main] INFO  Server (org.apache.jena.fuseki.server.FusekiServer) Started`  
✅ Vérifiez: http://localhost:3030

---

### 2️⃣ Backend (4 min)

```bash
cd backend

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Installation
pip install -r requirements.txt

# Lancement
python main.py
```

✅ Vous verrez: `Uvicorn running on http://127.0.0.1:8000`  
✅ Vérifiez: http://localhost:8000/health

---

### 3️⃣ Frontend (3 min)

```bash
cd frontend

# Installation
npm install

# Lancement
npm run dev
```

✅ Vous verrez: `Local: http://localhost:3000`  
✅ Ouvrez: http://localhost:3000

---

### 4️⃣ Test Rapide (2 min)

1. Allez à http://localhost:3000
2. Cliquez sur onglet "Recommandations"
3. Choisissez profil "Adventure"
4. Entrez destination "Paris"
5. Cliquez "Générer ma recommandation"

✅ Résultat: Voir une recommandation complète avec:
- Score de recommandation
- Activités suggérées
- Hébergement écologique
- Transport optimisé
- Calcul empreinte carbone

---

## 🔧 Commandes Essentielles

### Terminal 1 - Fuseki
```bash
cd apache-jena-fuseki
fuseki-server --update --mem /waste_management
```

### Terminal 2 - Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows
python main.py
```

### Terminal 3 - Frontend
```bash
cd frontend
npm run dev
```

---

## 🌐 URLs de Référence

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interface utilisateur |
| **Backend API** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Fuseki** | http://localhost:3030 | RDF Store |

---

## 🎮 Tests Rapides

### Test 1: Profils Disponibles
```bash
curl http://localhost:8000/recommendation/profiles
```

### Test 2: Calcul CO₂
```bash
curl "http://localhost:8000/recommendation/carbon-calculator?transport_type=Avion&distance_km=1000"
```

### Test 3: Santé de l'app
```bash
curl http://localhost:8000/health
```

---

## 📚 Cas d'Usage Rapides

### Voyageur Adventure 🏔️
```
Profil: Adventure
Destination: Alpes
Budget: 1500€
CO₂ Priority: OUI
Jours: 5
```

### Voyageur Culture 🏛️
```
Profil: Culture
Destination: Paris
Budget: 800€
CO₂ Priority: NON
Jours: 3
```

### Voyageur Famille 👨‍👩‍👧‍👦
```
Profil: Famille
Destination: Provence
Budget: 2000€
CO₂ Priority: NON
Jours: 7
```

---

## 🐛 Si Ça Ne Fonctionne Pas

### ❌ "Cannot connect to Fuseki"
```bash
# Vérifiez Fuseki
curl http://localhost:3030

# Vérifiez .env backend
FUSEKI_ENDPOINT=http://localhost:3030/waste_management/sparql
```

### ❌ "ModuleNotFoundError"
```bash
# Réactivez venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ CORS Error
```bash
# Vérifiez frontend URL
FRONTEND_URL=http://localhost:3000
```

### ❌ Port déjà utilisé
```bash
# Changez le port dans .env ou config.py
BACKEND_PORT=8001  # au lieu de 8000
```

---

## 📊 Exemple Flux Complet

```
1. Utilisateur visite http://localhost:3000
                          ↓
2. Clique "Recommandations"
                          ↓
3. Sélectionne Adventure + Paris + 1000€ + CO₂ priority
                          ↓
4. Backend génère recommandation
                          ↓
5. Requête Fuseki pour activités/hébergements
                          ↓
6. Calcul score matching + empreinte carbone
                          ↓
7. Retour résultat au frontend
                          ↓
8. Affichage Package complet avec raisons
```

---

## 💡 Tips & Tricks

✨ **Tip 1**: Ouvrez 3 terminals en même temps pour voir logs en direct

✨ **Tip 2**: Utilisez http://localhost:8000/docs pour tester API directement

✨ **Tip 3**: Chargez l'ontologie RDF via UI Fuseki pour voir les données

✨ **Tip 4**: Vérifiez browser console (F12) pour erreurs frontend

✨ **Tip 5**: Les recommandations se cachent en cache - actualisez pour nouvelles données

---

## 🚀 Prochaines Étapes

1. ✅ Tout fonctionne? Félicitations! 🎉
2. 📖 Lisez `API_DOCUMENTATION.md` pour détails endpoints
3. 🗺️ Consultez `README.md` pour architecture complète
4. 🔧 Personnalisez ontologie RDF dans `eco-toursime.rdf`
5. 🎨 Modifiez interface frontend dans `frontend/src/components/`

---

## 📞 Support Rapide

**Est-ce que ça fonctionne?**
```
✅ OUI: Allez à http://localhost:3000
❌ NON: Vérifiez que les 3 terminaux ont les logs sans erreur
```

**Port déjà utilisé?**
```
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux
```

**Besoin de réinitialiser?**
```bash
# Arrêtez tout (Ctrl+C dans chaque terminal)
# Redémarrez Fuseki
# Vérifiez .env
# Relancez backend et frontend
```

---

**Prêt à voyager écologiquement? 🌍✈️**
