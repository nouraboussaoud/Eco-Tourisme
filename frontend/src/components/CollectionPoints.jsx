import { useState } from 'react'
import './CollectionPoints.css'

function CollectionPoints({ points, wasteTypes }) {
  const [selectedPoint, setSelectedPoint] = useState(null)
  const [filterCity, setFilterCity] = useState('')

  const cities = [...new Set(points.map(p => {
    const parts = p.localiseDans?.split('#') || [''];
    return parts[parts.length - 1] || 'Non spécifiée';
  }))]

  const filteredPoints = filterCity 
    ? points.filter(p => {
        const parts = p.localiseDans?.split('#') || [''];
        return (parts[parts.length - 1] || '').includes(filterCity);
      })
    : points

  return (
    <div className="collection-points">
      <div className="points-header">
        <h2>
          <i className="fas fa-map-marker-alt"></i>
          Points de Collecte
        </h2>
        <p>Trouvez les points de collecte les plus proches de vous</p>
      </div>

      <div className="points-filters">
        <div className="filter-group">
          <label>Filtrer par ville:</label>
          <select 
            value={filterCity} 
            onChange={(e) => setFilterCity(e.target.value)}
            className="filter-select"
          >
            <option value="">Toutes les villes</option>
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>
        <div className="info-text">
          {filteredPoints.length} point{filteredPoints.length !== 1 ? 's' : ''} trouvé{filteredPoints.length !== 1 ? 's' : ''}
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
                  {point.adresse && (
                    <p>
                      <i className="fas fa-map-pin"></i>
                      {point.adresse}
                    </p>
                  )}
                  {point.horaires && (
                    <p>
                      <i className="fas fa-clock"></i>
                      {point.horaires}
                    </p>
                  )}
                  {point.telephone && (
                    <p>
                      <i className="fas fa-phone"></i>
                      {point.telephone}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-points">
            <i className="fas fa-search"></i>
            <p>Aucun point de collecte trouvé</p>
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
            {selectedPoint.adresse && (
              <div className="detail-item">
                <i className="fas fa-map-pin"></i>
                <div>
                  <label>Adresse</label>
                  <p>{selectedPoint.adresse}</p>
                </div>
              </div>
            )}

            {selectedPoint.latitude && selectedPoint.longitude && (
              <div className="detail-item">
                <i className="fas fa-globe"></i>
                <div>
                  <label>Coordonnées GPS</label>
                  <p>{selectedPoint.latitude}, {selectedPoint.longitude}</p>
                </div>
              </div>
            )}

            {selectedPoint.horaires && (
              <div className="detail-item">
                <i className="fas fa-clock"></i>
                <div>
                  <label>Horaires</label>
                  <p>{selectedPoint.horaires}</p>
                </div>
              </div>
            )}

            {selectedPoint.telephone && (
              <div className="detail-item">
                <i className="fas fa-phone"></i>
                <div>
                  <label>Téléphone</label>
                  <p>{selectedPoint.telephone}</p>
                </div>
              </div>
            )}
          </div>

          {wasteTypes && wasteTypes.length > 0 && (
            <div className="waste-types">
              <h3>Types de déchets acceptés:</h3>
              <div className="waste-list">
                {wasteTypes.map((type, idx) => (
                  <span key={idx} className="waste-badge">
                    <i className="fas fa-trash"></i>
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
