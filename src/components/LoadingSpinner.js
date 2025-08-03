// src/components/LoadingSpinner.js
import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <div className="loading-text">
        🤖 Analyzing your photo...
        <br />
        <small>This may take a few seconds</small>
      </div>
    </div>
  );
};

export default LoadingSpinner;