import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './EntityManager.css'

const API_URL = 'http://localhost:8000'

function EntityManager({ entityType, entityConfig }) {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sparqlQuery, setSparqlQuery] = useState('')
  const [jsonResults, setJsonResults] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({})
  const [executionTime, setExecutionTime] = useState(0)

  useEffect(() => {
    loadData()
  }, [entityType])

  const loadData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const startTime = performance.now()
      const response = await axios.get(`${API_URL}/${entityType}`)
      const endTime = performance.now()
      
      setExecutionTime(((endTime - startTime) / 1000).toFixed(3))
      
      // Récupérer la requête SPARQL depuis le backend (simulation)
      const sparqlResponse = await axios.post(`${API_URL}/query`, {
        question: entityConfig.defaultQuestion
      })
      
      setSparqlQuery(sparqlResponse.data.sparql_query)
      setJsonResults(response.data)
      setData(response.data[entityType] || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement')
      console.error('Erreur:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const sparqlInsert = generateInsertQuery(formData)
      setSparqlQuery(sparqlInsert)
      
      const params = new URLSearchParams()
      params.append('query', sparqlInsert)
      
      await axios.post(`${API_URL}/sparql`, params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      
      alert('✅ Entité créée avec succès!')
      setShowForm(false)
      setFormData({})
      loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la création')
    } finally {
      setLoading(false)
    }
  }

  const generateInsertQuery = (data) => {
    const ns = 'http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco#'
    const timestamp = Date.now()
    const id = `${entityType}_${timestamp}`
    
    let triples = `eco:${id} rdf:type eco:${entityConfig.className}`
    
    const entries = Object.entries(data).filter(([key, value]) => value)
    if (entries.length > 0) {
      triples += ' ;'
      entries.forEach(([key, value], index) => {
        const property = entityConfig.propertyMap[key] || 'rdfs:label'
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

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('✅ Requête copiée dans le presse-papiers!')
  }

  return (
    <div className="entity-manager">
      {/* Header */}
      <div className="entity-header">
        <h2>
          <i className={entityConfig.icon}></i>
          {entityConfig.title}
        </h2>
        <p>{entityConfig.description}</p>
      </div>

      {/* Action Buttons */}
      <div className="entity-actions">
        <button 
          className="btn-primary" 
          onClick={loadData}
          disabled={loading}
        >
          <i className="fas fa-sync-alt"></i>
          Lire (SELECT)
        </button>
        <button 
          className="btn-success" 
          onClick={() => setShowForm(!showForm)}
        >
          <i className="fas fa-plus"></i>
          Créer (INSERT)
        </button>
      </div>

      {/* Create Form */}
      {showForm && (
        <div className="entity-form">
          <h3>
            <i className="fas fa-edit"></i>
            Créer {entityConfig.singleName}
          </h3>
          <form onSubmit={handleCreate}>
            {entityConfig.fields.map(field => (
              <div key={field.name} className="form-group">
                <label>{field.label}</label>
                <input
                  type={field.type || 'text'}
                  value={formData[field.name] || ''}
                  onChange={(e) => setFormData({
                    ...formData,
                    [field.name]: e.target.value
                  })}
                  placeholder={field.placeholder}
                  required={field.required !== false}
                />
              </div>
            ))}
            <div className="form-actions">
              <button type="submit" className="btn-success" disabled={loading}>
                <i className="fas fa-save"></i>
                Créer
              </button>
              <button 
                type="button" 
                className="btn-secondary" 
                onClick={() => setShowForm(false)}
              >
                Annuler
              </button>
            </div>
          </form>
        </div>
      )}

      {/* SPARQL Query Display */}
      {sparqlQuery && (
        <div className="sparql-section">
          <div className="section-header">
            <h3>
              <i className="fas fa-code"></i>
              Requête SPARQL générée
            </h3>
            <span className="execution-time">⏱️ {executionTime}s</span>
          </div>
          <div className="sparql-code">
            <pre><code>{sparqlQuery}</code></pre>
          </div>
          <button 
            className="btn-copy" 
            onClick={() => copyToClipboard(sparqlQuery)}
          >
            <i className="fas fa-copy"></i>
            Copier la requête
          </button>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="loading">
          <i className="fas fa-spinner fa-spin"></i>
          Chargement...
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="error-message">
          <i className="fas fa-exclamation-circle"></i>
          {error}
        </div>
      )}

      {/* JSON Results */}
      {!loading && jsonResults && (
        <div className="json-section">
          <h3>
            <i className="fas fa-code"></i>
            Résultats JSON
          </h3>
          <div className="json-viewer">
            <pre>{JSON.stringify(jsonResults, null, 2)}</pre>
          </div>
        </div>
      )}

      {/* Formatted Results */}
      {!loading && data.length > 0 && (
        <div className="results-section">
          <h3>
            <i className="fas fa-table"></i>
            Résultats ({data.length} élément{data.length > 1 ? 's' : ''})
          </h3>
          <div className="results-table">
            <table>
              <thead>
                <tr>
                  {entityConfig.displayFields.map(field => (
                    <th key={field}>{field}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((item, index) => (
                  <tr key={index}>
                    {entityConfig.displayFields.map(field => (
                      <td key={field}>{item[field] || 'N/A'}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* No Results */}
      {!loading && data.length === 0 && !error && (
        <div className="no-results">
          <i className="fas fa-info-circle"></i>
          <p>La requête a été exécutée mais n'a retourné aucun résultat.</p>
          <p>Utilisez le bouton "Créer" pour ajouter des données.</p>
        </div>
      )}
    </div>
  )
}

export default EntityManager
