// src/components/NutritionCard.js
import React from 'react';

const NutritionCard = ({ product, nutrition, onBack, onRetake }) => {
  const getHealthScoreColor = (score) => {
    if (score >= 7) return '#00D4AA';
    if (score >= 5) return '#F6AD55';
    return '#FC8181';
  };

  const getHealthScoreText = (score) => {
    if (score >= 8) return 'Excellent';
    if (score >= 6) return 'Good';
    if (score >= 4) return 'Okay';
    return 'Poor';
  };

  return (
    <div className="nutrition-card">
      <div className="nutrition-header">
        <h2>{nutrition.name}</h2>
        <div className="serving-size">{nutrition.servingSize}</div>
        <div className="health-score">
          <span>Health Score:</span>
          <span style={{ color: getHealthScoreColor(nutrition.healthScore) }}>
            {nutrition.healthScore}/10
          </span>
          <span>({getHealthScoreText(nutrition.healthScore)})</span>
        </div>
      </div>
      
      <div className="nutrition-content">
        <div className="nutrition-source">
          Data from {nutrition.source}
        </div>
        
        <div className="nutrition-grid">
          <div className="nutrition-item calories">
            <div className="nutrition-value">{nutrition.calories}</div>
            <div className="nutrition-label">Calories</div>
          </div>
          
          <div className="nutrition-item">
            <div className="nutrition-value">{nutrition.protein}</div>
            <div className="nutrition-label">Protein</div>
          </div>
          
          <div className="nutrition-item">
            <div className="nutrition-value">{nutrition.carbs}</div>
            <div className="nutrition-label">Carbs</div>
          </div>
          
          <div className="nutrition-item">
            <div className="nutrition-value">{nutrition.fat}</div>
            <div className="nutrition-label">Fat</div>
          </div>
          
          <div className="nutrition-item">
            <div className="nutrition-value">{nutrition.fiber}</div>
            <div className="nutrition-label">Fiber</div>
          </div>
          
          <div className="nutrition-item">
            <div className="nutrition-value">{nutrition.sugar}</div>
            <div className="nutrition-label">Sugar</div>
          </div>
          
          <div className="nutrition-item">
            <div className="nutrition-value">{nutrition.sodium}</div>
            <div className="nutrition-label">Sodium</div>
          </div>
        </div>
        
        <div className="list-actions">
          <button className="action-button secondary" onClick={onBack}>
            ← Back to Results
          </button>
          <button className="action-button primary" onClick={onRetake}>
            📸 Scan Again
          </button>
        </div>
      </div>
    </div>
  );
};

export default NutritionCard;