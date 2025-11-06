import './Header.css'

function Header({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'dashboard', icon: 'fas fa-home', label: 'Accueil' },
    { id: 'recommendations', icon: 'fas fa-compass', label: 'Recommandations' },
    { id: 'query', icon: 'fas fa-search', label: 'Recherche' },
    { id: 'crud', icon: 'fas fa-database', label: 'CRUD' },
    { id: 'points', icon: 'fas fa-map-location-dot', label: 'Destinations' },
    { id: 'community', icon: 'fas fa-earth-americas', label: 'Communauté' },
    { id: 'statistics', icon: 'fas fa-chart-bar', label: 'Statistiques' }
  ]

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <i className="fas fa-leaf"></i>
          <h1>Tourisme Éco-responsable</h1>
          <p>Plateforme de Voyage Durable</p>
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
