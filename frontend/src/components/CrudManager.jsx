import { useState } from 'react'
import axios from 'axios'
import './CrudManager.css'

const API_URL = 'http://localhost:8000'

function CrudManager() {
  const [selectedEntity, setSelectedEntity] = useState('destinations')
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({})
  const [showForm, setShowForm] = useState(false)
  const [editMode, setEditMode] = useState(false)

  const entities = {
    destinations: {
      name: 'Destinations',
      icon: 'fa-map-marked-alt',
      endpoint: '/destinations',
      fields: ['nom', 'description', 'localiseDans', 'scoreDurabilite']
    },
    hebergements: {
      name: 'Hébergements',
      icon: 'fa-hotel',
      endpoint: '/hebergements',
      fields: ['nom', 'type', 'description', 'localiseDans', 'scoreDurabilite', 'certification']
    },
    activites: {
      name: 'Activités',
      icon: 'fa-running',
      endpoint: '/activites',
      fields: ['nom', 'description', 'type', 'kgCO2', 'profileRecommande']
    },
    certifications: {
      name: 'Certifications',
      icon: 'fa-certificate',
      endpoint: '/certifications',
      fields: ['nom', 'description', 'criteres']
    }
  }

  const handleRead = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_URL}${entities[selectedEntity].endpoint}`)
      setData(response.data[selectedEntity] || response.data[Object.keys(response.data)[0]] || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la récupération des données')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      // Create SPARQL INSERT query
      const sparqlInsert = generateInsertQuery(selectedEntity, formData)
      
      // Envoyer avec URLSearchParams pour FastAPI
      const params = new URLSearchParams()
      params.append('query', sparqlInsert)
      
      await axios.post(`${API_URL}/sparql`, params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      
      alert('Entité créée avec succès!')
      setShowForm(false)
      setFormData({})
      handleRead()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la création')
      console.error('Erreur CRUD:', err.response?.data)
    } finally {
      setLoading(false)
    }
  }

  const generateInsertQuery = (entity, data) => {
    const ns = 'http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#'
    const timestamp = Date.now()
    const id = `${entity}_${timestamp}`
    
    // Mapping des entités plurielles vers les classes OWL
    const classMap = {
      'destinations': 'Destination',
      'hebergements': 'Hebergement',
      'activites': 'ActiviteTouristique',
      'certifications': 'CertificatEco'
    }
    
    const className = classMap[entity] || 'Destination'
    
    // Créer les triples RDF avec mapping des propriétés
    const propertyMap = {
      'nom': 'rdfs:label',
      'description': 'rdfs:comment',
      'region': 'eco:localiseDans',
      'type': 'eco:typeDestination',
      'prix': 'eco:prixNuit',
      'capacite': 'eco:capacite',
      'duree': 'eco:duree'
    }
    
    let triples = `eco:${id} rdf:type eco:${className}`
    
    const entries = Object.entries(data).filter(([key, value]) => value)
    if (entries.length > 0) {
      triples += ' ;'
      entries.forEach(([key, value], index) => {
        const property = propertyMap[key] || 'rdfs:label'
        const isLast = index === entries.length - 1
        triples += `\n    ${property} "${value}"${isLast ? ' .' : ' ;'}`
      })
    } else {
      triples += ' .'
    }
    
    return `PREFIX eco: <${ns}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
  ${triples}
}`
  }

  const handleDelete = async (item) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cet élément?')) return
    
    // For this demo, we'll just show an alert
    // In production, you'd implement a SPARQL DELETE query
    alert('Fonctionnalité de suppression à implémenter avec SPARQL DELETE')
  }

  return (
    <div className="crud-manager">
      <div className="crud-header">
        <h2>
          <i className="fas fa-database"></i>
          Gestionnaire CRUD des Entités
        </h2>
        <p>Testez les opérations CRUD (Create, Read, Update, Delete) sur les entités de l'ontologie</p>
      </div>

      <div className="crud-container">
        {/* Entity Selector */}
        <div className="entity-selector">
          <h3>
            <i className="fas fa-list"></i>
            Sélectionner une Entité
          </h3>
          <div className="entity-grid">
            {Object.entries(entities).map(([key, entity]) => (
              <button
                key={key}
                className={`entity-btn ${selectedEntity === key ? 'active' : ''}`}
                onClick={() => {
                  setSelectedEntity(key)
                  setData([])
                  setError(null)
                }}
              >
                <i className={`fas ${entity.icon}`}></i>
                <span>{entity.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* CRUD Actions */}
        <div className="crud-actions">
          <button className="action-btn read-btn" onClick={handleRead} disabled={loading}>
            <i className="fas fa-search"></i>
            Lire (SELECT)
          </button>
          <button 
            className="action-btn create-btn" 
            onClick={() => {
              setShowForm(!showForm)
              setEditMode(false)
              setFormData({})
            }}
          >
            <i className="fas fa-plus"></i>
            Créer (INSERT)
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-box">
            <i className="fas fa-exclamation-triangle"></i>
            <span>{error}</span>
          </div>
        )}

        {/* Create/Update Form */}
        {showForm && (
          <div className="crud-form">
            <h3>
              <i className="fas fa-edit"></i>
              {editMode ? 'Modifier' : 'Créer'} {entities[selectedEntity].name}
            </h3>
            <form onSubmit={handleCreate}>
              {entities[selectedEntity].fields.map(field => (
                <div key={field} className="form-group">
                  <label>{field}</label>
                  <input
                    type="text"
                    value={formData[field] || ''}
                    onChange={(e) => setFormData({...formData, [field]: e.target.value})}
                    placeholder={`Entrer ${field}`}
                    required
                  />
                </div>
              ))}
              <div className="form-actions">
                <button type="submit" className="submit-btn" disabled={loading}>
                  <i className="fas fa-save"></i>
                  {loading ? 'Enregistrement...' : 'Enregistrer'}
                </button>
                <button 
                  type="button" 
                  className="cancel-btn"
                  onClick={() => {
                    setShowForm(false)
                    setFormData({})
                  }}
                >
                  <i className="fas fa-times"></i>
                  Annuler
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Data Display */}
        {loading && (
          <div className="loading-box">
            <i className="fas fa-spinner fa-spin"></i>
            <p>Chargement...</p>
          </div>
        )}

        {!loading && data.length > 0 && (
          <div className="data-display">
            <div className="data-header">
              <h3>
                <i className="fas fa-table"></i>
                Résultats ({data.length} éléments)
              </h3>
            </div>
            <div className="data-table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    {data[0] && Object.keys(data[0]).map(key => (
                      <th key={key}>{key}</th>
                    ))}
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((item, idx) => (
                    <tr key={idx}>
                      {Object.values(item).map((value, i) => (
                        <td key={i}>{value}</td>
                      ))}
                      <td>
                        <div className="action-buttons">
                          <button 
                            className="btn-icon edit"
                            onClick={() => {
                              setFormData(item)
                              setShowForm(true)
                              setEditMode(true)
                            }}
                            title="Modifier"
                          >
                            <i className="fas fa-edit"></i>
                          </button>
                          <button 
                            className="btn-icon delete"
                            onClick={() => handleDelete(item)}
                            title="Supprimer"
                          >
                            <i className="fas fa-trash"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {!loading && !error && data.length === 0 && selectedEntity && (
          <div className="empty-state">
            <i className="fas fa-inbox"></i>
            <p>Aucune donnée disponible. Cliquez sur "Lire" pour charger les données.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default CrudManager
