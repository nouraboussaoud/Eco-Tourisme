# 🔧 Guide de Résolution des Erreurs 500

## 🔴 Problème Actuel

Vous avez des erreurs 500 sur tous les endpoints :
```
INFO: 127.0.0.1:63099 - "GET /destinations HTTP/1.1" 500 Internal Server Error
INFO: 127.0.0.1:63100 - "GET /activites HTTP/1.1" 500 Internal Server Error
```

---

## 🎯 Solutions par Ordre de Priorité

### **Solution 1 : Utiliser le Mock Client (RAPIDE)**

Le mock client fonctionne sans Fuseki. C'est la solution la plus simple pour tester.

#### Étapes :
1. **Arrêtez le backend** (Ctrl+C)

2. **Vérifiez que main.py utilise le Mock** :
   ```python
   # Dans backend/main.py ligne 30-39
   # Devrait dire :
   print("🔧 Using Mock Fuseki Client with sample eco-tourism data")
   from services.mock_fuseki_client import MockFusekiClient
   fuseki_client = MockFusekiClient()
   ```

3. **Relancez le backend** :
   ```powershell
   cd C:\Users\ACHREF\Eco-Tourisme\backend
   .\venv\Scripts\Activate.ps1
   python main.py
   ```

4. **Testez dans un navigateur** :
   - http://localhost:8000/health
   - http://localhost:8000/destinations
   - http://localhost:8000/activites

5. **Si ça marche** → Allez sur http://localhost:3000 ✅

6. **Si erreurs 500 persistent** → Regardez les logs détaillés dans le terminal backend

---

### **Solution 2 : Diagnostic Complet**

Si le mock ne marche toujours pas, lancez le script de diagnostic :

```powershell
cd C:\Users\ACHREF\Eco-Tourisme\backend
.\venv\Scripts\Activate.ps1
python test_connection.py
```

Ce script va :
- ✅ Vérifier si Fuseki tourne
- ✅ Tester la connexion SPARQL
- ✅ Lister les classes de votre ontologie
- ✅ Chercher des destinations dans vos données

---

### **Solution 3 : Connecter Fuseki RÉEL**

#### A. Démarrer Fuseki
```powershell
# Terminal 1
cd C:\apache-jena-fuseki-5.6.0
.\fuseki-server.bat
```

Attendez de voir :
```
Started 2025-11-06 ...
```

#### B. Créer/Vérifier le Dataset

1. Ouvrir navigateur : http://localhost:3030
2. Si vous voyez "tourisme-eco-2" → OK ✅
3. Si pas de dataset :
   - Cliquer "Manage datasets" → "New dataset"
   - Name: `tourisme-eco-2`
   - Type: "Persistent (TDB2)"
   - Create

#### C. Uploader votre Ontologie RDF

1. Cliquer sur votre dataset "tourisme-eco-2"
2. Onglet "**upload data**"
3. Cliquer "select files..."
4. Choisir : `C:\Users\ACHREF\Eco-Tourisme\eco-toursime.rdf`
5. Upload

#### D. Vérifier les données

1. Onglet "**query**"
2. Requête de test :
   ```sparql
   SELECT * WHERE { ?s ?p ?o } LIMIT 10
   ```
3. Execute → Devrait afficher vos triplets ✅

#### E. Redémarrer le Backend

```powershell
cd C:\Users\ACHREF\Eco-Tourisme\backend
.\venv\Scripts\Activate.ps1
python main.py
```

Vous devriez voir :
```
🔧 Connecting to Real Fuseki Server at /tourisme-eco-2
✅ Successfully connected to Fuseki!
```

---

## 📊 Vérifications Rapides

### Test 1 : Backend Health
```bash
curl http://localhost:8000/health
```

Attendu :
```json
{"status": "healthy"}
```

### Test 2 : Destinations
```bash
curl http://localhost:8000/destinations
```

Attendu :
```json
{
  "destinations": [...],
  "count": 5
}
```

### Test 3 : Frontend
Ouvrir : http://localhost:3000

Si vous voyez l'interface → ✅

---

## 🐛 Debugging Avancé

### Voir les logs détaillés du backend

J'ai ajouté des logs détaillés. Quand vous appelez `/destinations`, vous verrez :

```
🔍 Destinations - Question: Quelles sont les destinations éco-responsables?
🔍 Destinations - SPARQL: PREFIX eco: ...
🔍 Destinations - JSON keys: dict_keys(['head', 'results'])
✅ Destinations - Found 5 results
```

Si erreur :
```
❌ Erreur destinations: [détails de l'erreur]
```

### Erreurs Communes

#### Erreur : "Connection refused"
→ Fuseki n'est pas démarré
→ Solution : `.\fuseki-server.bat`

#### Erreur : "Dataset not found"
→ Le dataset n'existe pas dans Fuseki
→ Solution : Créer le dataset dans l'interface web

#### Erreur : "No results"
→ Le dataset est vide
→ Solution : Uploader le fichier RDF

#### Erreur : "Module not found"
→ Dépendances manquantes
→ Solution : `python -m pip install -r requirements.txt`

---

## 🎬 Scénario Complet de Test

### Étape 1 : Backend seul (Mock)
```powershell
cd C:\Users\ACHREF\Eco-Tourisme\backend
.\venv\Scripts\Activate.ps1
python main.py
```

Ouvrir navigateur :
- http://localhost:8000/docs (Swagger UI)
- Tester endpoint `/destinations` → GET → Execute

### Étape 2 : Avec Frontend
```powershell
# Terminal 2
cd C:\Users\ACHREF\Eco-Tourisme\frontend
npm run dev
```

Ouvrir : http://localhost:3000

### Étape 3 : Avec Fuseki
```powershell
# Terminal 1
cd C:\apache-jena-fuseki-5.6.0
.\fuseki-server.bat

# Terminal 2
cd C:\Users\ACHREF\Eco-Tourisme\backend
.\venv\Scripts\Activate.ps1
python main.py

# Terminal 3
cd C:\Users\ACHREF\Eco-Tourisme\frontend
npm run dev
```

---

## 📞 Aide Urgente

Si toujours des erreurs 500 :

1. **Copiez les logs complets** du terminal backend
2. **Prenez une capture** des erreurs dans le terminal
3. **Testez** : `curl http://localhost:8000/destinations`
4. **Partagez** le résultat

Les nouveaux logs détaillés vont nous dire exactement où ça casse !

---

## ✅ Checklist Finale

- [ ] Backend démarre sans erreur
- [ ] Message "Using Mock Fuseki Client" ou "Successfully connected"
- [ ] http://localhost:8000/health → `{"status": "healthy"}`
- [ ] http://localhost:8000/destinations → Données JSON
- [ ] http://localhost:3000 → Interface chargée
- [ ] Onglet "Recherche" fonctionne
- [ ] Onglet "CRUD" fonctionne

---

**Prochaine étape** : Relancez le backend et partagez-moi les logs complets !
