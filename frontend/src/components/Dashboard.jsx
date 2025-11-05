import './Dashboard.css'

function Dashboard({ stats, destinations, activites }) {
  const statCards = [
    {
      title: 'Destinations',
      value: destinations?.length || 0,
      icon: 'fas fa-map-location-dot',
      color: '#667eea'
    },
    {
      title: 'Activités',
      value: activites?.length || 0,
      icon: 'fas fa-calendar',
      color: '#f093fb'
    },
    {
      title: 'Voyageurs',
      value: stats?.totalVoyageurs || 0,
      icon: 'fas fa-users',
      color: '#4ade80'
    },
    {
      title: 'Hébergements',
      value: stats?.totalHebergements || 0,
      icon: 'fas fa-hotel',
      color: '#fbbf24'
    }
  ]

  return (
    <div className="dashboard">
      <div className="welcome-section">
        <h1>Bienvenue sur Tourisme Éco-responsable</h1>
        <p>Plateforme collaborative de voyage durable avec recommandations intelligentes</p>
      </div>

      <div className="stats-grid">
        {statCards.map((card, idx) => (
          <div key={idx} className="stat-card">
            <div className="stat-icon" style={{ color: card.color }}>
              <i className={card.icon}></i>
            </div>
            <div className="stat-content">
              <h3>{card.title}</h3>
              <p className="stat-value">{card.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-question-circle"></i>
          </div>
          <h3>Recherche Intelligente</h3>
          <p>Posez vos questions en français, nos algorithmes les convertissent en requêtes SPARQL</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-map"></i>
          </div>
          <h3>Localisation</h3>
          <p>Trouvez les points de collecte proches de vous avec coordonnées GPS et horaires</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-users"></i>
          </div>
          <h3>Engagement Communautaire</h3>
          <p>Participez à des défis, gagnez des badges et contribuez à une meilleure gestion</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-chart-line"></i>
          </div>
          <h3>Statistiques</h3>
          <p>Suivez l'impact de vos contributions via un dashboard complet et transparent</p>
        </div>
      </div>

      <div className="recent-activities">
        <h2>Activités Récentes</h2>
        {activites && activites.length > 0 ? (
          <div className="activities-list">
            {activites.slice(0, 5).map((activity, idx) => (
              <div key={idx} className="activity-item">
                <div className="activity-icon">
                  <i className="fas fa-star"></i>
                </div>
                <div className="activity-content">
                  <h4>{activity.nom || 'Activité'}</h4>
                  <p>{activity.description || 'Pas de description'}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data">Aucune activité disponible pour le moment</p>
        )}
      </div>
    </div>
  )
}

export default Dashboard
