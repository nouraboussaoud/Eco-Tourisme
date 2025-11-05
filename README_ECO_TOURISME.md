# 🌍 Tourisme Éco-responsable - Plateforme Web Sémantique

[![Status](https://img.shields.io/badge/status-active-brightgreen)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

> **Une plateforme intelligente de recommandations de voyage durable utilisant le Web Sémantique, SPARQL et des ontologies RDF.**

---

## 🎯 Vision du Projet

Promouvoir un **tourisme durable et responsable** en :
- 🏖️ Recommandant des destinations respectueuses de l'environnement
- 🏨 Guidant vers des hébergements écologiques certifiés
- 🎯 Proposant des activités à faible impact carbone
- 📊 Calculant et visualisant l'empreinte carbone des voyages
- 🌱 Sensibilisant les voyageurs aux enjeux écologiques
- 🤝 Créant une communauté d'éco-voyageurs

---

## 🏗️ Architecture Technique

### 🔗 Web Sémantique
- **Ontologie RDF**: Concepts du tourisme durable (destinations, hébergements, activités, transports)
- **Requêtes SPARQL**: Interrogation intelligente du graphe de connaissances
- **Triplet Store Fuseki**: Stockage et interrogation des données RDF
- **NL to SPARQL**: Conversion automatique de questions en français vers SPARQL

### 💻 Stack Technique
```
┌─────────────────────────────────────────────────────────┐
│  Frontend (React/Vite)                                  │
│  - Dashboard avec statistiques éco-touristiques         │
│  - Recommandations personnalisées                        │
│  - Calculatrice d'empreinte carbone                     │
│  - Interface de recherche sémantique                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ API HTTP
                     │
┌────────────────────▼────────────────────────────────────┐
│  Backend (Python/FastAPI)                               │
│  - REST API endpoints                                   │
│  - Conversion NL → SPARQL                               │
│  - Moteur de recommandations                            │
│  - Calcul d'impact carbone                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ SPARQL Query
                     │
┌────────────────────▼────────────────────────────────────┐
│  Fuseki (Triplet Store RDF)                             │
│  - Base de connaissances sémantique                     │
│  - Ontologie du tourisme durable                        │
│  - Données sur destinations, hébergements, activités    │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Concepts Clés du Domaine

### 🏖️ Destination (Lieu de visite)
- **Types**: Plage, Montagne, Ville, Patrimoine Culturel
- **Propriétés**: Nom, Description, Région, Certification Eco
- **Exemples**: Provence, Alpes, Côte d'Azur

### 🏨 Hébergement (Où dormir)
- **Types**: Hôtel Écologique, Gîte Rural, Auberge, Camping Éco
- **Propriétés**: Certification, Empreinte Carbone, Services
- **Critères**: Durabilité, Impact environnemental

### 🎯 Activité Touristique (Que faire)
- **Sportives**: Randonnée, Plongée, Vélo
- **Culturelles**: Musée, Visite historique, Ateliers locaux
- **Détente**: Spa, Méditation, Yoga
- **Éducatives**: Ateliers culinaires, Apprentissage local

### ✈️ Transport (Comment voyager)
- **Aériens**: Avion (❌ haut CO2), Hélicoptère
- **Terrestres**: Train (✅ écologique), Bus, Vélo électrique
- **Maritimes**: Bateau Éco (faible impact), Ferry
- **Métrique**: kg CO2 par km

### 👥 Voyageur (Profil)
- **Aventure**: Sports et nature
- **Culture**: Patrimoine et apprentissage local
- **Bien-Être**: Détente et méditation
- **Famille**: Activités adaptées aux enfants

### 🏅 Certification Écologique
- **Labels Nationaux**: EcoTourism, France Qualité
- **Labels Internationaux**: GreenGlobe, EU Ecolabel
- **Critères**: Durabilité, Protection environnement, Engagement local

---

## 🚀 Installation & Démarrage

### Prérequis
- Python 3.8+
- Node.js 16+
- Apache Jena Fuseki (pour le triplet store)
- Docker (optionnel)

### 1️⃣ Installer Fuseki

```bash
# Télécharger Fuseki
wget https://archive.apache.org/dist/jena/apache-jena-fuseki-5.6.0.zip
unzip apache-jena-fuseki-5.6.0.zip

# Démarrer Fuseki
cd apache-jena-fuseki-5.6.0
./fuseki-server --mem /eco-tourism
```

Fuseki sera disponible sur: `http://localhost:3030`

### 2️⃣ Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur
python main.py
```

Backend sur: `http://localhost:8000`
Docs API: `http://localhost:8000/docs`

### 3️⃣ Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
```

Frontend sur: `http://localhost:3000` (ou le port indiqué)

---

## 📊 Endpoints Principaux

### Découverte
- `GET /destinations` - Toutes les destinations durables
- `GET /hebergements` - Hébergements écologiques
- `GET /activites` - Activités disponibles
- `GET /certifications` - Labels écologiques reconnus

### Données
- `GET /stats` - Statistiques du tourisme durable
- `GET /recommendation/profiles` - Profils de voyageurs
- `GET /recommendation/carbon-calculator` - Calcul empreinte carbone

### Sémantique
- `POST /query` - Question en langage naturel → Résultats SPARQL
- `POST /sparql` - Requête SPARQL directe
- `GET /examples` - Exemples de requêtes

### Communauté
- `POST /avis` - Ajouter un avis sur une attraction
- `POST /signalement-eco` - Signaler un problème environnemental

---

## 🔍 Exemples de Requêtes SPARQL

### Trouver les destinations certifiées Eco
```sparql
PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?destination ?nom ?certification
WHERE {
  ?destination rdf:type eco:Destination .
  ?destination wm:nom ?nom .
  ?destination eco:aCertification ?cert .
  ?cert rdf:type eco:GreenGlobe .
}
```

### Comparer empreinte carbone des transports
```sparql
PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?transport ?nom ?co2
WHERE {
  ?transport rdf:type eco:Transport .
  ?transport wm:nom ?nom .
  ?transport eco:aEmpreinte ?empreinte .
  ?empreinte eco:kgCO2 ?co2
}
ORDER BY ?co2
```

### Recommandation personnalisée
```sparql
PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?destination ?hebergement ?activite ?score
WHERE {
  ?destination rdf:type eco:Destination .
  ?hebergement rdf:type eco:Hebergement .
  ?activite rdf:type eco:ActiviteSportive .
  
  ?destination eco:aCertification ?cert .
  ?hebergement eco:aCertification ?cert .
}
LIMIT 10
```

---

## 🎨 Interface Utilisateur

### 🏠 Accueil
- Bienvenue et contexte du tourisme durable
- Statistiques globales (destinations, voyageurs, impact carbone)
- Appel à l'action

### 🗺️ Destinations
- Liste filtrable des destinations durables
- Détails: certification, empreinte carbone, activités
- Carte interactive (optionnel)

### ⭐ Recommandations
- Questionnaire profil du voyageur
- Générateur de packages éco-touristiques
- Calcul de l'impact carbone
- Comparaison d'alternatives

### 🌐 Communauté
- Avis de voyageurs
- Signalement de problèmes écologiques
- Forum/discussions
- Badges et récompenses

### 📊 Statistiques
- Tendances du tourisme durable
- Impact carbone des voyages
- Comparaison destinations
- Performances des certifications

---

## 📚 Documentation Complète

- **Ontologie**: [`ONTOLOGY_DOCUMENTATION.md`](./ONTOLOGY_DOCUMENTATION.md)
- **Structure du Projet**: [`PROJECT_STRUCTURE.md`](./PROJECT_STRUCTURE.md)
- **Configuration Avancée**: [`CONFIGURATION_AVANCEE.md`](./CONFIGURATION_AVANCEE.md)
- **Résumé Transformation**: [`TRANSFORMATION_SUMMARY.md`](./TRANSFORMATION_SUMMARY.md)

---

## 🔧 Configuration

### Variables d'Environnement (.env)
```env
# Backend
FUSEKI_ENDPOINT=http://localhost:3030/eco-tourism/sparql
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# Optionnel: Gemini API pour NL→SPARQL amélioré
USE_GEMINI=false
GEMINI_API_KEY=your_key_here

# Fuseki
FUSEKI_DATASET=eco-tourism
```

---

## 💡 Cas d'Usage

### 1️⃣ Voyageur Aventurier
```
Question: "Je veux faire de la randonnée écologique"
Résultats:
- Destinations: Alpes, Pyrénées, Jura
- Activités: Randonnée, Escalade
- Transport: Train + vélo électrique
- Hébergement: Gîte rural certifié
- Impact CO2: 250kg (estimé)
```

### 2️⃣ Famille en Vacances
```
Question: "Vacances famille écologiques de 2 semaines"
Résultats:
- Destinations: Bretagne, Côte d'Azur
- Activités: Plage, Musée, Ateliers
- Transport: Bus, train (en group)
- Hébergement: Camping éco-responsable
- Budget: 2000€/famille
```

### 3️⃣ Digital Nomade
```
Question: "Je veux voyager durable avec faible impact carbone"
Résultats:
- Destinations: Paris, Lyon, Marseille
- Transport: Train principalement
- Empreinte carbone: Très faible
- Durabilité: Optimale
```

---

## 🌱 Enjeux Adressés

### 🌍 Changement Climatique
- ✅ Calcul transparent d'empreinte carbone
- ✅ Recommandation de transports bas-carbone
- ✅ Sensibilisation aux impacts écologiques

### 🏞️ Préservation de la Nature
- ✅ Promotion des destinations protégées
- ✅ Certifications écologiques vérifiées
- ✅ Limitation de l'overtourism

### 👥 Responsabilité Sociale
- ✅ Soutien aux communautés locales
- ✅ Partage des bénéfices économiques
- ✅ Respect des cultures locales

### 📊 Transparence et Education
- ✅ Données ouvertes et sémantiques
- ✅ Interface éducative
- ✅ Engagement de la communauté

---

## 🎯 Feuille de Route

### ✅ Phase 1 (Actuelle)
- [x] Ontologie du tourisme durable
- [x] Architecture backend/frontend
- [x] Endpoints principaux
- [x] Recommandations de base

### 📅 Phase 2 (Court terme)
- [ ] Interface utilisateur complète
- [ ] Population de données d'exemple
- [ ] Moteur de recommandations avancé
- [ ] Calcul d'empreinte carbone raffiné

### 🔮 Phase 3 (Moyen terme)
- [ ] Mobile app (iOS/Android)
- [ ] Intégration réseaux sociaux
- [ ] Gamification (badges, défi, récompenses)
- [ ] Community features (avis, forums)

### 🌟 Phase 4 (Long terme)
- [ ] IA/Machine Learning pour suggestions
- [ ] Partenariats avec opérateurs touristiques
- [ ] Intégration paiement/booking
- [ ] Certification blockchain

---

## 📞 Support et Contact

### Documentation
- 📖 Wiki du projet: [À créer]
- 🐛 Issue Tracker: [GitHub Issues]
- 💬 Discussions: [GitHub Discussions]

### Équipe
- **Architecture**: Achref Limem, Ahmed Mejri
- **Ontologie**: Nour Aboussaoud, Elyess Borji
- **Frontend**: Adem Khedhira
- **Coordination**: L'équipe

---

## 📄 Licence & Crédits

### Licence
MIT License - Libre d'utilisation et de modification

### Crédits
- Apache Jena pour Fuseki
- React pour l'interface
- FastAPI pour le backend
- Web Sémantique W3C standards

---

## 🌟 Contribution

Nous accueillons les contributions! Pour participer:

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

**🚀 Bienvenue dans l'avenir du tourisme durable! 🌱**

*"Voyager bien, c'est voyager responsable."*
