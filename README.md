# 🍿 SnackScan

**Snap, Scan, Snack Smart!**

SnackScan is a full-stack web application that helps you make healthier snack choices by scanning vending machines with your camera. The app uses AI-powered image recognition to detect snack products and provides comprehensive nutritional information to help you make informed decisions.

## 🚀 Quick Start

### Option 1: One-Click Startup (Windows)
1. Double-click `start-full-app.bat` to start both frontend and backend
2. Open your browser to http://localhost:3000
3. Start scanning vending machines! 📸

### Option 2: Manual Setup

#### Prerequisites
- **Python 3.8+** ([Download here](https://python.org))
- **Node.js 16+** ([Download here](https://nodejs.org))

#### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# or source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python run.py
```

#### Frontend Setup  
```bash
npm install
npm start
```

## 🏗️ Architecture

**React Frontend** ↔ **Python Flask API** ↔ **External APIs (USDA, Google Vision)**

- **Frontend**: Modern React app with camera integration
- **Backend**: Python Flask API with AI image recognition
- **Database**: 50+ popular vending machine products with nutrition data
- **APIs**: USDA FoodData Central, Edamam, Spoonacular, Google Vision

## 🔧 Configuration

### API Keys (Optional but Recommended)

1. **USDA FoodData Central** (Free) - [Get API Key](https://fdc.nal.usda.gov/api-guide.html)
2. **Google Vision API** (Paid) - [Get API Key](https://cloud.google.com/vision/docs/setup)
3. **Edamam Nutrition API** (Free tier) - [Sign Up](https://developer.edamam.com/)

Add your keys to `backend/.env`:
```bash
USDA_API_KEY=your-key-here
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

**Note**: The app works great without API keys using our comprehensive mock database!

## 📱 Features

- 📸 **Camera Integration**: Scan vending machines with your webcam or mobile camera
- 🤖 **AI Recognition**: Google Vision API + intelligent product detection
- 📊 **Nutrition Data**: Real nutrition facts from USDA and other APIs
- ⭐ **Health Scoring**: 1-10 health rating for each product
- 📱 **Mobile Ready**: Responsive design works on all devices
- 🔄 **Offline Mode**: Mock data ensures app works without internet

## 🎯 How It Works

1. **Point & Scan**: Use your camera to capture a vending machine
2. **AI Detection**: Our Python backend analyzes the image and detects products
3. **Choose Product**: Select from the detected snacks and drinks
4. **Get Nutrition**: View detailed nutrition facts and health scores
5. **Make Smart Choices**: Use the information to pick healthier options!

## 🛠️ Development

### Project Structure
```
SnackScan/
├── src/                    # React frontend
│   ├── components/         # React components
│   └── services/          # API clients
├── backend/               # Python Flask API
│   ├── services/          # Core business logic
│   ├── app.py            # Flask app
│   └── requirements.txt   # Python dependencies
├── start-full-app.bat    # One-click startup (Windows)
└── CLAUDE.md            # Development guide
```

### Available Commands
```bash
# Development
npm start              # Start React frontend
cd backend && python run.py  # Start Python backend
npm run start:full     # Start both simultaneously

# Building
npm run build          # Build React for production

# Backend Management
npm run backend:install    # Install Python dependencies
npm run backend:dev       # Start backend in dev mode
```

## 🧪 Testing

- **Frontend**: Jest + React Testing Library (`npm test`)
- **Backend**: pytest framework (`cd backend && pytest`)
- **Manual Testing**: Use the included batch files for quick testing

## 🌟 Sample Products Detected

The app recognizes 50+ popular vending machine items including:

**Beverages**: Coca-Cola, Pepsi, Mountain Dew, Sprite, Dasani Water, Gatorade  
**Candy**: Snickers, M&Ms, Reese's Cups, Kit Kat, Twix, Skittles  
**Chips**: Lays, Doritos, Cheetos, Pringles, Sun Chips  
**Healthy**: Granola bars, nuts, energy bars, bottled water  

## 📊 Nutrition Data Sources

1. **USDA FoodData Central** - Comprehensive, government database
2. **Edamam Nutrition API** - Excellent for branded products  
3. **Spoonacular API** - Premium nutrition data
4. **Enhanced Mock Database** - 200+ products with accurate nutrition facts

## 🤝 Contributing

This is a demo project showcasing full-stack development with React and Python. Feel free to:

- Add new vending machine products to the database
- Improve image recognition accuracy
- Add new nutrition APIs
- Enhance the UI/UX

## 📄 License

This project is for educational and demonstration purposes.

---

**Made with ❤️ using React + Python Flask**

Start making smarter snack choices today! 🥗✨