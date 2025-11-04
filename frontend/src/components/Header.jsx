import './Header.css'

function Header({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'dashboard', icon: 'fas fa-home', label: 'Accueil' },
    { id: 'recommendations', icon: 'fas fa-wand-magic-sparkles', label: 'Recommandations' },
    { id: 'query', icon: 'fas fa-search', label: 'Recherche' },
    { id: 'points', icon: 'fas fa-map-marker-alt', label: 'Points de collecte' },
    { id: 'community', icon: 'fas fa-users', label: 'Communauté' },
    { id: 'statistics', icon: 'fas fa-chart-bar', label: 'Statistiques' }
  ]

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <i className="fas fa-leaf"></i>
          <h1>EcoWaste Manager</h1>
          <p>Plateforme de Gestion des Déchets</p>
        </div>
        
        <nav className="nav">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`nav-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
              title={tab.label}
            >
              <i className={tab.icon}></i>
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </header>
  )
}

export default Header
