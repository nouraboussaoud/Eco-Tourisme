import React, { useState, useEffect } from 'react';
import './PersonalityTest.css';

const PersonalityTest = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [testCompleted, setTestCompleted] = useState(false);
  const [personalityProfile, setPersonalityProfile] = useState(null);
  const [tripPackage, setTripPackage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/personality-test/questions');
      const data = await response.json();
      setQuestions(data.questions);
      setLoading(false);
    } catch (err) {
      setError('Erreur lors du chargement des questions');
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, answerValue) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerValue
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:8000/personality-test/generate-package', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la génération du package');
      }

      const data = await response.json();
      setPersonalityProfile(data.personality_profile);
      setTripPackage(data.trip_package);
      setTestCompleted(true);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const restartTest = () => {
    setCurrentQuestionIndex(0);
    setAnswers({});
    setTestCompleted(false);
    setPersonalityProfile(null);
    setTripPackage(null);
    setError(null);
  };

  if (loading) {
    return (
      <div className="personality-test-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Chargement en cours...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="personality-test-container">
        <div className="error-message">
          <h3>❌ Erreur</h3>
          <p>{error}</p>
          <button onClick={fetchQuestions} className="btn-primary">
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  if (testCompleted && personalityProfile && tripPackage) {
    return (
      <div className="personality-test-container">
        <div className="results-container">
          <h2>🎉 Votre Profil de Voyage Personnalisé</h2>
          
          {/* Personality Profile Section */}
          <div className="profile-section">
            <div className="profile-header">
              <h3>🌟 {personalityProfile.personality_type}</h3>
              <div className="eco-score">
                <span className="score-label">Score Écologique</span>
                <span className="score-value">{personalityProfile.eco_score}/100</span>
              </div>
            </div>
            <p className="profile-description">{personalityProfile.profile_description}</p>
            
            {personalityProfile.preferences && (
              <div className="preferences-grid">
                <div className="preference-item">
                  <span className="label">Niveau d'activité:</span>
                  <span className="value">{personalityProfile.preferences.activity_level}</span>
                </div>
                <div className="preference-item">
                  <span className="label">Priorité écologique:</span>
                  <span className="value">{personalityProfile.preferences.eco_priority}</span>
                </div>
                <div className="preference-item">
                  <span className="label">Style d'hébergement:</span>
                  <span className="value">{personalityProfile.preferences.accommodation_style}</span>
                </div>
              </div>
            )}
          </div>

          {/* Trip Package Section */}
          <div className="package-section">
            <h3>📦 {tripPackage.package_name}</h3>
            <p className="package-description">{tripPackage.description}</p>
            
            <div className="package-overview">
              <div className="overview-item">
                <span className="icon">📅</span>
                <span className="text">{tripPackage.duration_days} jours</span>
              </div>
              <div className="overview-item">
                <span className="icon">💰</span>
                <span className="text">{tripPackage.total_budget}€</span>
              </div>
              <div className="overview-item">
                <span className="icon">🌱</span>
                <span className="text">Score: {tripPackage.eco_score}/100</span>
              </div>
            </div>

            {/* Cost Breakdown */}
            <div className="cost-breakdown">
              <h4>💵 Détail des Coûts</h4>
              <div className="breakdown-grid">
                <div className="breakdown-item">
                  <span>Hébergement:</span>
                  <span>{tripPackage.breakdown.accommodation}€</span>
                </div>
                <div className="breakdown-item">
                  <span>Activités:</span>
                  <span>{tripPackage.breakdown.activities}€</span>
                </div>
                <div className="breakdown-item">
                  <span>Transport:</span>
                  <span>{tripPackage.breakdown.transport}€</span>
                </div>
                <div className="breakdown-item">
                  <span>Repas:</span>
                  <span>{tripPackage.breakdown.meals}€</span>
                </div>
                <div className="breakdown-item total">
                  <span>Total:</span>
                  <span>{tripPackage.breakdown.total}€</span>
                </div>
              </div>
            </div>

            {/* Itinerary */}
            <div className="itinerary-section">
              <h4>🗓️ Itinéraire Suggéré</h4>
              <div className="itinerary-timeline">
                {tripPackage.itinerary.map((day) => (
                  <div key={day.day} className="itinerary-day">
                    <div className="day-number">Jour {day.day}</div>
                    <div className="day-content">
                      <h5>{day.title}</h5>
                      <p className="day-description">{day.description}</p>
                      {day.eco_highlights && day.eco_highlights.length > 0 && (
                        <div className="eco-highlights">
                          {day.eco_highlights.map((highlight, idx) => (
                            <span key={idx} className="eco-badge">
                              🌿 {highlight}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Places to Visit - SECTION PRINCIPALE */}
            <div className="places-section">
              <h4>📍 Lieux à Visiter ({tripPackage.places?.length || 0} destinations)</h4>
              {tripPackage.places && tripPackage.places.length > 0 ? (
                <div className="places-grid">
                  {tripPackage.places.map((place, idx) => (
                    <div key={idx} className="place-card">
                      <h5>{place.nom}</h5>
                      <div className="place-info">
                        <span className="place-type">{place.type || 'Attraction'}</span>
                        {place.eco_match_score && (
                          <span className="match-score">
                            ⭐ {place.eco_match_score}/100
                          </span>
                        )}
                      </div>
                      {place.scoreDurabilite && (
                        <div className="place-sustainability">
                          <small>🌱 Durabilité: {place.scoreDurabilite}/100</small>
                        </div>
                      )}
                      {place.certifications && (
                        <div className="certifications">
                          <small>🏆 {place.certifications}</small>
                        </div>
                      )}
                      {place.region && (
                        <div className="place-region">
                          <small>📍 {place.region}</small>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="no-data-message">Aucune destination disponible pour le moment.</p>
              )}
            </div>

            {/* Accommodations */}
            {tripPackage.accommodations && tripPackage.accommodations.length > 0 ? (
              <div className="accommodations-section">
                <h4>🏨 Hébergements Recommandés ({tripPackage.accommodations.length})</h4>
                <div className="accommodations-grid">
                  {tripPackage.accommodations.map((acc, idx) => (
                    <div key={idx} className="accommodation-card">
                      <h5>{acc.nom}</h5>
                      <div className="acc-details">
                        <span className="acc-type">{acc.type}</span>
                        {acc.scoreDurabilite && (
                          <span className="sustainability-score">
                            🌱 {acc.scoreDurabilite}/100
                          </span>
                        )}
                      </div>
                      {acc.certifications && (
                        <p className="acc-cert">🏆 {acc.certifications}</p>
                      )}
                      {acc.prix && (
                        <p className="acc-price">{acc.prix}€/nuit</p>
                      )}
                      {acc.destination && (
                        <p className="acc-destination">📍 Près de: {acc.destination}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="accommodations-section">
                <h4>🏨 Hébergements Recommandés</h4>
                <p className="no-data-message">
                  💡 Les hébergements seront disponibles prochainement. 
                  En attendant, vous pouvez explorer les destinations et réserver directement sur place.
                </p>
              </div>
            )}

            {/* Transport Recommendations */}
            {tripPackage.transport_recommendations && (
              <div className="transport-section">
                <h4>🚆 Options de Transport</h4>
                <div className="transport-grid">
                  {tripPackage.transport_recommendations.map((transport, idx) => (
                    <div key={idx} className="transport-card">
                      <div className="transport-header">
                        <span className="transport-type">{transport.type}</span>
                        <span className="eco-score">🌿 {transport.eco_score}/100</span>
                      </div>
                      <p className="transport-desc">{transport.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Sustainability Highlights */}
            {tripPackage.sustainability_highlights && (
              <div className="sustainability-section">
                <h4>✨ Points Forts de Durabilité</h4>
                <ul className="highlights-list">
                  {tripPackage.sustainability_highlights.map((highlight, idx) => (
                    <li key={idx}>
                      <span className="highlight-icon">✓</span>
                      {highlight}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div className="action-buttons">
            <button onClick={restartTest} className="btn-secondary">
              🔄 Refaire le Test
            </button>
            <button 
              onClick={() => window.print()} 
              className="btn-primary"
            >
              🖨️ Imprimer le Package
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="personality-test-container">
        <p>Aucune question disponible</p>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
  const isLastQuestion = currentQuestionIndex === questions.length - 1;
  const currentAnswer = answers[currentQuestion.id];

  return (
    <div className="personality-test-container">
      <div className="test-header">
        <h2>🧭 Test de Personnalité Voyageur</h2>
        <p className="test-subtitle">
          Découvrez votre profil de voyage éco-responsable personnalisé
        </p>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }}></div>
        </div>
        <p className="question-counter">
          Question {currentQuestionIndex + 1} sur {questions.length}
        </p>
      </div>

      <div className="question-container">
        <h3 className="question-text">{currentQuestion.question}</h3>
        
        <div className="options-container">
          {currentQuestion.options.map((option) => (
            <button
              key={option.value}
              className={`option-button ${
                currentAnswer === option.value ? 'selected' : ''
              }`}
              onClick={() => handleAnswerSelect(currentQuestion.id, option.value)}
            >
              <span className="option-radio">
                {currentAnswer === option.value ? '●' : '○'}
              </span>
              <span className="option-label">{option.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="navigation-buttons">
        <button
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
          className="btn-secondary"
        >
          ← Précédent
        </button>

        {!isLastQuestion ? (
          <button
            onClick={handleNext}
            disabled={!currentAnswer}
            className="btn-primary"
          >
            Suivant →
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={!currentAnswer || Object.keys(answers).length !== questions.length}
            className="btn-success"
          >
            ✨ Générer mon Package
          </button>
        )}
      </div>

      <div className="answers-summary">
        <p>
          Réponses complétées: {Object.keys(answers).length}/{questions.length}
        </p>
      </div>
    </div>
  );
};

export default PersonalityTest;
