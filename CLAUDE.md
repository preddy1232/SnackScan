# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SnackScan is a full-stack application with a **React frontend** and **Python Flask backend** that helps users make healthier snack choices by scanning vending machines with their camera. The app uses AI-powered image recognition to detect snack products and provides comprehensive nutritional information.

**Key Features:**
- Camera-based vending machine scanning
- Python-powered AI image recognition with Google Vision API support
- Multi-API nutrition data fetching (USDA, Edamam, Spoonacular)
- Intelligent health scoring system
- Mobile-responsive React frontend

## Development Commands

### Frontend (React)
```bash
# Install frontend dependencies
npm install

# Start React development server (http://localhost:3000)
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Backend (Python)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask development server (http://127.0.0.1:5000)
python run.py
```

### Full Application
```bash
# Start both frontend and backend simultaneously
npm run start:full

# Or use the Windows batch files:
start-full-app.bat     # Starts both in separate windows
start-backend.bat      # Backend only
start-frontend.bat     # Frontend only
```

## Architecture Overview

### Full-Stack Architecture
**Frontend (React)** ↔ **Backend API (Python Flask)** ↔ **External APIs (USDA, Google Vision, etc.)**

### Core Application Flow
1. **Camera View** (`src/components/Camera.js`) - Captures image via webcam or file upload
2. **Image Upload** - React sends image to Python backend via REST API
3. **Python Image Analysis** (`backend/services/image_recognition.py`) - Uses Google Vision API or intelligent simulation
4. **Product Detection** - Returns list of detected vending machine products
5. **Product Selection** (`src/components/ProductList.js`) - User selects product from detected list
6. **Nutrition Lookup** (`backend/services/nutrition_api.py`) - Python backend fetches nutrition data
7. **Health Assessment** (`src/components/NutritionCard.js`) - Displays nutrition with health scoring

### Backend API Endpoints
- `GET /` - Health check
- `POST /api/analyze-image` - Upload image for product detection
- `GET /api/nutrition/<product_name>` - Get nutrition data for product
- `GET /api/products` - List all available products

### Frontend State Management
React hooks in `App.js` manage:
- `currentView`: Navigation between camera/results/nutrition views
- `detectedProducts`: Products detected by Python backend
- `selectedProduct`: User's selected product
- `nutritionData`: Nutrition information from backend
- `isLoading`/`error`: UI state

### Python Backend Services

#### Image Recognition (`backend/services/image_recognition.py`)
- **Google Vision API integration** for real image analysis
- **Comprehensive product database** with 50+ popular vending machine items
- **Intelligent mock recognition** that simulates realistic vending machine detection
- **Confidence scoring** based on text detection and product popularity

#### Nutrition API (`backend/services/nutrition_api.py`)
- **Multi-API strategy** with automatic fallback:
  1. USDA FoodData Central (free, comprehensive)
  2. Edamam Nutrition API (free tier available)
  3. Spoonacular API (paid, very reliable)
  4. Enhanced mock database (200+ products)
- **Smart search optimization** with product-specific search terms
- **Health scoring algorithm** (1-10 scale based on nutritional content)

## Key Files & Directories

### Frontend (`src/`)
- `src/App.js` - Main React component and state management
- `src/components/` - React components (Camera, ProductList, NutritionCard, etc.)
- `src/services/` - API client services (calls Python backend)
- `src/styles/` - CSS styling

### Backend (`backend/`)
- `backend/app.py` - Flask application and API routes
- `backend/run.py` - Development server runner
- `backend/services/image_recognition.py` - Image analysis service
- `backend/services/nutrition_api.py` - Nutrition data service
- `backend/requirements.txt` - Python dependencies
- `backend/.env` - Backend configuration and API keys

## API Configuration

### Backend Environment (`.env` in `backend/` folder)
```bash
# Flask Configuration
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True

# Required: USDA API key (free)
USDA_API_KEY=your-usda-api-key

# Optional: Additional nutrition APIs
EDAMAM_APP_ID=your-edamam-app-id
EDAMAM_APP_KEY=your-edamam-app-key
SPOONACULAR_API_KEY=your-spoonacular-api-key

# Optional: Google Vision API for advanced image recognition
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

### Frontend Environment (`.env` in root folder)
```bash
# Backend API URL (default: http://127.0.0.1:5000)
REACT_APP_API_URL=http://127.0.0.1:5000
```

## Testing

- **Frontend**: Jest + React Testing Library (`npm test`)
- **Backend**: pytest (`cd backend && pytest`)

## Deployment Notes

- Frontend builds to static files (`npm run build`)
- Backend can use Gunicorn for production (`gunicorn app:app`)
- Environment variables must be configured for production APIs
- Backend requires Python 3.8+ with virtual environment