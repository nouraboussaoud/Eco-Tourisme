# 🎓 Guide Pratique - Tourisme Éco-responsable
## Exemples et Cas d'Usage Réels

---

## 📍 Carte Conceptuelle

```
TOURISME ÉCO-RESPONSABLE
│
├─ 🏖️ DESTINATION
│  ├─ Plage (Côte d'Azur, Bretagne)
│  ├─ Montagne (Alpes, Pyrénées)
│  ├─ Ville (Paris, Lyon)
│  └─ Patrimoine (Versailles, Mont Saint-Michel)
│
├─ 🏨 HÉBERGEMENT
│  ├─ Hôtel Écologique (Label)
│  ├─ Gîte Rural (Fermier)
│  ├─ Auberge (Communautaire)
│  └─ Camping Éco (Écotourisme)
│
├─ 🎯 ACTIVITÉ
│  ├─ Sportive (Randonnée, Plongée)
│  ├─ Culturelle (Musée, Visite)
│  ├─ Détente (Spa, Yoga)
│  └─ Éducative (Atelier, Apprentissage)
│
├─ ✈️ TRANSPORT
│  ├─ Train (Faible CO2) ✅
│  ├─ Bus (Faible CO2) ✅
│  ├─ Voiture (Moyen CO2) ⚠️
│  ├─ Avion (Haut CO2) ❌
│  └─ Vélo/Marche (0 CO2) ✅✅
│
├─ 👥 PROFIL VOYAGEUR
│  ├─ Aventurier (sports, nature)
│  ├─ Culturel (patrimoine, local)
│  ├─ Bien-Être (détente, santé)
│  └─ Famille (enfants, activités)
│
├─ 🏅 CERTIFICATION
│  ├─ EcoTourism (Label national)
│  ├─ GreenGlobe (International)
│  ├─ Ecolabel UE (Europe)
│  └─ France Qualité
│
└─ 📊 IMPACT
   ├─ Empreinte CO2 (kg)
   ├─ Consommation d'eau
   ├─ Préservation biodiversité
   └─ Support économique local
```

---

## 💼 Cas d'Usage #1: Jeune Aventurier

### 👤 Profil
- **Nom**: Marc, 28 ans
- **Profil**: Aventurier
- **Budget**: 1500€
- **Durée**: 1 semaine
- **Priorité**: Basse empreinte carbone

### 🤔 Question
```
"Je veux faire une semaine de randonnée écologique dans les montagnes françaises
 avec le moins possible d'impact carbone et un petit budget."
```

### 🔍 Processus

1. **Reconnaissance NL→SPARQL**
   - Type: "destinations" + "activites" + "transports_eco"
   - Profil détecté: Aventurier
   - Budget: < 1500€
   - Priorité CO2: Oui

2. **Requête SPARQL Générée**
   ```sparql
   PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
   SELECT ?destination ?nom ?activite ?hebergement ?transport ?co2_total ?prix
   WHERE {
     ?destination rdf:type eco:Montagne .
     ?destination wm:nom ?nom .
     
     ?activite rdf:type eco:ActiviteSportive .
     ?activite eco:aLieu ?destination .
     
     ?hebergement rdf:type eco:GiteRural .
     ?hebergement eco:aLieu ?destination .
     ?hebergement wm:prix ?prix .
     FILTER (?prix < 100)
     
     ?transport rdf:type eco:Transport .
     ?transport eco:aEmpreinte ?empreinte .
     ?empreinte eco:kgCO2 ?co2_total .
     FILTER (?co2_total < 500)
   }
   ORDER BY ?co2_total
   LIMIT 5
   ```

3. **Résultats**
   ```
   ✅ PACKAGE RECOMMANDÉ #1
   ├─ Destination: Alpes (Chamonix)
   ├─ Transport: Train Paris→Chamonix (52 kg CO2)
   ├─ Activités:
   │  ├─ Randonnée Mont-Blanc (local, 0 CO2)
   │  ├─ Alpinisme guidé
   │  └─ Visite refuge écologique
   ├─ Hébergement: Gîte Montagnard certifié (80€/nuit)
   ├─ Repas: Local & bio
   ├─ Total CO2: 52 kg (très faible!)
   ├─ Total Budget: 1200€
   └─ Score Durabilité: 92/100 ⭐⭐⭐⭐⭐
   
   ✅ PACKAGE ALTERNATIF #2
   ├─ Destination: Pyrénées
   ├─ Transport: Bus éco (38 kg CO2)
   ├─ Total Budget: 980€
   └─ Score Durabilité: 95/100 ⭐⭐⭐⭐⭐
   ```

### 💡 Insights
- Empreinte carbone: 52kg (vs. 1500kg si avion)
- 96,5% de réduction d'empreinte!
- Soutien à l'économie locale
- Experience authentique

---

## 👨‍👩‍👧‍👦 Cas d'Usage #2: Famille en Vacances

### 👤 Profil
- **Famille**: 2 adultes + 2 enfants (6 & 10 ans)
- **Budget**: 3000€ 
- **Durée**: 2 semaines
- **Préoccupations**: Sécurité, divertissement, éducation

### 🤔 Question
```
"Où pouvons-nous aller en famille pendant 2 semaines avec des activités adaptées,
 en restant responsables?"
```

### 🔍 Processus SPARQL

```sparql
PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?destination ?nom ?hebergement ?activites ?transport ?prix_total
WHERE {
  ?destination rdf:type eco:Destination .
  
  ?hebergement rdf:type eco:Hebergement .
  ?hebergement eco:aLieu ?destination .
  ?hebergement wm:prix ?prix_nuit .
  FILTER (?prix_nuit * 14 < 3000)
  
  ?activite rdf:type ?type .
  FILTER (?type IN (eco:ActiviteCulturelle, eco:ActiviteSportive))
  ?activite eco:adapteeAuxEnfants true .
  
  ?hebergement eco:aCertification ?cert .
  ?cert rdf:type eco:CertificatEco .
}
ORDER BY ?destination
LIMIT 10
```

### 📊 Résultats

```
✅ OPTION #1: Bretagne (Idéale pour Famille)
├─ Destination: Côte de Bretagne
│  ├─ Plages de sable fin
│  ├─ Châteaux historiques
│  ├─ Forêts de pins
│  └─ Crêperies locales
│
├─ Hébergement: Camping Familial Éco (★★★★★)
│  ├─ Mobile-home confortable
│  ├─ Piscine chauffée
│  ├─ Énergie solaire + 90% déchets recyclés
│  ├─ 60€/nuit (840€ total 14 nuits)
│  └─ Certification: GreenGlobe ✓
│
├─ Activités Enfants (très variées!):
│  ├─ Canoë-kayak en rivière
│  ├─ Visite Aquarium (Brest)
│  ├─ Ferme pédagogique (animaux)
│  ├─ Musée pirates de Nantes
│  ├─ Croisière traditionnel
│  ├─ Plage & jeux de sable
│  └─ Atelier crêpes & cidre!
│
├─ Transport:
│  ├─ Paris→Rennes (Train Éco, 145 kg CO2)
│  ├─ Rennes→Camping (Bus local, 12 kg CO2)
│  └─ Sur place: Vélos fournis gratuitement
│
├─ Budget Total: 2100€
│  ├─ Hébergement: 840€
│  ├─ Transport: 200€
│  ├─ Activités: 600€
│  ├─ Repas locaux: 400€
│  └─ Contingence: 60€
│
├─ Empreinte CO2: 157 kg/famille (très faible)
├─ CO2 par personne/jour: 0,56 kg
└─ Score Durabilité: 94/100 ⭐⭐⭐⭐⭐
```

---

## 👩‍💼 Cas d'Usage #3: Entreprise Responsable

### 🏢 Contexte
- **Client**: Startup Tech écologique
- **Besoin**: Séminaire d'équipe (15 personnes, 3 jours)
- **Valeurs**: Durabilité, bien-être, team-building
- **Budget**: 500€/personne

### 📋 Question
```
"Organisez un séminaire éco-responsable pour notre équipe dans un
 hébergement certifié avec des activités team-building durables."
```

### 🔍 Requête SPARQL Avancée

```sparql
PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?destination ?hebergement ?activites ?co2_total ?score
WHERE {
  # Destination accessible par train
  ?destination rdf:type eco:Destination .
  
  # Hébergement avec salle séminaire
  ?hebergement rdf:type eco:Hebergement .
  ?hebergement eco:aLieu ?destination .
  ?hebergement wm:salleSeminaire true .
  ?hebergement wm:prix ?prix .
  FILTER (?prix < 500)
  
  # Certifié écologique
  ?hebergement eco:aCertification ?cert .
  ?cert rdf:type eco:GreenGlobe .
  
  # Activités group-friendly
  ?activite rdf:type eco:ActiviteTouristique .
  ?activite eco:aLieu ?destination .
  ?activite wm:adapteeGroupe true .
  
  # Calcul CO2: train seulement
  ?transport rdf:type eco:Train .
  ?transport eco:aEmpreinte ?em .
  ?em eco:kgCO2 ?co2_total .
}
ORDER BY ?co2_total DESC(?prix)
```

### ✅ Recommandation

```
🏆 SÉMINAIRE ECO-RESPONSABLE: LOIRE VALLEY

Destination: Château de Loire Valley
├─ Accessible par train direct Paris
├─ Vignobles locaux
├─ Patrimoine UNESCO
└─ Région certifiée Eco-Destination

Hébergement: Château Hôtel Éco (★★★★★)
├─ Salle séminaire (150 places)
├─ Chambres confortables (3 jours/2 nuits)
├─ Énergie 100% renouvelable
├─ Restaurant farm-to-table
├─ Certification GreenGlobe + Ecolabel
└─ 450€/personne (tout inclus!)

PROGRAMME 3 JOURS:

JOUR 1:
├─ 09:00 - Arrivée train & accueil
├─ 10:30 - Séminaire (morning session)
├─ 13:00 - Lunch bio local
├─ 14:30 - Visite vignobles écologiques
├─ 18:00 - Atelier cuisine bio
└─ 20:00 - Dîner gastronomique

JOUR 2:
├─ 09:00 - Séminaire (brainstorm)
├─ 12:30 - Déjeuner
├─ 14:00 - Activités team-building:
│  ├─ Randonnée château (2h)
│  ├─ Atelier viticulture
│  └─ Jeux de réflexion nature
├─ 18:00 - Yoga sunset
└─ 20:00 - Soirée conviviale

JOUR 3:
├─ 09:00 - Séminaire (conclusions)
├─ 12:00 - Déjeuner networking
├─ 14:00 - Départ train
└─ 16:00 - À Paris

IMPACT ÉCOLOGIQUE:
├─ Transport: Train (120 kg CO2 pour 15 pers.)
│  → 8 kg CO2 par personne
│  → Vs. Avion: 180 kg/personne! ❌
├─ Hébergement: 100% vert
├─ Repas: Bio & local
├─ Déchets: 100% triés/recyclés
└─ TOTAL CO2: 120 kg (très faible) ✅

BÉNÉFICES:
✅ Team-building mémorable
✅ Impact écologique minimal
✅ Support économie locale
✅ Produits bio/de qualité
✅ Image RSE renforcée
✅ Budget optimisé

SCORE ECO: 96/100 ⭐⭐⭐⭐⭐
```

---

## 📱 Interface Utilisateur Exemple

### 🔍 Page de Recommandation

```
┌─────────────────────────────────────────────────────┐
│ 🌍 CRÉER MON VOYAGE PARFAIT                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Profil: [ Aventurier ▼ ]                          │
│         Qui êtes-vous? Adventure | Culture         │
│                       | BienEtre | Famille          │
│                                                     │
│ Budget: [ 1500 € ]    Durée: [ 7 ] jours         │
│                                                     │
│ Priorité Écologie:  ● Très important               │
│                     ○ Importante                   │
│                     ○ Normal                       │
│                                                     │
│ Région: [ Toute France ▼ ]                        │
│                                                     │
│         [🔍 GÉNÉRER RECOMMANDATIONS]              │
│                                                     │
└─────────────────────────────────────────────────────┘

RÉSULTATS:
┌─────────────────────────────────────────────────────┐
│ ⭐ PACKAGE #1: Alpes - Semaine d'Aventure       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 🏔️  Destination: Mont-Blanc                        │
│ 🏨 Hébergement: Gîte Montagnard (★★★★★)         │
│ 🎯 Activités: Randonnée, Escalade, Alpinisme   │
│ ✈️  Transport: Train (52 kg CO2) ✅              │
│                                                     │
│ Budget: 1200€  |  CO2: 52kg  |  Score: 92/100    │
│                                                     │
│ [📸 Voir détails] [❤️ Sauvegarder] [📤 Partager] │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 📊 Calculatrice CO2

```
┌──────────────────────────────────────────┐
│ 🌱 CALCULER MON EMPREINTE CARBONE       │
├──────────────────────────────────────────┤
│                                          │
│ Transport Aller:                         │
│ ├─ Avion (Paris→Nice) : 1500 kg CO2 ❌ │
│ ├─ Train (Paris→Nice) : 110 kg CO2 ✅  │
│ ├─ Bus (Paris→Nice)  : 80 kg CO2 ✅   │
│ └─ Voiture (Paris)   : 450 kg CO2 ⚠️  │
│                                          │
│ Hébergement (7 nuits):                   │
│ ├─ Hôtel standard: 120 kg CO2           │
│ ├─ Hôtel bio     : 30 kg CO2 ✅        │
│ └─ Gîte eco      : 10 kg CO2 ✅✅      │
│                                          │
│ Activités:                               │
│ ├─ Randonnée locale: 0 kg CO2 ✅✅     │
│ ├─ Tour en voiture: 200 kg CO2         │
│ └─ Croisière bateau: 80 kg CO2         │
│                                          │
│ TOTAL: 200 kg CO2 (très écologique!) ✅ │
│                                          │
│ Équivalent:                              │
│ ├─ Vol Paris→Berlin → 7x moins          │
│ └─ Voiture semaine → 2x moins           │
│                                          │
└──────────────────────────────────────────┘
```

---

## 🎓 Conseils pour Voyageur Éco-responsable

### ✅ À FAIRE
1. **Transport**
   - ✅ Prendre le train (80% moins d'émissions)
   - ✅ Voiture partagée
   - ✅ Bus local
   - ✅ Vélo/marche sur place

2. **Hébergement**
   - ✅ Chercher certification (GreenGlobe, Ecolabel)
   - ✅ Gîtes et chambres d'hôtes locales
   - ✅ Hôtels utilisant énergies renouvelables
   - ✅ Respecter les règles de tri des déchets

3. **Activités**
   - ✅ Guides locaux et guides à pied
   - ✅ Activités sans moteur
   - ✅ Apprendre la langue et culture locales
   - ✅ Manger local et bio
   - ✅ Soutenir petits commerces

4. **Budget**
   - ✅ Rester plus longtemps (vs. multiples courts voyages)
   - ✅ Voyager hors saison (less overtourism)
   - ✅ Manger où mangent les locaux
   - ✅ Utiliser transports publics

### ❌ À ÉVITER
1. **Transport**
   - ❌ Avion (sauf indispensable)
   - ❌ Voiture seul
   - ❌ Hélicoptère touristique
   - ❌ Croisière (énorme impact!)

2. **Hébergement**
   - ❌ Chaînes hôtelières sans engagement eco
   - ❌ Resorts all-inclusive isolés
   - ❌ Constructions neuves en zones protégées

3. **Activités**
   - ❌ Drones/quads/motos
   - ❌ Sports aquatiques motorisés
   - ❌ Safari touristique intensif
   - ❌ Attractions exploitant animaux

4. **Achat**
   - ❌ Souvenirs en plastique
   - ❌ Produits de faune/flore protégée
   - ❌ Achats inutiles "touristiques"

---

## 🌟 Impact Mesurable

### Exemple: 1 Semaine Alpes vs. Autres Options

| Critère | Train (Recommandé) | Avion | Voiture | CO2 Économisé |
|---------|------------------|-------|---------|--------------|
| Transport CO2 | 52 kg | 1500 kg | 450 kg | 1448 kg |
| Hébergement | 30 kg | 30 kg | 30 kg | - |
| Total | **82 kg** | **1530 kg** | **480 kg** | **95% vs avion** |
| Équivalent | Voiture 430 km | Rome ↔ Paris | 2500 km | - |

### Votre Impact Écologique
- **82 kg CO2** = Moins d'1 vol intérieur français
- **1 semaine sage** = 6 mois de transports quotidiens
- **Empreinte réduite de 96,5%** = 10 ans de progrès climatique!

---

**🌍 Voyagez responsable. Explorez consciemment. Protégez l'avenir. 🌱**
