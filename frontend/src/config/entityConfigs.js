// Configuration pour chaque type d'entité

export const entityConfigs = {
  destinations: {
    title: 'Gestion des Destinations',
    singleName: 'une Destination',
    description: 'Explorez et gérez les destinations éco-responsables',
    icon: 'fas fa-map-marked-alt',
    className: 'Destination',
    defaultQuestion: 'Quelles sont les destinations éco-responsables?',
    
    fields: [
      { 
        name: 'nom', 
        label: 'Nom de la destination', 
        type: 'text',
        placeholder: 'Ex: Parc National Ichkeul',
        required: true 
      },
      { 
        name: 'description', 
        label: 'Description', 
        type: 'text',
        placeholder: 'Ex: Magnifique réserve naturelle protégée',
        required: true 
      },
      { 
        name: 'region', 
        label: 'Région', 
        type: 'text',
        placeholder: 'Ex: Bizerte',
        required: false 
      },
      { 
        name: 'pays', 
        label: 'Pays', 
        type: 'text',
        placeholder: 'Ex: Tunisie',
        required: false 
      }
    ],
    
    propertyMap: {
      'nom': 'rdfs:label',
      'description': 'rdfs:comment',
      'region': 'eco:localiseDans',
      'pays': 'eco:pays'
    },
    
    displayFields: ['nom', 'description', 'region', 'destination']
  },

  hebergements: {
    title: 'Gestion des Hébergements',
    singleName: 'un Hébergement',
    description: 'Découvrez et gérez les hébergements écologiques',
    icon: 'fas fa-hotel',
    className: 'Hebergement',
    defaultQuestion: 'Quels sont les hébergements éco-responsables?',
    
    fields: [
      { 
        name: 'nom', 
        label: 'Nom de l\'hébergement', 
        type: 'text',
        placeholder: 'Ex: Eco-Lodge Dar Bhar',
        required: true 
      },
      { 
        name: 'description', 
        label: 'Description', 
        type: 'text',
        placeholder: 'Ex: Hébergement écologique avec vue sur mer',
        required: true 
      },
      { 
        name: 'prix', 
        label: 'Prix par nuit (€)', 
        type: 'number',
        placeholder: 'Ex: 120',
        required: false 
      },
      { 
        name: 'capacite', 
        label: 'Capacité (personnes)', 
        type: 'number',
        placeholder: 'Ex: 4',
        required: false 
      }
    ],
    
    propertyMap: {
      'nom': 'rdfs:label',
      'description': 'rdfs:comment',
      'prix': 'eco:prixNuit',
      'capacite': 'eco:capacite'
    },
    
    displayFields: ['nom', 'description', 'certification', 'hebergement']
  },

  activites: {
    title: 'Gestion des Activités',
    singleName: 'une Activité',
    description: 'Explorez et gérez les activités touristiques durables',
    icon: 'fas fa-hiking',
    className: 'ActiviteTouristique',
    defaultQuestion: 'Quelles sont les activités disponibles?',
    
    fields: [
      { 
        name: 'nom', 
        label: 'Nom de l\'activité', 
        type: 'text',
        placeholder: 'Ex: Randonnée Parc Ichkeul',
        required: true 
      },
      { 
        name: 'description', 
        label: 'Description', 
        type: 'text',
        placeholder: 'Ex: Découverte de la faune et flore locale',
        required: true 
      },
      { 
        name: 'duree', 
        label: 'Durée', 
        type: 'text',
        placeholder: 'Ex: 4 heures',
        required: false 
      },
      { 
        name: 'prix', 
        label: 'Prix (€)', 
        type: 'number',
        placeholder: 'Ex: 25',
        required: false 
      }
    ],
    
    propertyMap: {
      'nom': 'rdfs:label',
      'description': 'rdfs:comment',
      'duree': 'eco:duree',
      'prix': 'eco:cout'
    },
    
    displayFields: ['nom', 'description', 'activite']
  },

  certifications: {
    title: 'Gestion des Certifications',
    singleName: 'une Certification',
    description: 'Gérez les certifications et labels écologiques',
    icon: 'fas fa-certificate',
    className: 'CertificatEco',
    defaultQuestion: 'Quelles sont les certifications écologiques?',
    
    fields: [
      { 
        name: 'nom', 
        label: 'Nom de la certification', 
        type: 'text',
        placeholder: 'Ex: Green Key',
        required: true 
      },
      { 
        name: 'description', 
        label: 'Description', 
        type: 'text',
        placeholder: 'Ex: Label international pour l\'environnement',
        required: true 
      },
      { 
        name: 'organisme', 
        label: 'Organisme certificateur', 
        type: 'text',
        placeholder: 'Ex: Foundation for Environmental Education',
        required: false 
      }
    ],
    
    propertyMap: {
      'nom': 'rdfs:label',
      'description': 'rdfs:comment',
      'organisme': 'eco:organismeEmetteur'
    },
    
    displayFields: ['nom', 'description', 'cert']
  }
}
