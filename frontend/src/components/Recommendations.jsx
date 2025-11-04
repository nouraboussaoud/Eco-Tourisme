import { useState } from 'react'
import axios from 'axios'
import './Recommendations.css'

function Recommendations({ apiUrl }) {
  const [selectedProfile, setSelectedProfile] = useState('Adventure')
  const [destination, setDestination] = useState('Paris')
  const [budget, setBudget] = useState(1000)
  const [carbonPriority, setCarbonPriority] = useState(false)
  const [days, setDays] = useState(3)
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [profiles, setProfiles] = useState([])

  React.useEffect(() => {
    const fetchProfiles = async () => {
      try {
        const res = await axios.get(`${apiUrl}/recommendation/profiles`)
        setProfiles(res.data.profiles || [])
      } catch (err) {
        console.error('Error fetching profiles:', err)
      }
    }
    fetchProfiles()
  }, [apiUrl])

  const handleGenerateRecommendation = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${apiUrl}/recommendation/generate`, {
        params: {
          profile: selectedProfile,
          destination,
          budget,
          carbon_priority: carbonPriority,
          days
        }
      })
      setRecommendation(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la génération')
      setRecommendation(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="recommendations-page">
      <div className="recommendations-form-card">
        <h2>
          <i className="fas fa-magic"></i>
          Recommandation Personnalisée
        </h2>
        <p className="subtitle">Découvrez des voyages adaptés à vos préférences et à vos valeurs écologiques</p>

        <form onSubmit={handleGenerateRecommendation} className="rec-form">
          <div className="form-row">
            <div className="form-group">
              <label>Profil de voyageur</label>
              <select
                value={selectedProfile}
                onChange={(e) => setSelectedProfile(e.target.value)}
                className="form-input"
              >
                {profiles.map(profile => (
                  <option key={profile.id} value={profile.id}>
                    {profile.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Destination</label>
              <input
                type="text"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                placeholder="Ex: Paris, Lyon..."
                className="form-input"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Budget (€)</label>
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Durée (jours)</label>
              <input
                type="number"
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                min="1"
                max="30"
                className="form-input"
              />
            </div>
          </div>

          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                checked={carbonPriority}
                onChange={(e) => setCarbonPriority(e.target.checked)}
              />
              <span>Priorité à la réduction de l'empreinte carbone</span>
            </label>
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? (
              <>
                <i className="fas fa-spinner fa-spin"></i>
                Génération en cours...
              </>
            ) : (
              <>
                <i className="fas fa-magic"></i>
                Générer ma recommandation
              </>
            )}
          </button>
        </form>

        {error && (
          <div className="error-box">
            <i className="fas fa-exclamation-triangle"></i>
            <span>{error}</span>
          </div>
        )}
      </div>

      {recommendation && (
        <div className="recommendation-result">
          <div className="result-header">
            <h2>Votre Recommandation Personnalisée</h2>
            <div className="score-badge">
              <span className="score">{recommendation.recommendation_score}</span>
              <span className="label">Score</span>
            </div>
          </div>

          <div className="reasons-box">
            <h3>Pourquoi cette recommandation ?</h3>
            <ul>
              {recommendation.reasons.map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>

          <div className="recommendation-grid">
            <div className="rec-card carbon-card">
              <h3>
                <i className="fas fa-leaf"></i>
                Empreinte Carbone
              </h3>
              <p className="value">{recommendation.total_carbon_kg} kg CO₂</p>
              <p className="description">Impact total du voyage</p>
            </div>

            <div className="rec-card budget-card">
              <h3>
                <i className="fas fa-euro-sign"></i>
                Budget
              </h3>
              <p className="value">{recommendation.budget}€</p>
              <p className="description">Estimé total</p>
            </div>

            <div className="rec-card duration-card">
              <h3>
                <i className="fas fa-calendar"></i>
                Durée
              </h3>
              <p className="value">{recommendation.duration_days} jours</p>
              <p className="description">Séjour recommandé</p>
            </div>
          </div>

          {recommendation.activities && recommendation.activities.length > 0 && (
            <div className="activities-recommendation">
              <h3>
                <i className="fas fa-star"></i>
                Activités Recommandées
              </h3>
              <div className="activities-grid">
                {recommendation.activities.map((activity, idx) => (
                  <div key={idx} className="activity-rec-card">
                    <div className="activity-header">
                      <h4>{activity.nom}</h4>
                      <span className="match-score">{Math.round(activity.match_score)}%</span>
                    </div>
                    <p>{activity.description || 'Activité intéressante'}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {recommendation.accommodation && (
            <div className="accommodation-recommendation">
              <h3>
                <i className="fas fa-bed"></i>
                Hébergement Recommandé
              </h3>
              <div className="acc-card">
                <h4>{recommendation.accommodation.nom}</h4>
                <p>{recommendation.accommodation.description}</p>
                <div className="acc-details">
                  <span className="eco-score">
                    <i className="fas fa-leaf"></i>
                    Durabilité: {recommendation.accommodation.scoreDurabilite}/100
                  </span>
                </div>
              </div>
            </div>
          )}

          {recommendation.transport && (
            <div className="transport-recommendation">
              <h3>
                <i className="fas fa-bus"></i>
                Transport Recommandé
              </h3>
              <div className="transport-card">
                <h4>{recommendation.transport.nom}</h4>
                <div className="transport-details">
                  <span className="carbon-info">
                    <i className="fas fa-wind"></i>
                    {recommendation.transport.carbon.kg_co2} kg CO₂
                  </span>
                  <span className={`carbon-level ${recommendation.transport.carbon.level.toLowerCase()}`}>
                    {recommendation.transport.carbon.level}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Recommendations
