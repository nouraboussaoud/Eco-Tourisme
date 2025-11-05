import { useState } from 'react'
import './CollectionPoints.css'

function CollectionPoints({ destinations, hebergements }) {
  const [selectedPoint, setSelectedPoint] = useState(null)
  const [filterRegion, setFilterRegion] = useState('')

  const regions = [...new Set(destinations.map(p => {
    const parts = p.localiseDans?.split('#') || [''];
    return parts[parts.length - 1] || 'Non spécifiée';
  }))]

  const filteredPoints = filterRegion 
    ? destinations.filter(p => {
        const parts = p.localiseDans?.split('#') || [''];
        return (parts[parts.length - 1] || '').includes(filterRegion);
      })
    : destinations

  return (
    <div className="collection-points">
      <div className="points-header">
        <h2>
          <i className="fas fa-map-location-dot"></i>
          Destinations Éco-responsables
        </h2>
        <p>Explorez nos destinations durables et respectueuses de l'environnement</p>
      </div>

      <div className="points-filters">
        <div className="filter-group">
          <label>Filtrer par région:</label>
          <select 
            value={filterRegion} 
            onChange={(e) => setFilterRegion(e.target.value)}
            className="filter-select"
          >
            <option value="">Toutes les régions</option>
            {regions.map(region => (
              <option key={region} value={region}>{region}</option>
            ))}
          </select>
        </div>
        <div className="info-text">
          {filteredPoints.length} destination{filteredPoints.length !== 1 ? 's' : ''} trouvée{filteredPoints.length !== 1 ? 's' : ''}
        </div>
      </div>

      <div className="points-container">
        {filteredPoints && filteredPoints.length > 0 ? (
          <div className="points-grid">
            {filteredPoints.map((point, idx) => (
              <div 
                key={idx}
                className={`point-card ${selectedPoint?.nom === point.nom ? 'active' : ''}`}
                onClick={() => setSelectedPoint(point)}
              >
                <div className="point-header">
                  <h3>{point.nom}</h3>
                  <i className="fas fa-chevron-right"></i>
                </div>
                <div className="point-info">
                  {point.description && (
                    <p>
                      <i className="fas fa-info-circle"></i>
                      {point.description}
                    </p>
                  )}
                  {point.localiseDans && (
                    <p>
                      <i className="fas fa-location-dot"></i>
                      {point.localiseDans}
                    </p>
                  )}
                  {point.certification && (
                    <p>
                      <i className="fas fa-leaf"></i>
                      Certifié Eco
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-points">
            <i className="fas fa-search"></i>
            <p>Aucune destination trouvée</p>
          </div>
        )}
      </div>

      {selectedPoint && (
        <div className="point-details">
          <div className="details-header">
            <h2>{selectedPoint.nom}</h2>
            <button className="close-btn" onClick={() => setSelectedPoint(null)}>
              <i className="fas fa-times"></i>
            </button>
          </div>

          <div className="details-grid">
            {selectedPoint.description && (
              <div className="detail-item">
                <i className="fas fa-book"></i>
                <div>
                  <label>Description</label>
                  <p>{selectedPoint.description}</p>
                </div>
              </div>
            )}

            {selectedPoint.type && (
              <div className="detail-item">
                <i className="fas fa-tag"></i>
                <div>
                  <label>Type de destination</label>
                  <p>{selectedPoint.type}</p>
                </div>
              </div>
            )}

            {selectedPoint.localiseDans && (
              <div className="detail-item">
                <i className="fas fa-map-pin"></i>
                <div>
                  <label>Région</label>
                  <p>{selectedPoint.localiseDans}</p>
                </div>
              </div>
            )}

            {selectedPoint.certification && (
              <div className="detail-item">
                <i className="fas fa-certificate"></i>
                <div>
                  <label>Certification</label>
                  <p>{selectedPoint.certification}</p>
                </div>
              </div>
            )}
          </div>

          {hebergements && hebergements.length > 0 && (
            <div className="waste-types">
              <h3>Hébergements recommandés:</h3>
              <div className="waste-list">
                {hebergements.map((type, idx) => (
                  <span key={idx} className="waste-badge">
                    <i className="fas fa-hotel"></i>
                    {type.nom}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default CollectionPoints
