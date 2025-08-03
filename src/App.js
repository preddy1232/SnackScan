// src/App.js
import React, { useState } from 'react';
import Camera from './components/Camera';
import ProductList from './components/ProductList';
import NutritionCard from './components/NutritionCard';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { analyzeImage } from './services/imageRecognition';
import { getNutritionData } from './services/nutritionAPI';
import './styles/global.css';

function App() {
  const [currentView, setCurrentView] = useState('camera'); // camera, results, nutrition
  const [detectedProducts, setDetectedProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [nutritionData, setNutritionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageCapture = async (imageFile) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Analyze image with AI
      const products = await analyzeImage(imageFile);
      
      if (products.length === 0) {
        setError('No snacks detected in the image. Try getting closer to the vending machine.');
        setIsLoading(false);
        return;
      }
      
      setDetectedProducts(products);
      setCurrentView('results');
    } catch (err) {
      setError('Failed to analyze image. Please try again.');
      console.error('Image analysis error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProductSelect = async (product) => {
    setIsLoading(true);
    setSelectedProduct(product);
    
    try {
      const nutrition = await getNutritionData(product.name);
      setNutritionData(nutrition);
      setCurrentView('nutrition');
    } catch (err) {
      setError('Failed to load nutrition data. Please try again.');
      console.error('Nutrition data error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const resetApp = () => {
    setCurrentView('camera');
    setDetectedProducts([]);
    setSelectedProduct(null);
    setNutritionData(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 onClick={resetApp}>🍿 SnackScan</h1>
        <p>Snap, Scan, Snack Smart!</p>
      </header>

      <main className="app-main">
        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}
        
        {isLoading && <LoadingSpinner />}
        
        {currentView === 'camera' && !isLoading && (
          <Camera onImageCapture={handleImageCapture} />
        )}
        
        {currentView === 'results' && !isLoading && (
          <ProductList 
            products={detectedProducts} 
            onProductSelect={handleProductSelect}
            onRetake={resetApp}
          />
        )}
        
        {currentView === 'nutrition' && !isLoading && (
          <NutritionCard 
            product={selectedProduct}
            nutrition={nutritionData}
            onBack={() => setCurrentView('results')}
            onRetake={resetApp}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>Make healthier choices with SnackScan</p>
      </footer>
    </div>
  );
}

export default App;