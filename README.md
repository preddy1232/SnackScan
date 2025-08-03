<div align="center">

# 🍿 SnackScan  
### *Snap, Scan, Snack Smart.*  

**SnackScan** is a **full-stack web application** that helps users make healthier snack choices by scanning vending machines with their camera.  
Using **AI-powered image recognition**, it detects snack products and provides **comprehensive nutritional information** to support informed decisions.  

---

## 🚀 Features  

- 📸 **Camera Integration** – Scan vending machines via webcam or mobile camera  
- 🤖 **AI Recognition** – Detect products using Google Vision API and custom logic  
- 📊 **Nutrition Data** – Pull verified nutrition facts from USDA and other APIs  
- ⭐ **Health Scoring** – Rate products from 1–10 based on nutritional quality  
- 📱 **Mobile-Friendly** – Fully responsive design for all devices  
- 🔄 **Offline Mode** – Works without internet using a built-in mock database  

---

## 🏗 Architecture  

**React Frontend** ↔ **Python Flask API** ↔ **External APIs**  
*(USDA, Google Vision, Edamam, Spoonacular)*  

- **Frontend**: React with camera integration and responsive UI  
- **Backend**: Python Flask API with AI image recognition  
- **Database**: 200+ popular vending machine products with nutrition data  
- **External APIs**: USDA FoodData Central, Edamam, Spoonacular, Google Vision  

</div>
