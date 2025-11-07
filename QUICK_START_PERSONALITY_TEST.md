# 🚀 Quick Start - Test de Personnalité

## Lancer l'Application

### 1. Démarrer Fuseki (si pas déjà lancé)
```powershell
# Assurez-vous que Fuseki tourne sur localhost:3030
```

### 2. Démarrer le Backend
```powershell
cd backend
python main.py
```

**Attendez de voir:**
```
✅ Gemini API configured successfully
✅ Successfully connected to Fuseki!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Démarrer le Frontend
```powershell
cd frontend
npm run dev
```

**Ouvrez:** http://localhost:3000

## Utilisation

1. **Cliquez sur "Test Personnalité"** dans le menu
2. **Répondez aux 7 questions** (une par une)
3. **Cliquez sur "Générer mon Package"**
4. **Admirez votre package personnalisé!** 🎉

## Ce qui se passe en coulisses

```
Vos Réponses 
    ↓
Fuseki: Récupère toutes vos destinations
    ↓
Gemini AI: Analyse + Recommande parmi VOS destinations
    ↓
Fuseki: Récupère les hébergements liés
    ↓
Package complet avec VOS vraies données!
```

## Tester l'API Directement

### Test rapide avec curl:
```powershell
# 1. Voir les questions
curl http://localhost:8000/personality-test/questions

# 2. Générer un package exemple
curl http://localhost:8000/personality-test/sample-package?personality_type=adventure

# 3. Générer un vrai package
curl -X POST http://localhost:8000/personality-test/generate-package `
  -H "Content-Type: application/json" `
  -d '{
    "answers": {
      "1": "adventure",
      "2": "very_high",
      "3": "eco_lodge",
      "4": "medium",
      "5": "moderate",
      "6": "train",
      "7": "authentic"
    }
  }'
```

## Vérifier les Logs

**Backend doit afficher:**
```
📍 Récupération des destinations depuis Fuseki...
✅ Trouvé X destinations
🧠 Analyse du profil avec Gemini AI...
✅ Profil généré: [Type de profil]
🏨 Récupération des hébergements depuis Fuseki...
✅ Trouvé Y hébergements
📦 Génération du package de voyage personnalisé...
✅ Package généré avec Z destinations
```

## Troubleshooting

### ❌ "Gemini API Key not found"
→ Vérifiez que `backend/.env` contient:
```
GEMINI_API_KEY=AIzaSyAvMIn3rIX1eaTgSuOoejjLI4vf5d909GM
```

### ❌ "Erreur récupération destinations"
→ Vérifiez que Fuseki tourne sur `localhost:3030`
→ Le système utilisera des données mock en fallback

### ❌ Frontend ne charge pas
→ Vérifiez que `npm install` a été fait
→ Backend doit tourner sur port 8000

## 🎉 Succès!

Si vous voyez un package avec:
- ✅ Destinations de votre base de données
- ✅ Hébergements avec certifications
- ✅ Itinéraire jour par jour
- ✅ Coûts détaillés
- ✅ Score écologique

**C'est parfait!** Le système fonctionne et utilise vos vraies données. 🚀
