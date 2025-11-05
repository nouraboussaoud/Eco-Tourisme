import { useState } from 'react'
import axios from 'axios'
import './QueryTest.css'

function QueryTest() {
  const [question, setQuestion] = useState('')
  const [sparqlQuery, setSparqlQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [executionTime, setExecutionTime] = useState(0)

  const exampleQuestions = [
    "Trouve toutes les destinations avec une faible empreinte carbone",
    "Quels sont les hébergements écologiques disponibles?",
    "Liste les activités de randonnée",
    "Montre-moi les destinations certifiées éco-tourisme",
    "Quels sont les voyageurs intéressés par le bien-être?",
    "Trouve les destinations en Tunisie",
    "Quelles sont les activités sportives disponibles?",
    "Liste tous les hébergements avec certification Green Globe"
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSparqlQuery('')
    setResults([])
    setExecutionTime(0)

    try {
      const response = await axios.post('http://localhost:8000/query/nl', {
        question: question
      })

      setSparqlQuery(response.data.sparql_query)
      setResults(response.data.results || [])
      setExecutionTime(response.data.execution_time || 0)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="query-test">
      <div className="test-header">
        <h2>
          <i className="fas fa-flask"></i>
          Test du Modèle NL → SPARQL
        </h2>
        <p>Testez la conversion de langage naturel en requêtes SPARQL sémantiques</p>
      </div>

      <div className="test-container">
        <div className="examples-section">
          <h3>
            <i className="fas fa-lightbulb"></i>
            Questions d'exemple
          </h3>
          <div className="example-buttons">
            {exampleQuestions.map((q, idx) => (
              <button
                key={idx}
                className="example-btn"
                onClick={() => setQuestion(q)}
                title="Cliquez pour utiliser cette question"
              >
                <i className="fas fa-comment-dots"></i>
                {q}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="query-form">
          <div className="form-group">
            <label>
              <i className="fas fa-keyboard"></i>
              Votre question en langage naturel:
            </label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ex: Trouve toutes les destinations avec une faible empreinte carbone"
              rows={4}
              required
            />
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? (
              <>
                <i className="fas fa-spinner fa-spin"></i>
                Conversion en cours...
              </>
            ) : (
              <>
                <i className="fas fa-magic"></i>
                Convertir en SPARQL
              </>
            )}
          </button>
        </form>

        {error && (
          <div className="error-box">
            <i className="fas fa-exclamation-triangle"></i>
            <div>
              <strong>Erreur:</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {sparqlQuery && (
          <div className="result-section sparql-section">
            <div className="section-header">
              <h3>
                <i className="fas fa-code"></i>
                Requête SPARQL générée
              </h3>
              {executionTime > 0 && (
                <span className="execution-time">
                  <i className="fas fa-clock"></i>
                  {executionTime.toFixed(3)}s
                </span>
              )}
            </div>
            <pre className="sparql-output">{sparqlQuery}</pre>
            <button
              className="copy-btn"
              onClick={() => {
                navigator.clipboard.writeText(sparqlQuery)
                alert('Requête SPARQL copiée!')
              }}
            >
              <i className="fas fa-copy"></i>
              Copier la requête
            </button>
          </div>
        )}

        {results.length > 0 && (
          <div className="result-section results-section">
            <h3>
              <i className="fas fa-database"></i>
              Résultats de la requête ({results.length})
            </h3>
            <div className="results-table-wrapper">
              <table className="results-table">
                <thead>
                  <tr>
                    {Object.keys(results[0]).map((key) => (
                      <th key={key}>
                        <i className="fas fa-tag"></i>
                        {key}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {results.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((val, i) => (
                        <td key={i}>{val}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {sparqlQuery && results.length === 0 && !error && !loading && (
          <div className="no-results">
            <i className="fas fa-info-circle"></i>
            <p>La requête a été exécutée mais n'a retourné aucun résultat.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default QueryTest
