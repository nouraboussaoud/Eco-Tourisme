import './Statistics.css'

function Statistics({ stats, destinations, activites }) {
  const chartData = {
    pointsPerCity: (destinations || []).reduce((acc, point) => {
      const city = point.localiseDans?.split('#').pop() || 'Non spécifiée'
      acc[city] = (acc[city] || 0) + 1
      return acc
    }, {}),
    activityTypes: (activites || []).reduce((acc, activity) => {
      const type = activity.type || 'Autre'
      acc[type] = (acc[type] || 0) + 1
      return acc
    }, {})
  }

  return (
    <div className="statistics">
      <div className="stats-header">
        <h2>
          <i className="fas fa-chart-bar"></i>
          Statistiques & Analytiques
        </h2>
        <p>Suivez l'impact de nos efforts communautaires</p>
      </div>

      <div className="stats-cards">
        <div className="stat-card">
          <div className="stat-number">
            {destinations?.length || 0}
          </div>
          <div className="stat-label">
            <i className="fas fa-map-location-dot"></i>
            Destinations
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-number">
            {activites?.length || 0}
          </div>
          <div className="stat-label">
            <i className="fas fa-calendar"></i>
            Activités
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-number">
            {stats?.totalVoyageurs || 0}
          </div>
          <div className="stat-label">
            <i className="fas fa-users"></i>
            Voyageurs Actifs
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-number">
            {stats?.totalHebergements || 0}
          </div>
          <div className="stat-label">
            <i className="fas fa-hotel"></i>
            Hébergements
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Destinations par Région</h3>
          <div className="chart">
            {Object.entries(chartData.pointsPerCity).length > 0 ? (
              <ul className="bar-chart">
                {Object.entries(chartData.pointsPerCity).map(([city, count]) => (
                  <li key={city}>
                    <span className="city-name">{city}</span>
                    <div className="bar-container">
                      <div 
                        className="bar"
                        style={{ 
                          width: `${(count / Math.max(...Object.values(chartData.pointsPerCity))) * 100}%` 
                        }}
                      >
                        <span className="bar-value">{count}</span>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="no-data">Aucune donnée</p>
            )}
          </div>
        </div>

        <div className="chart-card">
          <h3>Types d'Activités</h3>
          <div className="chart">
            {Object.entries(chartData.activityTypes).length > 0 ? (
              <ul className="pie-chart">
                {Object.entries(chartData.activityTypes).map(([type, count], idx) => {
                  const colors = ['#667eea', '#f093fb', '#4ade80', '#fbbf24', '#f87171']
                  return (
                    <li key={type}>
                      <span className="color-indicator" style={{ backgroundColor: colors[idx % colors.length] }}></span>
                      <span className="type-label">{type}: {count}</span>
                    </li>
                  )
                })}
              </ul>
            ) : (
              <p className="no-data">Aucune donnée</p>
            )}
          </div>
        </div>
      </div>

      <div className="impact-section">
        <h3>Impact Environnemental du Tourisme</h3>
        <div className="impact-cards">
          <div className="impact-card">
            <div className="icon">
              <i className="fas fa-wind"></i>
            </div>
            <div className="content">
              <h4>Empreinte Carbone Réduite</h4>
              <p>Estimée à <strong>50% vs tourisme classique</strong></p>
            </div>
          </div>

          <div className="impact-card">
            <div className="icon">
              <i className="fas fa-leaf"></i>
            </div>
            <div className="content">
              <h4>Destinations Préservées</h4>
              <p>Estimé à <strong>250+ écosystèmes protégés</strong></p>
            </div>
          </div>

          <div className="impact-card">
            <div className="icon">
              <i className="fas fa-users-heart"></i>
            </div>
            <div className="content">
              <h4>Impact Communautaire</h4>
              <p>Revenu pour <strong>1,250+ communautés locales</strong></p>
            </div>
          </div>

          <div className="impact-card">
            <div className="icon">
              <i className="fas fa-check-circle"></i>
            </div>
            <div className="content">
              <h4>Certifications Éco</h4>
              <p>Actuellement <strong>400+ hébergements certifiés</strong></p>
            </div>
          </div>
        </div>
      </div>

      <div className="timeline-section">
        <h3>Historique des Activités</h3>
        <div className="timeline">
          {activities.slice(0, 5).map((activity, idx) => (
            <div key={idx} className="timeline-item">
              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <h4>{activity.nom}</h4>
                <p>{activity.description || 'Pas de description'}</p>
                {activity.dateActivite && (
                  <span className="timeline-date">
                    {new Date(activity.dateActivite).toLocaleDateString('fr-FR')}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Statistics
