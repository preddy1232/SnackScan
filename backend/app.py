#!/usr/bin/env python3
"""
SnackScan Backend API
A Flask API for vending machine image recognition and nutrition data
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Import our services
from services.image_recognition import analyze_image
from services.nutrition_api import get_nutrition_data

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SnackScan Backend API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analyze-image', methods=['POST'])
def analyze_vending_image():
    """
    Analyze uploaded vending machine image for products
    
    Returns:
        JSON response with detected products
    """
    try:
        # Check if image file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save uploaded file temporarily
        filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f"Processing image: {filename}")
        
        # Analyze image for products
        products = analyze_image(filepath)
        
        # Clean up temporary file
        try:
            os.remove(filepath)
        except OSError:
            logger.warning(f"Could not remove temporary file: {filepath}")
        
        logger.info(f"Found {len(products)} products in image")
        
        return jsonify({
            'success': True,
            'products': products,
            'count': len(products)
        })
        
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to analyze image',
            'details': str(e)
        }), 500

@app.route('/api/nutrition/<product_name>', methods=['GET'])
def get_product_nutrition(product_name):
    """
    Get nutrition data for a specific product
    
    Args:
        product_name: Name of the product to look up
        
    Returns:
        JSON response with nutrition information
    """
    try:
        if not product_name or len(product_name.strip()) == 0:
            return jsonify({'error': 'Product name is required'}), 400
        
        logger.info(f"Looking up nutrition for: {product_name}")
        
        # Get nutrition data
        nutrition_data = get_nutrition_data(product_name.strip())
        
        if not nutrition_data:
            return jsonify({
                'success': False,
                'error': 'Nutrition data not found'
            }), 404
        
        logger.info(f"Found nutrition data for: {product_name}")
        
        return jsonify({
            'success': True,
            'nutrition': nutrition_data
        })
        
    except Exception as e:
        logger.error(f"Error getting nutrition data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get nutrition data',
            'details': str(e)
        }), 500

@app.route('/api/products', methods=['GET'])
def get_available_products():
    """
    Get list of all available products in our database
    
    Returns:
        JSON response with product list
    """
    try:
        # Import the product database
        from services.image_recognition import COMPREHENSIVE_VENDING_PRODUCTS
        
        products = []
        for product in COMPREHENSIVE_VENDING_PRODUCTS:
            products.append({
                'name': product['official'],
                'category': product['category'],
                'popularity': product['popularity'],
                'description': product.get('description', '')
            })
        
        # Sort by popularity
        products.sort(key=lambda x: x['popularity'], reverse=True)
        
        return jsonify({
            'success': True,
            'products': products,
            'count': len(products)
        })
        
    except Exception as e:
        logger.error(f"Error getting products: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get products',
            'details': str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting SnackScan Backend API on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)