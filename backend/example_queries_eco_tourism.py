# Exemples de Requêtes pour Tourisme Éco-responsable
# Conversions du langage naturel français en SPARQL

EXAMPLE_QUERIES = {
    # ================================
    # DESTINATIONS
    # ================================
    "Où puis-je voyager de manière durable?": {
        "type": "destinations",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?destination ?nom ?description ?certification
WHERE {
  ?destination rdf:type eco:Destination .
  ?destination wm:nom ?nom .
  OPTIONAL { ?destination wm:description ?description }
  OPTIONAL { ?destination eco:aCertification ?certification }
}
LIMIT 10"""
    },
    
    "Quelles sont les montagnes accessibles de manière écologique?": {
        "type": "destinations",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?montagne ?nom ?region
WHERE {
  ?montagne rdf:type eco:Montagne .
  ?montagne wm:nom ?nom .
  OPTIONAL { ?montagne wm:localiseDans ?region }
}"""
    },
    
    "Quelles plages proposent un tourisme responsable?": {
        "type": "destinations",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?plage ?nom ?certification ?impact
WHERE {
  ?plage rdf:type eco:Plage .
  ?plage wm:nom ?nom .
  OPTIONAL { ?plage eco:aCertification ?certification }
  OPTIONAL { ?plage eco:aEmpreinte ?impact }
}"""
    },
    
    # ================================
    # HÉBERGEMENTS
    # ================================
    "Où puis-je dormir de façon écologique?": {
        "type": "hebergements",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?hebergement ?nom ?type ?certification
WHERE {
  ?hebergement rdf:type eco:Hebergement .
  ?hebergement wm:nom ?nom .
  OPTIONAL { ?hebergement rdf:type ?type }
  OPTIONAL { ?hebergement eco:aCertification ?certification }
}
LIMIT 15"""
    },
    
    "Quels gîtes ruraux sont respectueux de l'environnement?": {
        "type": "hebergements",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?gite ?nom ?certification ?empreinte
WHERE {
  ?gite rdf:type eco:GiteRural .
  ?gite wm:nom ?nom .
  OPTIONAL { ?gite eco:aCertification ?certification }
  OPTIONAL { ?gite eco:aEmpreinte ?empreinte }
}"""
    },
    
    "Quels campings éco-responsables proposent des services?": {
        "type": "hebergements",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?camping ?nom ?services
WHERE {
  ?camping rdf:type eco:CampingEcoResponsable .
  ?camping wm:nom ?nom .
  OPTIONAL { ?camping wm:services ?services }
}"""
    },
    
    # ================================
    # ACTIVITÉS
    # ================================
    "Quelles activités sportives écologiques puis-je faire?": {
        "type": "activites",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?activite ?nom ?description ?lieu
WHERE {
  ?activite rdf:type eco:ActiviteSportive .
  ?activite wm:nom ?nom .
  OPTIONAL { ?activite wm:description ?description }
  OPTIONAL { ?activite eco:aLieu ?lieu }
}"""
    },
    
    "Où puis-je explorer la culture locale de manière responsable?": {
        "type": "activites",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?activite ?nom ?type ?region
WHERE {
  ?activite rdf:type eco:ActiviteCulturelle .
  ?activite wm:nom ?nom .
  OPTIONAL { ?activite rdf:type ?type }
  OPTIONAL { ?activite eco:aLieu ?region }
}"""
    },
    
    "Quels ateliers créatifs sont proposés?": {
        "type": "activites",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?atelier ?nom ?description ?duree
WHERE {
  ?atelier rdf:type eco:ActiviteEducative .
  ?atelier wm:nom ?nom .
  OPTIONAL { ?atelier wm:description ?description }
  OPTIONAL { ?atelier eco:duree ?duree }
}"""
    },
    
    "Où puis-je méditer et me détendre?": {
        "type": "activites",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?activite ?nom ?lieu ?benefices
WHERE {
  ?activite rdf:type eco:ActiviteDetente .
  ?activite wm:nom ?nom .
  OPTIONAL { ?activite eco:aLieu ?lieu }
  OPTIONAL { ?activite wm:description ?benefices }
}"""
    },
    
    # ================================
    # TRANSPORTS
    # ================================
    "Quel transport est le plus écologique pour voyager?": {
        "type": "transports_eco",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?transport ?nom ?co2 ?niveau
WHERE {
  ?transport rdf:type eco:Transport .
  ?transport wm:nom ?nom .
  ?transport eco:aEmpreinte ?empreinte .
  ?empreinte eco:kgCO2 ?co2 .
  ?empreinte rdf:type ?niveau
}
ORDER BY ?co2"""
    },
    
    "Quelle est l'empreinte carbone du train vs l'avion?": {
        "type": "transports_eco",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?transport ?nom ?co2km
WHERE {
  { ?transport rdf:type eco:Train }
  UNION { ?transport rdf:type eco:Avion }
  ?transport wm:nom ?nom .
  ?transport eco:aEmpreinte ?empreinte .
  ?empreinte eco:kgCO2 ?co2km
}"""
    },
    
    "Existe-t-il des bus ou des vélos électriques?": {
        "type": "transports_eco",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?transport ?nom ?co2
WHERE {
  { ?transport rdf:type eco:Bus }
  UNION { ?transport rdf:type eco:VelosElectrique }
  ?transport wm:nom ?nom .
  OPTIONAL { 
    ?transport eco:aEmpreinte ?empreinte .
    ?empreinte eco:kgCO2 ?co2
  }
}"""
    },
    
    # ================================
    # CERTIFICATIONS
    # ================================
    "Quels sont les labels écologiques reconnus?": {
        "type": "certifications",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?cert ?nom ?description ?type
WHERE {
  ?cert rdf:type eco:CertificatEco .
  ?cert wm:nom ?nom .
  OPTIONAL { ?cert wm:description ?description }
  OPTIONAL { ?cert rdf:type ?type }
}"""
    },
    
    "Qui dispose du label GreenGlobe?": {
        "type": "certifications",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?entity ?nom ?type
WHERE {
  ?entity eco:aCertification ?cert .
  ?cert rdf:type eco:GreenGlobe .
  ?entity wm:nom ?nom .
  ?entity rdf:type ?type
}"""
    },
    
    # ================================
    # PROFILS VOYAGEURS
    # ================================
    "Quels profils de voyageurs existentent?": {
        "type": "voyageurs",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?profil ?label ?description
WHERE {
  ?profil rdf:type eco:ProfilVoyageur .
  OPTIONAL { ?profil rdfs:label ?label }
  OPTIONAL { ?profil rdfs:comment ?description }
}"""
    },
    
    "Je suis aventurier, que me recommandez-vous?": {
        "type": "recommandations",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?activite ?nom ?description
WHERE {
  ?activite rdf:type eco:ActiviteSportive .
  ?activite wm:nom ?nom .
  OPTIONAL { ?activite wm:description ?description }
}
LIMIT 10"""
    },
    
    # ================================
    # IMPACTS ENVIRONNEMENTAUX
    # ================================
    "Quel est l'impact environnemental de mon voyage?": {
        "type": "impacts_eco",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?element ?nom ?co2 ?niveau
WHERE {
  ?element eco:aEmpreinte ?impact .
  ?element wm:nom ?nom .
  ?impact eco:kgCO2 ?co2 .
  ?impact rdf:type ?niveau
}
ORDER BY DESC(?co2)"""
    },
    
    "Quel transport a le moins d'impact?": {
        "type": "impacts_eco",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?transport ?nom ?co2
WHERE {
  ?transport rdf:type eco:Transport .
  ?transport wm:nom ?nom .
  ?transport eco:aEmpreinte ?empreinte .
  ?empreinte eco:kgCO2 ?co2
}
ORDER BY ?co2
LIMIT 5"""
    },
    
    "Quelles destinations ont le moins d'impact écologique?": {
        "type": "impacts_eco",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?destination ?nom ?impact ?niveau
WHERE {
  ?destination rdf:type eco:Destination .
  ?destination wm:nom ?nom .
  ?destination eco:aEmpreinte ?impact .
  ?impact rdf:type eco:ImpactFaible
}"""
    },
    
    # ================================
    # REQUÊTES COMPLEXES
    # ================================
    "Recommandez-moi un voyage durable pour la famille?": {
        "type": "recommandations",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?destination ?hebergement ?activite ?co2_total ?score
WHERE {
  ?destination rdf:type eco:Destination .
  ?hebergement rdf:type eco:Hebergement .
  ?activite rdf:type eco:ActiviteTouristique .
  
  ?destination eco:aEmpreinte ?dest_impact .
  ?dest_impact eco:kgCO2 ?dest_co2 .
  
  ?hebergement eco:aEmpreinte ?heb_impact .
  ?heb_impact eco:kgCO2 ?heb_co2 .
  
  ?activite eco:aEmpreinte ?act_impact .
  ?act_impact eco:kgCO2 ?act_co2 .
  
  BIND(?dest_co2 + ?heb_co2 + ?act_co2 AS ?co2_total)
  
  ?destination eco:aCertification ?cert .
  ?hebergement eco:aCertification ?cert .
}
LIMIT 5"""
    },
    
    "Quel est le meilleur package éco-responsable?": {
        "type": "recommandations",
        "sparql": """PREFIX eco: <http://www.semanticweb.org/eco-tourism/2025/1/#>
SELECT ?package ?destination ?hebergement ?transport ?score
WHERE {
  ?package rdf:type eco:PackageTourisme .
  ?package eco:recommande ?destination .
  ?package eco:recommande ?hebergement .
  ?package eco:recommande ?transport .
  ?package eco:scoreRecommandation ?score .
  
  ?destination rdf:type eco:Destination .
  ?hebergement rdf:type eco:Hebergement .
  ?transport rdf:type eco:Transport .
}
ORDER BY DESC(?score)
LIMIT 10"""
    },
}

# Exemples de questions en langage naturel
NL_QUESTIONS = [
    "Où puis-je voyager de manière durable?",
    "Quel transport est le plus écologique?",
    "Quels hébergements respectent l'environnement?",
    "Recommandez-moi un voyage éco-responsable",
    "Quel est l'impact carbone de l'avion?",
    "Où faire de la randonnée responsable?",
    "Je veux méditer en nature, où aller?",
    "Quelles activités culturelles locales?",
    "Quel label écologique choisir?",
    "Comment réduire mon empreinte carbone?",
]
