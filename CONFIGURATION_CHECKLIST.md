# ✅ CHECKLIST DE CONFIGURATION

## Phase 1: Prérequis (Avant de commencer)

- [ ] Python 3.9+ installé (`python --version`)
- [ ] Node.js 18+ installé (`node --version`)
- [ ] Apache Jena Fuseki téléchargé et extrait
- [ ] Git installé (optionnel)
- [ ] Editeur de texte/IDE disponible

## Phase 2: Configuration Backend

### 2.1 Dépendances Python
- [ ] Virtual environment créé: `python -m venv venv`
- [ ] Virtual environment activé: `.\venv\Scripts\Activate.ps1`
- [ ] Dépendances installées: `pip install -r requirements.txt`
- [ ] SpaCy français optionnel: `python -m spacy download fr_core_news_md`

### 2.2 Fichier .env Backend
- [ ] Fichier créé: `backend/.env`
- [ ] FUSEKI_ENDPOINT configuré
- [ ] USE_GEMINI configuré
- [ ] BACKEND_PORT configuré (défaut: 8000)
- [ ] FRONTEND_URL configuré

### 2.3 Validation Backend
- [ ] Fichier main.py valide
- [ ] Fichier config.py valide
- [ ] Dossier services/ présent avec __init__.py
- [ ] Services fuseki_client.py et nl_to_sparql.py présents

## Phase 3: Configuration Frontend

### 3.1 Dépendances Node
- [ ] npm install exécuté
- [ ] node_modules créé
- [ ] package.json valide
- [ ] package-lock.json généré

### 3.2 Configuration Vite
- [ ] vite.config.js présent
- [ ] Proxy configuré pour /api
- [ ] index.html présent

### 3.3 Validation Frontend
- [ ] Dossier src/ avec components/
- [ ] App.jsx, main.jsx, index.css présents
- [ ] Tous les components (Header, Dashboard, etc.) présents

## Phase 4: Apache Jena Fuseki

### 4.1 Installation
- [ ] Fuseki téléchargé (version 4.x)
- [ ] Fuseki extrait dans C:\apache-jena-fuseki-4.x.x
- [ ] fuseki-server.bat accessible
- [ ] Répertoire bin/ présent

### 4.2 Configuration
- [ ] Port 3030 disponible
- [ ] Dossier databases/ créé (optionnel)
- [ ] Permissions d'exécution OK

### 4.3 Chargement Ontologie
- [ ] waste-management.rdf présent dans racine
- [ ] Fichier RDF valide
- [ ] Dataset "waste_management" créé dans Fuseki
- [ ] Ontologie chargée dans le dataset

## Phase 5: Tests de Connectivité

### 5.1 Test Fuseki
- [ ] Fuseki démarre: `.\fuseki-server.bat --update --mem /waste_management`
- [ ] Interface accessible: http://localhost:3030
- [ ] Status page: http://localhost:3030/status
- [ ] Dataset "waste_management" présent

### 5.2 Test Backend
- [ ] Backend démarre: `python main.py`
- [ ] Écoute sur port 8000
- [ ] Health check: `curl http://localhost:8000/health`
- [ ] API Docs: http://localhost:8000/docs
- [ ] Se connecte à Fuseki

### 5.3 Test Frontend
- [ ] Frontend démarre: `npm run dev`
- [ ] Écoute sur port 3000
- [ ] Page charge: http://localhost:3000
- [ ] Se connecte au backend
- [ ] API calls fonctionnent

## Phase 6: Validation Fonctionnelle

### 6.1 Recherche NL→SPARQL
- [ ] Page Recherche accessible
- [ ] Question test: "Quels sont les points de collecte?"
- [ ] Requête SPARQL générée visible
- [ ] Résultats affichés

### 6.2 Points de Collecte
- [ ] Page Points accessible
- [ ] Points chargés depuis Fuseki
- [ ] Filtres fonctionnent
- [ ] Détails affichables

### 6.3 Communauté
- [ ] Page Communauté accessible
- [ ] Badges affichés
- [ ] Activités listées
- [ ] Formulaire contribution visible

### 6.4 Statistiques
- [ ] Page Stats accessible
- [ ] Métriques chargées
- [ ] Graphiques affichés
- [ ] Timeline visible

### 6.5 Dashboard
- [ ] Page Accueil accessible
- [ ] Statistiques principales affichées
- [ ] Caractéristiques listées
- [ ] Activités récentes affichées

## Phase 7: Performance & Optimisation

### 7.1 Chargement Initial
- [ ] Frontend charge en < 3s
- [ ] API répond en < 1s
- [ ] Requêtes SPARQL < 500ms
- [ ] Pas d'erreurs console

### 7.2 Responsivité
- [ ] Mobile (< 768px) OK
- [ ] Tablet (768px-1024px) OK
- [ ] Desktop (> 1024px) OK
- [ ] Touch events fonctionnent

### 7.3 Navigateur
- [ ] Chrome OK
- [ ] Firefox OK
- [ ] Edge OK
- [ ] Safari (si Mac) OK

## Phase 8: Sécurité Développement

### 8.1 CORS
- [ ] Frontend sur 3000
- [ ] Backend sur 8000
- [ ] Pas d'erreurs CORS
- [ ] CORS_ORIGINS bien configuré

### 8.2 Variables d'Environnement
- [ ] .env créé (pas versionné)
- [ ] Secrets protégés
- [ ] Ports corrects
- [ ] Endpoints corrects

### 8.3 Validation
- [ ] Inputs validés (Pydantic)
- [ ] Pas d'injection SQL
- [ ] SPARQL queries sécurisées
- [ ] XSS protégé

## Phase 9: Documentation

### 9.1 Fichiers Documentation
- [ ] README.md complet et lisible
- [ ] QUICKSTART.md à jour
- [ ] INSTALLATION.md détaillé
- [ ] ONTOLOGY_DOCUMENTATION.md fourni

### 9.2 Code Documentation
- [ ] Fonctions documentées
- [ ] Classes documentées
- [ ] Commentaires clairs
- [ ] Docstrings présentes

### 9.3 Exemples
- [ ] Exemples de requêtes
- [ ] Exemple .env
- [ ] Scripts de démarrage
- [ ] Exemples de réponses

## Phase 10: Déploiement Préparation

### 10.1 Scripts Automatisation
- [ ] start-all.bat créé
- [ ] start-all.ps1 créé
- [ ] Scripts testés
- [ ] Scripts documentés

### 10.2 Logging
- [ ] Logs backend correctement formatés
- [ ] Logs frontend visibles (console)
- [ ] Logs Fuseki accessibles
- [ ] Logs persistants (optionnel)

### 10.3 Backup & Persistance
- [ ] Ontologie RDF backupée
- [ ] Base Fuseki persistent (optionnel)
- [ ] Procédure backup documentée
- [ ] Procédure restore documentée

## Phase 11: Tests Finaux

### 11.1 Scénarios Utilisateur
- [ ] Nouveau utilisateur peut chercher
- [ ] Utilisateur peut voir les points
- [ ] Utilisateur peut participer
- [ ] Utilisateur peut voir stats

### 11.2 Flux Complets
- [ ] Recherche NL → Résultats ✓
- [ ] Localisation → Détails ✓
- [ ] Activité → Participation ✓
- [ ] Stats → Graphiques ✓

### 11.3 Gestion d'Erreurs
- [ ] Backend indisponible gérée
- [ ] Fuseki indisponible gérée
- [ ] Résultats vides gérés
- [ ] Erreurs API gérées

## Phase 12: Maintenance

### 12.1 Monitoring
- [ ] Services UP
- [ ] CPU usage < 50%
- [ ] Memory usage sain
- [ ] Disk space available

### 12.2 Logs Réguliers
- [ ] Vérifier logs journaliers
- [ ] Vérifier erreurs
- [ ] Vérifier performance
- [ ] Archiver logs anciens

### 12.3 Mise à Jour
- [ ] Dependencies à jour (optionnel)
- [ ] Security patches appliqués
- [ ] Documentation mise à jour
- [ ] Version number incrémentée

## 🎯 Points de Contrôle Critiques

| Point | Critère | Status |
|-------|---------|--------|
| Fuseki | 3030 répondre | [ ] |
| Backend | 8000 répondre | [ ] |
| Frontend | 3000 répondre | [ ] |
| Health | `/health` OK | [ ] |
| Query | NL→SPARQL OK | [ ] |
| Data | Points de collecte | [ ] |
| UI | Dashboard visible | [ ] |
| API | Swagger disponible | [ ] |

## 📋 Action Items

```
AVANT DE DÉMARRER:
[ ] Tous les prérequis installés
[ ] Backend .env configuré
[ ] Fuseki démarre

AVANT D'UTILISER:
[ ] Tous les services démarrent
[ ] Ontologie chargée
[ ] Tests basiques passent

AVANT PRODUCTION:
[ ] Tous les tests réussissent
[ ] Documentation complète
[ ] Logs configurés
```

## 🚀 Go/No-Go Decision

**Green Light si:**
- ✅ Tous les services up
- ✅ API health check OK
- ✅ UI interactive
- ✅ Requêtes NL→SPARQL OK
- ✅ Données chargées
- ✅ Pas d'erreurs console

**Red Flag si:**
- ❌ Service indisponible
- ❌ CORS errors
- ❌ Port occupé
- ❌ Ontologie non chargée
- ❌ Erreurs Python/npm

---

**Imprimez cette checklist et cochez au fur et à mesure! ✅**

**Status Global:** [ ] Prêt pour démarrage
**Date de vérification:** _______________
**Vérifiée par:** _______________
