# 🔴 RÉSOUDRE LES ERREURS 500

## 🎯 Diagnostic Rapide

Vous avez ces erreurs :
```
INFO: 127.0.0.1:63099 - "GET /destinations HTTP/1.1" 500 Internal Server Error
INFO: 127.0.0.1:63100 - "GET /activites HTTP/1.1" 500 Internal Server Error
```

---

## ✅ SOLUTION IMMÉDIATE (2 minutes)

### **Étape 1 : Arrêter tout**
```powershell
# Dans chaque terminal, faire : Ctrl+C
```

### **Étape 2 : Relancer le backend avec debug**
```powershell
cd C:\Users\ACHREF\Eco-Tourisme
.\start-backend-debug.ps1
```

### **Étape 3 : Regarder les logs**

Vous allez voir des messages comme :
```
🔍 Destinations - Question: Quelles sont les destinations éco-responsables?
🔍 Destinations - SPARQL: PREFIX eco: ...
✅ Destinations - Found 5 results
```

**OU**

```
❌ Erreur destinations: [message d'erreur détaillé]
```

### **Étape 4 : Tester dans le navigateur**

Ouvrir : **http://localhost:8000/docs**

1. Scroll vers `/destinations`
2. Cliquer "Try it out"
3. Cliquer "Execute"
4. Regarder la réponse

**Si ça marche** → ✅ Passez à l'étape 5

**Si erreur** → ⚠️ Copiez le message d'erreur complet

### **Étape 5 : Lancer le frontend**

Dans un **NOUVEAU** terminal :
```powershell
cd C:\Users\ACHREF\Eco-Tourisme\frontend
npm run dev
```

Ouvrir : **http://localhost:3000**

---

## 🔍 Causes Possibles

### **Cause 1 : Mock Client a un problème**

**Symptôme :** Backend dit "Using Mock Fuseki Client" mais erreurs 500

**Solution :** J'ai ajouté des logs détaillés dans le code. Relancez et regardez les logs.

---

### **Cause 2 : Fuseki ne répond pas**

**Symptôme :** Backend essaie de se connecter à Fuseki mais timeout

**Solution :**
```powershell
# Terminal 1
cd C:\apache-jena-fuseki-5.6.0
.\fuseki-server.bat

# Attendre "Started ..."
# Puis relancer le backend
```

---

### **Cause 3 : Dataset vide ou manquant**

**Symptôme :** "Successfully connected" mais 0 résultats

**Solution :**
1. Ouvrir http://localhost:3030
2. Cliquer sur votre dataset
3. Onglet "upload data"
4. Uploader `eco-toursime.rdf`

---

### **Cause 4 : Erreur de parsing**

**Symptôme :** Erreur dans `parse_results()`

**Solution :** Les logs détaillés vont montrer exactement quelle ligne cause le problème.

---

## 📋 Checklist Complète

### Avant de démarrer :

- [ ] Python venv activé
- [ ] `pip show fastapi` fonctionne
- [ ] Fichier `.env` existe dans `backend/`
- [ ] Port 8000 est libre

### Pour tester avec Mock :

- [ ] Backend démarre
- [ ] Message "Using Mock Fuseki Client"
- [ ] `curl http://localhost:8000/health` → OK
- [ ] `curl http://localhost:8000/destinations` → JSON

### Pour tester avec Fuseki :

- [ ] Fuseki démarre (port 3030)
- [ ] Dataset `/tourisme-eco-2` existe
- [ ] Données RDF uploadées
- [ ] Backend dit "Successfully connected"
- [ ] Requête de test dans Fuseki UI → résultats

---

## 🆘 Si rien ne marche

### Collectez ces informations :

1. **Logs backend complets** (tout le terminal)

2. **Test manuel** :
   ```powershell
   curl http://localhost:8000/health
   ```
   → Copiez la réponse

3. **Test destinations** :
   ```powershell
   curl http://localhost:8000/destinations
   ```
   → Copiez la réponse

4. **Version Python** :
   ```powershell
   python --version
   ```

5. **Liste des packages** :
   ```powershell
   pip list | findstr "fastapi\|uvicorn\|pydantic"
   ```

---

## 🎯 Test Final Simple

```powershell
# 1. Backend
cd C:\Users\ACHREF\Eco-Tourisme\backend
.\venv\Scripts\Activate.ps1
python main.py

# Attendez "Application startup complete"

# 2. Nouveau terminal - Test
curl http://localhost:8000/destinations

# Résultat attendu :
# {"destinations": [...], "count": 5}
```

**Si ça marche** → ✅ Le problème est résolu !

**Si erreur** → Copiez TOUT le message d'erreur

---

## 💡 Astuce Pro

Utilisez Swagger UI pour tester facilement :

1. Ouvrir : http://localhost:8000/docs
2. Tous les endpoints sont listés
3. Cliquer "Try it out" → "Execute"
4. Voir la réponse directement

C'est plus facile que curl ! 😊

---

**Maintenant** : Lancez `.\start-backend-debug.ps1` et envoyez-moi les logs ! 🚀
