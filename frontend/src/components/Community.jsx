import { useState } from 'react'
import './Community.css'

function Community({ activites, certifications }) {
  const [showForm, setShowForm] = useState(false)
  const [selectedCert, setSelectedCert] = useState(null)

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
            Certifications Écologiques
          </h3>
          <div className="badges-grid">
            {certifications && certifications.length > 0 ? (
              certifications.map((cert, idx) => (
                <div 
                  key={idx}
                  className="badge-card"
                  onClick={() => setSelectedCert(cert)}
                >
                  <div className="badge-icon">
                    <i className="fas fa-leaf"></i>
                  </div>
                  <h4>{cert.nom}</h4>
                  <p>{cert.description || 'Certification'}</p>
                </div>
              ))
            ) : (
              <p className="no-data">Aucune certification disponible</p>
            )}
          </div>
        </div>

        {/* Activities Section */}
        <div className="activities-section">
          <h3>
            <i className="fas fa-calendar"></i>
            Activités & Avis Voyageurs
          </h3>
          <button className="btn-add" onClick={() => setShowForm(!showForm)}>
            <i className="fas fa-plus"></i>
            Ajouter un Avis
          </button>

          <div className="activities-list">
            {activites && activites.length > 0 ? (
              activites.map((activity, idx) => (
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
                    Partager mon Expérience
                  </button>
                </div>
              ))
            ) : (
              <p className="no-data">Aucune activité disponible</p>
            )}
          </div>
        </div>
      </div>

      {selectedCert && (
        <div className="badge-modal" onClick={() => setSelectedCert(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-modal" onClick={() => setSelectedCert(null)}>
              <i className="fas fa-times"></i>
            </button>
            <div className="modal-badge">
              <i className="fas fa-leaf"></i>
            </div>
            <h2>{selectedCert.nom}</h2>
            <p>{selectedCert.description || 'Certification'}</p>
            <button className="btn-primary">
              <i className="fas fa-info-circle"></i>
              Voir Plus
            </button>
          </div>
        </div>
      )}

      {showForm && (
        <div className="contribution-form">
          <h3>Ajouter un Avis Voyageur</h3>
          <form>
            <div className="form-group">
              <label>Type de Voyage</label>
              <select>
                <option>Aventure</option>
                <option>Culture</option>
                <option>Bien-être</option>
                <option>Famille</option>
              </select>
            </div>
            <div className="form-group">
              <label>Commentaire</label>
              <textarea placeholder="Partagez votre expérience de voyage..."></textarea>
            </div>
            <div className="form-group">
              <label>Note (1-5)</label>
              <input type="number" min="1" max="5" placeholder="Entrez votre note" />
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
