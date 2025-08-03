// src/services/imageRecognition.js - PYTHON BACKEND INTEGRATION
// Calls Python Flask API for image recognition

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

export const analyzeImage = async (imageFile) => {
  try {
    console.log('🔍 Sending image to Python backend for analysis...');
    console.log('📁 Image file:', imageFile.name, 'Size:', imageFile.size);
    
    // Create FormData to send the image file
    const formData = new FormData();
    formData.append('image', imageFile);
    
    // Call Python backend API
    const response = await fetch(`${API_BASE_URL}/api/analyze-image`, {
      method: 'POST',
      body: formData,
      // Don't set Content-Type header - let browser set it with boundary for FormData
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Unknown error from backend');
    }
    
    console.log(`✅ Python backend detected ${result.count} products`);
    console.log('🍿 Products found:', result.products.map(p => p.name).join(', '));
    
    // Transform the response to match the expected format
    return result.products.map(product => ({
      id: product.id,
      name: product.name,
      confidence: product.confidence,
      category: product.category,
      description: product.description || '',
      popularity: product.popularity || 50,
      imageUrl: null // Not used in current implementation
    }));
    
  } catch (error) {
    console.error('❌ Error calling Python backend:', error);
    
    // Check if backend is running
    if (error.message.includes('fetch')) {
      console.error('🔌 Backend connection failed. Make sure Python server is running on', API_BASE_URL);
      throw new Error('Cannot connect to backend server. Please make sure the Python API is running.');
    }
    
    throw new Error(`Image analysis failed: ${error.message}`);
  }
};

// Utility function to check if backend is available
export const checkBackendHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      timeout: 5000
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Backend health check passed:', data.service);
      return true;
    }
    
    return false;
  } catch (error) {
    console.warn('⚠️ Backend health check failed:', error.message);
    return false;
  }
};

// Get list of supported image formats from backend
export const getSupportedFormats = async () => {
  try {
    // For now, return common formats. Could be fetched from backend if needed.
    return ['png', 'jpg', 'jpeg', 'gif', 'webp'];
  } catch (error) {
    console.warn('Could not get supported formats from backend');
    return ['png', 'jpg', 'jpeg'];
  }
};