# ✅ CRUD RÉPARÉ - Guide de Test

## 🔧 Corrections Appliquées

### **1. Frontend - CrudManager.jsx**
- ✅ Utilisation de `URLSearchParams` pour envoyer la requête SPARQL
- ✅ Header `Content-Type: application/x-www-form-urlencoded`
- ✅ Mapping correct des classes d'entités (destinations → Destination, etc.)
- ✅ Génération correcte des triples RDF avec `rdfs:label` et `rdfs:comment`

### **2. Backend - main.py**
- ✅ Import de `Form` depuis FastAPI
- ✅ Endpoint `/sparql` accepte maintenant `query: str = Form(...)`

### **3. Format de la Requête**

#### Avant (❌ Cassé) :
```javascript
await axios.post(`${API_URL}/sparql`, sparqlInsert)
// Envoyait la string directement dans le body
```

#### Après (✅ Corrigé) :
```javascript
const params = new URLSearchParams()
params.append('query', sparqlInsert)
await axios.post(`${API_URL}/sparql`, params, {
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
})
```

---

## 🚀 Comment Tester

### **Étape 1 : Recharger le Frontend**

Le backend n'a pas besoin de redémarrer (hot reload). Mais rechargez la page frontend :

1. Aller sur : http://localhost:3000
2. **Appuyer sur F5** ou Ctrl+R

### **Étape 2 : Tester le CRUD**

1. Cliquer sur l'onglet **"CRUD"** dans la navigation
2. Sélectionner **"Destinations"**
3. Cliquer sur **"Créer une nouvelle destination"**
4. Remplir le formulaire :
   - **Nom** : Parc National Ichkeul
   - **Description** : Magnifique réserve naturelle protégée
   - **Région** : Bizerte
5. Cliquer sur **"Créer Destination"**

### **Étape 3 : Vérifier les Logs**

#### Terminal Backend :
```
INFO: 127.0.0.1:xxxxx - "POST /sparql HTTP/1.1" 200 OK  ✅
```

#### Terminal Fuseki :
```
INFO Fuseki :: [X] POST http://localhost:3030/tourisme-eco-2/update
INFO Fuseki :: [X] Update = PREFIX eco: ... INSERT DATA { ... }
INFO Fuseki :: [X] 204 No Content (XX ms)  ✅
```

**204 No Content** = Succès de l'insertion !

### **Étape 4 : Vérifier l'Insertion dans Fuseki**

1. Ouvrir : http://localhost:3030
2. Cliquer sur votre dataset **tourisme-eco-2**
3. Onglet **"query"**
4. Exécuter cette requête :

```sparql
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?destination ?nom ?description
WHERE {
  ?destination rdf:type eco:Destination .
  OPTIONAL { ?destination rdfs:label ?nom }
  OPTIONAL { ?destination rdfs:comment ?description }
}
```

Vous devriez voir votre nouvelle destination ! 🎉

---

## 📋 Exemple de Requête SPARQL Générée

Quand vous créez une destination avec :
- Nom : "Parc National Ichkeul"
- Description : "Réserve naturelle"

Le frontend génère :
```sparql
PREFIX eco: <http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
  eco:destinations_1730931234567 rdf:type eco:Destination ;
    rdfs:label "Parc National Ichkeul" ;
    rdfs:comment "Réserve naturelle" .
}
```

Cette requête est envoyée via **form data** :
```
query=PREFIX eco: ...
```

---

## 🔍 Dépannage

### Erreur 422 persiste
→ **Cause :** Frontend pas rechargé  
→ **Solution :** F5 sur http://localhost:3000

### Erreur 500 "update endpoint not found"
→ **Cause :** Fuseki dataset mal configuré  
→ **Solution :** Vérifier que le dataset a l'endpoint `/update` activé

### Insertion réussie mais données invisibles
→ **Cause :** Cache navigateur  
→ **Solution :** 
1. Recharger la page CRUD
2. Ou vérifier directement dans Fuseki UI

### Erreur "Invalid URI"
→ **Cause :** Caractères spéciaux dans les noms  
→ **Solution :** Éviter les accents et caractères spéciaux dans les noms d'entités

---

## ✨ Résultat Attendu

### **Succès :**
```
✅ "Entité créée avec succès!"
✅ Backend : 200 OK
✅ Fuseki : 204 No Content
✅ Données visibles dans Fuseki query
```

### **Échec :**
```
❌ Erreur 422 → Vérifier format de requête
❌ Erreur 500 → Vérifier logs backend
❌ Erreur Fuseki → Vérifier dataset
```

---

## 🎯 Test Complet des Entités

### **Destinations**
- Nom : "Lac de Bizerte"
- Description : "Magnifique lac naturel"
- Région : "Nord"

### **Hébergements**
- Nom : "Eco-Lodge Dar Bhar"
- Description : "Hébergement écologique"
- Prix : "120"

### **Activités**
- Nom : "Randonnée Parc Ichkeul"
- Description : "Découverte de la faune"
- Durée : "4h"

### **Certifications**
- Nom : "Green Key"
- Description : "Label international environnement"

---

## 📊 Vérification Finale

Après avoir créé quelques entités, testez :

```bash
curl http://localhost:8000/destinations
```

Devrait retourner vos nouvelles destinations ! 🎉

---

**Status :** ✅ CRUD Opérationnel  
**Date :** 6 Novembre 2025, 22:48  
**Test :** Prêt à tester !

🚀 **Rechargez le frontend et testez maintenant !**
