# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## ✨ Ce qui a changé

**AVANT :** Un seul onglet "CRUD" avec un sélecteur

**MAINTENANT :** 4 onglets séparés dans la navbar :
- 🗺️ **Destinations**
- 🏨 **Hébergements**  
- 🥾 **Activités**
- 🏆 **Certifications**

Chaque section affiche :
1. ✅ **Requête SPARQL générée** (avec temps d'exécution)
2. ✅ **Résultats en JSON brut**
3. ✅ **Tableau formaté** des résultats

---

## 🎯 Démarrage en 3 Étapes

### **1. Backend**
```powershell
cd C:\Users\ACHREF\Eco-Tourisme\backend
.\venv\Scripts\Activate.ps1
python main.py
```

Attendez : `✅ Successfully connected to Fuseki!`

### **2. Frontend**
```powershell
# Nouveau terminal
cd C:\Users\ACHREF\Eco-Tourisme\frontend
npm run dev
```

Attendez : `Local: http://localhost:3000`

### **3. Tester**
1. Ouvrir : **http://localhost:3000**
2. Cliquer sur **"Destinations"** dans la navbar
3. Cliquer sur **"Lire (SELECT)"**
4. Observer les 3 sections :
   - Requête SPARQL (noir)
   - JSON brut (blanc)
   - Tableau (blanc)

---

## 📝 Test Rapide : Créer une Destination

1. Clic sur **"Destinations"**
2. Clic sur **"Créer (INSERT)"**
3. Remplir :
   ```
   Nom : Parc National Ichkeul
   Description : Réserve naturelle protégée
   Région : Bizerte
   Pays : Tunisie
   ```
4. Clic sur **"Créer"**
5. ✅ Message de succès
6. Voir la requête INSERT affichée
7. Le tableau se recharge avec la nouvelle destination

---

## 🔍 Vérification Rapide

### Dans le navigateur :
- [ ] Navbar a 4 nouveaux onglets (Destinations, Hébergements, etc.)
- [ ] Cliquer sur "Destinations" affiche la page
- [ ] Voir "Gestion des Destinations" en vert
- [ ] Voir 2 boutons : "Lire (SELECT)" et "Créer (INSERT)"
- [ ] Cliquer "Lire" affiche la requête SPARQL

### Dans les logs backend :
```
INFO: 127.0.0.1:xxxxx - "GET /destinations HTTP/1.1" 200 OK
```

### Dans les logs Fuseki :
```
INFO Fuseki :: [X] Query = PREFIX eco: ... SELECT ?destination
INFO Fuseki :: [X] 200 OK (XX ms)
```

---

## 📂 Fichiers Importants

### Créés :
- ✅ `frontend/src/components/EntityManager.jsx`
- ✅ `frontend/src/components/EntityManager.css`
- ✅ `frontend/src/config/entityConfigs.js`

### Modifiés :
- ✅ `frontend/src/components/Header.jsx` (4 nouveaux onglets)
- ✅ `frontend/src/App.jsx` (gestion des 4 sections)

---

## 🆘 Problèmes Courants

### Erreur : "Cannot find module './config/entityConfigs'"
```powershell
# Solution : Le dossier config n'existe pas
cd C:\Users\ACHREF\Eco-Tourisme\frontend\src
mkdir config
# Puis copiez le fichier entityConfigs.js dedans
```

### Erreur : Onglets non visibles
→ **Solution :** Rechargez la page (F5)

### Erreur : SPARQL ne s'affiche pas
→ **Solution :** Vérifiez que le backend retourne bien la requête

---

## 🎉 C'est Tout !

L'interface est maintenant séparée en 4 sections dédiées.

**Profitez de votre nouvelle interface ! 🚀**

---

**Support :**
- Voir `NOUVELLE_INTERFACE.md` pour les détails complets
- Voir `CRUD_REPARE.md` pour le debugging
