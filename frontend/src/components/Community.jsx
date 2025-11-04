import { useState } from 'react'
import './Community.css'

function Community({ activities, badges }) {
  const [showForm, setShowForm] = useState(false)
  const [selectedBadge, setSelectedBadge] = useState(null)

  return (
    <div className="community">
      <div className="community-header">
        <h2>
          <i className="fas fa-users"></i>
          Engagement Communautaire
        </h2>
        <p>Participez à des activités et gagnez des récompenses</p>
      </div>

      <div className="community-grid">
        {/* Badges Section */}
        <div className="badges-section">
          <h3>
            <i className="fas fa-trophy"></i>
            Badges & Récompenses
          </h3>
          <div className="badges-grid">
            {badges && badges.length > 0 ? (
              badges.map((badge, idx) => (
                <div 
                  key={idx}
                  className="badge-card"
                  onClick={() => setSelectedBadge(badge)}
                >
                  <div className="badge-icon">
                    <i className="fas fa-star"></i>
                  </div>
                  <h4>{badge.nom}</h4>
                  <p>{badge.description || 'Badge'}</p>
                </div>
              ))
            ) : (
              <p className="no-data">Aucun badge disponible</p>
            )}
          </div>
        </div>

        {/* Activities Section */}
        <div className="activities-section">
          <h3>
            <i className="fas fa-calendar"></i>
            Activités & Défis
          </h3>
          <button className="btn-add" onClick={() => setShowForm(!showForm)}>
            <i className="fas fa-plus"></i>
            Nouvelle Activité
          </button>

          <div className="activities-list">
            {activities && activities.length > 0 ? (
              activities.map((activity, idx) => (
                <div key={idx} className="activity-card">
                  <div className="activity-badge">
                    <i className="fas fa-star"></i>
                  </div>
                  <div className="activity-body">
                    <h4>{activity.nom}</h4>
                    <p>{activity.description || 'Pas de description'}</p>
                    {activity.dateActivite && (
                      <span className="date">
                        <i className="fas fa-calendar-alt"></i>
                        {new Date(activity.dateActivite).toLocaleDateString('fr-FR')}
                      </span>
                    )}
                  </div>
                  <button className="btn-join">
                    <i className="fas fa-check"></i>
                    Participer
                  </button>
                </div>
              ))
            ) : (
              <p className="no-data">Aucune activité disponible</p>
            )}
          </div>
        </div>
      </div>

      {selectedBadge && (
        <div className="badge-modal" onClick={() => setSelectedBadge(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-modal" onClick={() => setSelectedBadge(null)}>
              <i className="fas fa-times"></i>
            </button>
            <div className="modal-badge">
              <i className="fas fa-star"></i>
            </div>
            <h2>{selectedBadge.nom}</h2>
            <p>{selectedBadge.description || 'Badge'}</p>
            <button className="btn-primary">
              <i className="fas fa-info-circle"></i>
              Voir Plus
            </button>
          </div>
        </div>
      )}

      {showForm && (
        <div className="contribution-form">
          <h3>Ajouter une Contribution</h3>
          <form>
            <div className="form-group">
              <label>Type d'activité</label>
              <select>
                <option>Contribution</option>
                <option>Nettoyage</option>
                <option>Tri des déchets</option>
                <option>Engagement Communautaire</option>
              </select>
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea placeholder="Décrivez votre contribution..."></textarea>
            </div>
            <div className="form-group">
              <label>Quantité (kg)</label>
              <input type="number" placeholder="Entrez la quantité" />
            </div>
            <div className="form-buttons">
              <button type="button" className="btn-cancel" onClick={() => setShowForm(false)}>
                Annuler
              </button>
              <button type="submit" className="btn-submit">
                <i className="fas fa-paper-plane"></i>
                Soumettre
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}

export default Community
