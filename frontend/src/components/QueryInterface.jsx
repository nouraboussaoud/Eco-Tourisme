import { useState } from 'react'
import axios from 'axios'
import './QueryInterface.css'

function QueryInterface({ apiUrl }) {
  const [question, setQuestion] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [sparqlQuery, setSparqlQuery] = useState('')

  const exampleQuestions = [
    "Quels sont les points de collecte à Paris?",
    "Liste tous les types de déchets",
    "Quels déchets sont acceptés aux points de collecte?",
    "Quelles sont toutes les villes?"
  ]

  const handleQuery = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    try {
      setLoading(true)
      setError(null)
      const response = await axios.post(`${apiUrl}/query`, { question })
      
      setResults(response.data.results)
      setSparqlQuery(response.data.sparql_query)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la requête')
      setResults(null)
    } finally {
      setLoading(false)
    }
  }

  const handleExampleClick = (exampleQuestion) => {
    setQuestion(exampleQuestion)
  }

  return (
    <div className="query-interface">
      <div className="query-card">
        <h2>
          <i className="fas fa-search"></i>
          Recherche en Langage Naturel
        </h2>
        <p className="subtitle">Posez vos questions en français, nous les convertissons en requêtes SPARQL</p>

        <form onSubmit={handleQuery} className="query-form">
          <div className="input-group">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Posez votre question ici... Ex: Quels sont les points de collecte?"
              className="query-input"
              disabled={loading}
            />
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <i className="fas fa-spinner fa-spin"></i> : <i className="fas fa-search"></i>}
              {loading ? 'Recherche...' : 'Rechercher'}
            </button>
          </div>
        </form>

        <div className="examples">
          <h4>Questions d'exemple:</h4>
          <div className="example-buttons">
            {exampleQuestions.map((example, idx) => (
              <button
                key={idx}
                className="example-btn"
                onClick={() => handleExampleClick(example)}
              >
                <i className="fas fa-lightbulb"></i>
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>

      {sparqlQuery && (
        <div className="sparql-query">
          <h3>Requête SPARQL générée:</h3>
          <pre><code>{sparqlQuery}</code></pre>
        </div>
      )}

      {error && (
        <div className="error-box">
          <i className="fas fa-exclamation-triangle"></i>
          <span>{error}</span>
        </div>
      )}

      {results && (
        <div className="results-card">
          <h3>
            <i className="fas fa-check-circle"></i>
            Résultats ({results.length} trouvés)
          </h3>
          {results.length > 0 ? (
            <div className="results-table">
              <table>
                <thead>
                  <tr>
                    {Object.keys(results[0]).map(key => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {results.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((value, vIdx) => (
                        <td key={vIdx}>
                          {typeof value === 'string' && value.includes('http') ? (
                            <a href={value} target="_blank" rel="noopener noreferrer" className="uri-link">
                              {value.split('#')[1] || value.split('/').pop()}
                            </a>
                          ) : (
                            value
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="no-results">
              <i className="fas fa-search"></i>
              <p>Aucun résultat trouvé</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default QueryInterface
