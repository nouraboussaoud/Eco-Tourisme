# Documentation de l'Ontologie Waste Management

## 📚 Vue d'ensemble

L'ontologie `waste-management.rdf` est une représentation sémantique complète d'un système de gestion des déchets avec engagement communautaire. Elle utilise OWL 2 et RDF pour structurer les concepts, propriétés et relations.

**Namespace:** `http://www.semanticweb.org/waste-management/2025/1/#`

## 🏗️ Architecture de l'Ontologie

### Classes Principales

#### 1. **Déchets (Waste)**

```
Dechet (base)
│
├── TypeDechet (classification)
│   ├── DechetsOrganiques
│   ├── DechetsRecyclables
│   ├── DechetsHazardeux
│   └── DechetsEncombrants
```

**Propriétés:**
- `nom`: Nom du déchet (String)
- `description`: Description détaillée (String)
- `quantite`: Quantité en kilos (Float)
- `unite`: Unité de mesure (String)

#### 2. **Points de Collecte (Collection Points)**

```
PointCollecte (base)
│
├── PointDecheterie (déchèteries)
├── PointBac (conteneurs)
└── PointCompostage (compostage communautaire)
```

**Propriétés:**
- `nom`: Nom du point (String)
- `adresse`: Adresse complète (String)
- `latitude`: Coordonnée GPS (Float)
- `longitude`: Coordonnée GPS (Float)
- `horaires`: Horaires d'ouverture (String)
- `telephone`: Numéro de contact (String)
- `accepte`: Types de déchets acceptés (ObjectProperty → TypeDechet)

**Relations:**
- `localiseDans`: Localisation dans une ville
- `localiseDansQuartier`: Localisation dans un quartier

#### 3. **Localisation (Location)**

```
Destination (base)
│
├── Ville (villes)
└── Quartier (quartiers)
```

**Propriétés:**
- `nom`: Nom de la localité (String)

#### 4. **Engagement Communautaire (Community)**

##### A. Utilisateurs

```
Utilisateur
├── nom, email, dateCreation
├── aContribution → Contribution
├── aBadge → Badge
└── aEffectue → Activite
```

##### B. Activités

```
Activite (base)
│
├── Evenement (événements)
└── Defi (défis)

Propriétés:
- nom, description
- dateActivite (DateTime)
- seLieuA → PointCollecte
- participant → Utilisateur
```

##### C. Système de Récompenses

```
Badge
├── nom, description
├── icone, couleur

Points
├── nombrePoints (Integer)
├── dateAcquisition
```

##### D. Contributions

```
Contribution
├── description, quantite, unite
├── dateCreation
├── statut (acceptée/en attente/rejetée)
├── aCommentaire → Commentaire
└── auteur → Utilisateur

Commentaire
├── texte, dateCreation
└── auteur → Utilisateur
```

#### 5. **Analytiques (Statistics)**

```
Statistique
├── nom, valeur, date

Rapport
├── titre, contenu
├── dateGeneration
└── periode
```

## 🔗 Propriétés Objet (Object Properties)

### Déchets et Types
| Propriété | Domain | Range | Description |
|-----------|--------|-------|-------------|
| `aType` | Dechet | TypeDechet | Lie un déchet à son type |

### Localisation
| Propriété | Domain | Range | Description |
|-----------|--------|-------|-------------|
| `localiseDans` | PointCollecte | Ville | Point dans une ville |
| `localiseDansQuartier` | PointCollecte | Quartier | Point dans un quartier |

### Points de Collecte
| Propriété | Domain | Range | Description |
|-----------|--------|-------|-------------|
| `accepte` | PointCollecte | TypeDechet | Types acceptés |

### Engagement
| Propriété | Domain | Range | Description |
|-----------|--------|-------|-------------|
| `participant` | Activite | Utilisateur | Participants |
| `aContribution` | Utilisateur | Contribution | Contributions |
| `aBadge` | Utilisateur | Badge | Badges gagnés |
| `aCommentaire` | Contribution | Commentaire | Commentaires |
| `aEffectue` | Utilisateur | Activite | Activités effectuées |
| `seLieuA` | Activite | PointCollecte | Lieu de l'activité |

## 📝 Propriétés de Données (Data Properties)

### Identification
| Propriété | Range | Description |
|-----------|-------|-------------|
| `nom` | String | Nom générique |
| `description` | String | Description générique |

### Contact
| Propriété | Range | Description |
|-----------|-------|-------------|
| `email` | String | Adresse email |
| `telephone` | String | Numéro de téléphone |
| `adresse` | String | Adresse postale |

### Géolocalisation
| Propriété | Range | Description |
|-----------|-------|-------------|
| `latitude` | Float | Latitude (WGS84) |
| `longitude` | Float | Longitude (WGS84) |

### Temporelles
| Propriété | Range | Description |
|-----------|-------|-------------|
| `dateCreation` | dateTime | Date de création |
| `dateActivite` | dateTime | Date de l'activité |

### Quantitatives
| Propriété | Range | Description |
|-----------|-------|-------------|
| `quantite` | Float | Quantité en kg |
| `unite` | String | Unité de mesure |
| `nombrePoints` | Integer | Nombre de points |

### Statut
| Propriété | Range | Description |
|-----------|-------|-------------|
| `statut` | String | État (acceptée/en attente/rejetée) |
| `horaires` | String | Horaires d'ouverture |

## 📊 Exemples de Requêtes SPARQL

### 1. Tous les points de collecte avec horaires

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?point ?nom ?adresse ?horaires ?telephone
WHERE {
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:horaires ?horaires .
  OPTIONAL { ?point wm:telephone ?telephone }
}
ORDER BY ?nom
```

### 2. Points de collecte à Paris acceptant déchets organiques

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?point ?nom ?adresse
WHERE {
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:localiseDans ?ville .
  ?ville wm:nom "Paris" .
  ?point wm:accepte wm:TypeOrganique .
}
```

### 3. Contributions par utilisateur

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>

SELECT ?utilisateur ?nom ?contributions (COUNT(?contrib) as ?total)
WHERE {
  ?utilisateur rdf:type wm:Utilisateur .
  ?utilisateur wm:nom ?nom .
  ?utilisateur wm:aContribution ?contrib .
}
GROUP BY ?utilisateur ?nom
ORDER BY DESC(?total)
```

### 4. Badges de récompense disponibles

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>

SELECT ?badge ?nom ?description
WHERE {
  ?badge rdf:type wm:Badge .
  ?badge wm:nom ?nom .
  OPTIONAL { ?badge wm:description ?description }
}
```

### 5. Activités dans le prochain mois

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>

SELECT ?activite ?nom ?date ?lieu
WHERE {
  ?activite rdf:type wm:Activite .
  ?activite wm:nom ?nom .
  ?activite wm:dateActivite ?date .
  OPTIONAL { ?activite wm:seLieuA ?lieu }
  FILTER (?date >= NOW() && ?date <= NOW() + "P30D"^^xsd:duration)
}
ORDER BY ?date
```

### 6. Statistiques d'engagement

```sparql
PREFIX wm: <http://www.semanticweb.org/waste-management/2025/1/#>

SELECT 
  (COUNT(DISTINCT ?utilisateur) as ?totalUsers)
  (COUNT(DISTINCT ?contribution) as ?totalContributions)
  (COUNT(DISTINCT ?badge) as ?badgesDistribues)
WHERE {
  ?utilisateur rdf:type wm:Utilisateur .
  OPTIONAL { ?utilisateur wm:aContribution ?contribution }
  OPTIONAL { ?utilisateur wm:aBadge ?badge }
}
```

## 🔄 Relations Clés

### Hiérarchies de Classes

```
Activite
├── Evenement (événements)
└── Defi (défis/challenges)

TypeDechet
├── DechetsOrganiques
├── DechetsRecyclables
├── DechetsHazardeux
└── DechetsEncombrants

PointCollecte
├── PointDecheterie
├── PointBac
└── PointCompostage

Destination
├── Ville
└── Quartier
```

## 🎯 Patterns d'Utilisation

### Pattern 1: Trouver des points proches d'une localité

```sparql
?point rdf:type wm:PointCollecte .
?point wm:localiseDans ?ville .
?ville wm:nom "Paris" .
?point wm:latitude ?lat .
?point wm:longitude ?lon .
```

### Pattern 2: Déchets acceptés par type

```sparql
?point wm:accepte ?typeDechet .
?typeDechet rdf:type wm:TypeDechet .
?typeDechet wm:nom ?nomType .
```

### Pattern 3: Contribution utilisateur

```sparql
?utilisateur wm:aContribution ?contrib .
?contrib wm:quantite ?quantite .
?contrib wm:unite ?unite .
?contrib wm:dateCreation ?date .
```

### Pattern 4: Activités avec participants

```sparql
?activite rdf:type wm:Activite .
?activite wm:participant ?utilisateur .
?utilisateur wm:nom ?nomUser .
?activite wm:seLieuA ?point .
?point wm:adresse ?adresse .
```

## 📈 Étendre l'Ontologie

### Ajouter un nouveau type de déchet

```xml
<owl:Class rdf:about="#DechetElectronique">
  <rdfs:subClassOf rdf:resource="#TypeDechet"/>
  <rdfs:label>Déchets Électroniques</rdfs:label>
  <rdfs:comment>Appareils et déchets électriques</rdfs:comment>
</owl:Class>
```

### Ajouter une nouvelle propriété

```xml
<owl:DatatypeProperty rdf:about="#capacite">
  <rdfs:label>Capacité</rdfs:label>
  <rdfs:domain rdf:resource="#PointCollecte"/>
  <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#float"/>
</owl:DatatypeProperty>
```

### Ajouter une instance

```xml
<owl:NamedIndividual rdf:about="#PointDecheterie_Lyon">
  <rdf:type rdf:resource="#PointDecheterie"/>
  <wm:nom>Déchèterie Nord Lyon</wm:nom>
  <wm:adresse>456 Avenue de la République, Lyon</wm:adresse>
  <wm:latitude>45.7640</wm:latitude>
  <wm:longitude>4.8357</wm:longitude>
  <wm:horaires>7h-19h</wm:horaires>
  <wm:localiseDans rdf:resource="#Lyon"/>
</owl:NamedIndividual>
```

## 🔍 Outils de Validation

Valider l'ontologie avec:
- **Protégé**: https://protege.stanford.edu/ (éditeur OWL)
- **Hermit**: Reasoner pour vérifier la cohérence
- **Fuseki UI**: http://localhost:3030 (tests SPARQL)

## 📚 Références

- [OWL 2 Specification](https://www.w3.org/TR/owl2-overview/)
- [RDF Specification](https://www.w3.org/RDF/)
- [SPARQL Tutorial](https://www.w3.org/TR/sparql11-query/)
- [Apache Jena Documentation](https://jena.apache.org/documentation/)

---

**Dernière mise à jour:** 2025-01-04
**Version:** 1.0.0
