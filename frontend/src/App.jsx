import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import QueryInterface from './components/QueryInterface'
import CollectionPoints from './components/CollectionPoints'
import Community from './components/Community'
import Statistics from './components/Statistics'
import Recommendations from './components/Recommendations'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [destinations, setDestinations] = useState([])
  const [hebergements, setHebergements] = useState([])
  const [activites, setActivites] = useState([])
  const [certifications, setCertifications] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Charger les données au démarrage
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [destRes, hebRes, activRes, certRes, statsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/destinations`),
          axios.get(`${API_BASE_URL}/hebergements`),
          axios.get(`${API_BASE_URL}/activites`),
          axios.get(`${API_BASE_URL}/certifications`),
          axios.get(`${API_BASE_URL}/stats`)
        ])

        setDestinations(destRes.data.destinations || [])
        setHebergements(hebRes.data.hebergements || [])
        setActivites(activRes.data.activites || [])
        setCertifications(certRes.data.certifications || [])
        setStats(statsRes.data.statistics || {})
        setError(null)
      } catch (err) {
        console.error('Erreur lors du chargement des données:', err)
        setError('Impossible de se connecter au serveur. Assurez-vous que le backend est lancé sur le port 8000.')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const handleRefresh = async () => {
    await fetchData()
  }

  return (
    <div className="app">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      
      {error && (
        <div className="error-banner">
          <i className="fas fa-exclamation-circle"></i>
          <span>{error}</span>
        </div>
      )}

      <main className="main-content">
        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Chargement des données...</p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <Dashboard 
                stats={stats} 
                destinations={destinations}
                activites={activites}
              />
            )}
            {activeTab === 'query' && (
              <QueryInterface apiUrl={API_BASE_URL} />
            )}
            {activeTab === 'points' && (
              <CollectionPoints 
                destinations={destinations}
                hebergements={hebergements}
              />
            )}
            {activeTab === 'community' && (
              <Community 
                activites={activites}
                certifications={certifications}
              />
            )}
            {activeTab === 'statistics' && (
              <Statistics 
                stats={stats}
                destinations={destinations}
                activites={activites}
              />
            )}
            {activeTab === 'recommendations' && (
              <Recommendations apiUrl={API_BASE_URL} />
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default App
