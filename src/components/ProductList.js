// src/components/ProductList.js - FIXED VERSION
import React from 'react';

const ProductList = ({ products, onProductSelect, onRetake }) => {
  const getCategoryEmoji = (category) => {
    const emojiMap = {
      beverages: '🥤',
      chips: '🍟',
      candy: '🍫',
      cookies: '🍪',
      crackers: '🧀',
      healthy: '🥜',
      nuts: '🥜',
      sports: '⚡',
      energy: '⚡',
      coffee: '☕',
      breakfast: '🥞',
      snacks: '🍿',
      other: '🍪'
    };
    return emojiMap[category] || '🍪';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 0.8) return '#00D4AA';
    if (confidence > 0.6) return '#F6AD55';
    return '#FC8181';
  };

  // Debug log to see what products we're receiving
  console.log('📋 ProductList received products:', products);

  if (!products || products.length === 0) {
    return (
      <div className="product-list">
        <h2>🔍 No Products Detected</h2>
        <p>Try taking another photo of the vending machine</p>
        <div className="list-actions">
          <button className="action-button secondary" onClick={onRetake}>
            📸 Retake Photo
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="product-list">
      <h2>🔍 Detected Snacks ({products.length} found)</h2>
      
      {products.map((product, index) => (
        <div
          key={product.id || index}
          className="product-item"
          onClick={() => onProductSelect(product)}
        >
          <div className="product-info">
            <h3>
              {getCategoryEmoji(product.category)} {product.name || 'Unknown Product'}
            </h3>
            <div 
              className="product-confidence"
              style={{ color: getConfidenceColor(product.confidence || 0) }}
            >
              {Math.round((product.confidence || 0) * 100)}% confidence
            </div>
            {product.description && (
              <div className="product-description" style={{ fontSize: '0.8rem', color: '#666', marginTop: '4px' }}>
                {product.description}
              </div>
            )}
          </div>
          <div className="product-category">
            {product.category || 'other'}
          </div>
        </div>
      ))}
      
      <div className="list-actions">
        <button 
          className="action-button primary"
          onClick={() => products.length > 0 && onProductSelect(products[0])}
          disabled={!products.length}
        >
          View Top Result
        </button>
        <button 
          className="action-button secondary"
          onClick={onRetake}
        >
          📸 Retake Photo
        </button>
      </div>
      
      {/* Debug info (remove in production) */}
      <div style={{ 
        background: '#f0f0f0', 
        padding: '10px', 
        borderRadius: '5px', 
        marginTop: '10px',
        fontSize: '12px',
        color: '#666'
      }}>
        <strong>Debug Info:</strong>
        <br />
        Products received: {products.length}
        <br />
        First product: {products[0]?.name || 'No name found'}
        <br />
        Product structure: {JSON.stringify(products[0], null, 2)}
      </div>
    </div>
  );
};

export default ProductList;