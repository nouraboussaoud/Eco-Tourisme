# Example SPARQL queries for testing
from config import ONTOLOGY_NS

ns = ONTOLOGY_NS

EXAMPLE_QUERIES = {
    "all_collection_points": f"""PREFIX wm: <{ns}>
SELECT ?point ?nom ?adresse ?horaires
WHERE {{
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:horaires ?horaires .
}}""",

    "collection_points_in_paris": f"""PREFIX wm: <{ns}>
SELECT ?point ?nom ?adresse ?latitude ?longitude
WHERE {{
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?nom .
  ?point wm:adresse ?adresse .
  ?point wm:latitude ?latitude .
  ?point wm:longitude ?longitude .
  ?point wm:localiseDans ?ville .
  ?ville wm:nom "Paris" .
}}""",

    "all_waste_types": f"""PREFIX wm: <{ns}>
SELECT ?type ?nom ?description
WHERE {{
  ?type rdf:type wm:TypeDechet .
  ?type wm:nom ?nom .
  OPTIONAL {{ ?type wm:description ?description }}
}}""",

    "accepted_waste_types": f"""PREFIX wm: <{ns}>
SELECT DISTINCT ?point ?pointNom ?typeNom
WHERE {{
  ?point rdf:type wm:PointCollecte .
  ?point wm:nom ?pointNom .
  ?point wm:accepte ?type .
  ?type wm:nom ?typeNom .
}}""",

    "all_cities": f"""PREFIX wm: <{ns}>
SELECT DISTINCT ?ville ?nom
WHERE {{
  ?ville rdf:type wm:Ville .
  ?ville wm:nom ?nom .
}}""",

    "all_activities": f"""PREFIX wm: <{ns}>
SELECT ?activite ?nom ?description ?date
WHERE {{
  ?activite rdf:type wm:Activite .
  ?activite wm:nom ?nom .
  OPTIONAL {{ ?activite wm:description ?description }}
  OPTIONAL {{ ?activite wm:dateActivite ?date }}
}}""",

    "all_badges": f"""PREFIX wm: <{ns}>
SELECT ?badge ?nom ?description
WHERE {{
  ?badge rdf:type wm:Badge .
  ?badge wm:nom ?nom .
  OPTIONAL {{ ?badge wm:description ?description }}
}}""",

    "user_contributions": f"""PREFIX wm: <{ns}>
SELECT ?utilisateur ?nom ?contribution ?contribDesc ?date
WHERE {{
  ?utilisateur rdf:type wm:Utilisateur .
  ?utilisateur wm:nom ?nom .
  ?utilisateur wm:aContribution ?contribution .
  OPTIONAL {{ ?contribution wm:description ?contribDesc }}
  OPTIONAL {{ ?contribution wm:dateCreation ?date }}
}}""",

    "community_stats": f"""PREFIX wm: <{ns}>
SELECT (COUNT(DISTINCT ?utilisateur) as ?totalUsers) (COUNT(DISTINCT ?activite) as ?totalActivities)
WHERE {{
  ?utilisateur rdf:type wm:Utilisateur .
  ?activite rdf:type wm:Activite .
}}""",
}
