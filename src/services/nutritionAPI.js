// src/services/nutritionAPI.js - PYTHON BACKEND INTEGRATION
// Calls Python Flask API for nutrition data

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

export const getNutritionData = async (productName) => {
  try {
    console.log(`🔍 Getting nutrition data from Python backend for: ${productName}`);
    
    // Encode the product name for URL
    const encodedProductName = encodeURIComponent(productName);
    
    // Call Python backend API
    const response = await fetch(`${API_BASE_URL}/api/nutrition/${encodedProductName}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      if (response.status === 404) {
        throw new Error('Nutrition data not found for this product');
      }
      
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Unknown error from backend');
    }
    
    console.log(`✅ Got nutrition data from ${result.nutrition.source}`);
    
    // Transform the response to match the expected frontend format
    const nutrition = result.nutrition;
    return {
      name: nutrition.name,
      servingSize: nutrition.serving_size,
      calories: nutrition.calories,
      protein: nutrition.protein,
      carbs: nutrition.carbs,
      fat: nutrition.fat,
      fiber: nutrition.fiber,
      sugar: nutrition.sugar,
      sodium: nutrition.sodium,
      healthScore: nutrition.health_score,
      source: nutrition.source
    };
    
  } catch (error) {
    console.error('❌ Error getting nutrition data from Python backend:', error);
    
    // Check if backend is running
    if (error.message.includes('fetch')) {
      console.error('🔌 Backend connection failed. Make sure Python server is running on', API_BASE_URL);
      throw new Error('Cannot connect to backend server. Please make sure the Python API is running.');
    }
    
    throw new Error(`Nutrition lookup failed: ${error.message}`);
  }
};

// Get list of all available products from backend
export const getAvailableProducts = async () => {
  try {
    console.log('📋 Getting available products from Python backend...');
    
    const response = await fetch(`${API_BASE_URL}/api/products`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to get products');
    }
    
    console.log(`✅ Got ${result.count} products from backend`);
    return result.products;
    
  } catch (error) {
    console.error('❌ Error getting products from backend:', error);
    return [];
  }
};

// Utility function to validate product name
export const validateProductName = (productName) => {
  if (!productName || typeof productName !== 'string') {
    return false;
  }
  
  const trimmed = productName.trim();
  return trimmed.length > 0 && trimmed.length <= 100;
};