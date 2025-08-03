// src/components/ErrorMessage.js
import React from 'react';

const ErrorMessage = ({ message, onDismiss }) => {
  return (
    <div className="error-message">
      <button className="error-dismiss" onClick={onDismiss}>
        ×
      </button>
      <strong>Oops!</strong> {message}
    </div>
  );
};

export default ErrorMessage;