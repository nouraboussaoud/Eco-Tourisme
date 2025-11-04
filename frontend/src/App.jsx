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
  const [collectionPoints, setCollectionPoints] = useState([])
  const [wasteTypes, setWasteTypes] = useState([])
  const [activities, setActivities] = useState([])
  const [badges, setBadges] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Charger les données au démarrage
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [pointsRes, typesRes, activitiesRes, badgesRes, statsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/collection-points`),
          axios.get(`${API_BASE_URL}/waste-types`),
          axios.get(`${API_BASE_URL}/activities`),
          axios.get(`${API_BASE_URL}/badges`),
          axios.get(`${API_BASE_URL}/stats`)
        ])

        setCollectionPoints(pointsRes.data.collection_points || [])
        setWasteTypes(typesRes.data.waste_types || [])
        setActivities(activitiesRes.data.activities || [])
        setBadges(badgesRes.data.badges || [])
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
                collectionPoints={collectionPoints}
                activities={activities}
              />
            )}
            {activeTab === 'query' && (
              <QueryInterface apiUrl={API_BASE_URL} />
            )}
            {activeTab === 'points' && (
              <CollectionPoints 
                points={collectionPoints}
                wasteTypes={wasteTypes}
              />
            )}
            {activeTab === 'community' && (
              <Community 
                activities={activities}
                badges={badges}
              />
            )}
            {activeTab === 'statistics' && (
              <Statistics 
                stats={stats}
                collectionPoints={collectionPoints}
                activities={activities}
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
