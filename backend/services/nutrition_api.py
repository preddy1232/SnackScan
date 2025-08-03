#!/usr/bin/env python3
"""
Nutrition API Service for SnackScan
Fetches nutrition data from multiple APIs with fallback strategy
"""

import os
import logging
import requests
import time
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# API Configuration
USDA_API_URL = 'https://api.nal.usda.gov/fdc/v1'
EDAMAM_API_URL = 'https://api.edamam.com/api/nutrition-data/v2'
SPOONACULAR_API_URL = 'https://api.spoonacular.com/food'

# Enhanced product search terms for better API results
PRODUCT_SEARCH_TERMS = {
    # Beverages - Sodas
    'Coca-Cola Classic': ['coca cola classic', 'coke classic', 'coca-cola original'],
    'Diet Coke': ['diet coke', 'coca cola diet', 'coke zero calories'],
    'Pepsi Cola': ['pepsi cola', 'pepsi original', 'pepsi classic'],
    'Diet Pepsi': ['diet pepsi', 'pepsi zero calories', 'pepsi diet'],
    'Mountain Dew': ['mountain dew original', 'mtn dew', 'mountain dew citrus'],
    'Dr Pepper': ['dr pepper original', 'dr. pepper', 'doctor pepper'],
    'Sprite Lemon-Lime Soda': ['sprite original', 'sprite lemon lime', 'sprite clear'],
    'Fanta Orange Soda': ['fanta orange', 'fanta orange soda', 'orange fanta'],
    
    # Candy & Chocolate
    'Snickers Chocolate Bar': ['snickers bar', 'snickers original', 'snickers chocolate peanut'],
    'M&Ms Milk Chocolate': ['m&m milk chocolate', 'mm plain', 'm and m chocolate'],
    'Reeses Peanut Butter Cups': ['reeses cups', 'reese peanut butter cups', 'peanut butter cups'],
    'Kit Kat Wafer Bar': ['kit kat original', 'kitkat wafer', 'kit-kat chocolate'],
    'Twix Caramel Cookie Bar': ['twix original', 'twix caramel', 'twix cookie bar'],
    'Hersheys Milk Chocolate Bar': ['hershey milk chocolate', 'hersheys original', 'hershey bar'],
    'Milky Way Chocolate Bar': ['milky way original', 'milky way bar', 'milky way chocolate'],
    'Skittles Original': ['skittles original', 'skittles fruit', 'skittles candy'],
    
    # Chips & Snacks
    'Lays Classic Potato Chips': ['lays classic', 'lays original', 'lay potato chips original'],
    'Doritos Nacho Cheese': ['doritos nacho cheese', 'doritos original', 'nacho cheese doritos'],
    'Cheetos Crunchy': ['cheetos original', 'cheetos crunchy', 'cheetos cheese puffs'],
    'Pringles Original': ['pringles original', 'pringles classic', 'pringles potato chips'],
    'Fritos Original Corn Chips': ['fritos original', 'fritos corn chips', 'fritos classic'],
    'Sun Chips Original': ['sun chips original', 'sunchips multigrain', 'sun chips whole grain'],
    
    # Cookies & Crackers
    'Oreo Chocolate Sandwich Cookies': ['oreo original', 'oreo chocolate cookies', 'oreo sandwich'],
    'Cheez-It Original Crackers': ['cheez it original', 'cheezit crackers', 'cheese crackers'],
    'Ritz Crackers': ['ritz original crackers', 'ritz round crackers', 'ritz classic'],
    
    # Healthy Options
    'Nature Valley Granola Bar': ['nature valley granola', 'granola bar', 'nature valley oats'],
    'Clif Energy Bar': ['clif bar original', 'clif energy bar', 'cliff bar'],
    'Planters Roasted Peanuts': ['planters peanuts', 'roasted peanuts', 'planters dry roasted'],
    
    # Water & Healthy Beverages
    'Dasani Bottled Water': ['dasani water', 'bottled water', 'purified water'],
    'Aquafina Bottled Water': ['aquafina water', 'aquafina purified', 'bottled water'],
    'Gatorade Sports Drink': ['gatorade original', 'gatorade thirst quencher', 'sports drink'],
    'Red Bull Energy Drink': ['red bull original', 'red bull energy', 'energy drink'],
    'Monster Energy Drink': ['monster energy original', 'monster energy drink', 'energy drink'],
    'Vitaminwater': ['vitamin water', 'vitaminwater enhanced', 'enhanced water'],
}

def get_nutrition_data(product_name: str) -> Optional[Dict[str, Any]]:
    """
    Get nutrition data for a product using multiple API sources
    
    Args:
        product_name: Name of the product to look up
        
    Returns:
        Nutrition data dictionary or None if not found
    """
    logger.info(f"Looking up nutrition for: {product_name}")
    
    try:
        # Get optimized search terms
        search_terms = _get_optimized_search_terms(product_name)
        logger.info(f"Using search terms: {search_terms}")
        
        # Try APIs in order of preference
        for search_term in search_terms:
            # 1. Try USDA API (free, comprehensive)
            usda_key = os.getenv('USDA_API_KEY')
            if usda_key:
                logger.info(f"Trying USDA API with: {search_term}")
                result = _fetch_usda_nutrition(search_term, usda_key)
                if result:
                    logger.info("Found data in USDA database")
                    return result
            
            # 2. Try Edamam API (free tier available)
            edamam_id = os.getenv('EDAMAM_APP_ID')
            edamam_key = os.getenv('EDAMAM_APP_KEY')
            if edamam_id and edamam_key:
                logger.info(f"Trying Edamam API with: {search_term}")
                result = _fetch_edamam_nutrition(search_term, edamam_id, edamam_key)
                if result:
                    logger.info("Found data in Edamam database")
                    return result
            
            # 3. Try Spoonacular API (paid but reliable)
            spoon_key = os.getenv('SPOONACULAR_API_KEY')
            if spoon_key:
                logger.info(f"Trying Spoonacular API with: {search_term}")
                result = _fetch_spoonacular_nutrition(search_term, spoon_key)
                if result:
                    logger.info("Found data in Spoonacular database")
                    return result
        
        # 4. Try FoodData Central fallback (no API key needed)
        logger.info("Trying FoodData Central fallback")
        result = _fetch_fooddata_fallback(search_terms[0])
        if result:
            logger.info("Found data in FoodData Central fallback")
            return result
        
        # 5. Use enhanced mock data
        logger.info("Using enhanced mock nutrition data")
        return _get_enhanced_mock_data(product_name)
        
    except Exception as e:
        logger.error(f"Error getting nutrition data: {e}")
        return _get_enhanced_mock_data(product_name)

def _get_optimized_search_terms(product_name: str) -> List[str]:
    """Get optimized search terms for better API results"""
    normalized = product_name.lower().strip()
    
    # Check for specific product mappings
    for product, terms in PRODUCT_SEARCH_TERMS.items():
        if product.lower() in normalized or normalized in product.lower():
            return terms
    
    # Generate fallback terms
    fallback_terms = [
        product_name,
        product_name.replace('-', ' ').replace('_', ' '),
        ' '.join(product_name.split()[:2]),  # First two words
        product_name.split()[0] if product_name.split() else product_name,  # Brand name
    ]
    
    return [term for term in fallback_terms if len(term.strip()) > 2]

def _fetch_usda_nutrition(search_term: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Fetch nutrition data from USDA FoodData Central API"""
    try:
        # Try branded foods first, then all foods
        search_types = [
            {'dataType': 'Branded', 'pageSize': 3},
            {'dataType': '', 'pageSize': 5}
        ]
        
        for search_config in search_types:
            params = {
                'query': search_term,
                'api_key': api_key,
                'pageSize': search_config['pageSize']
            }
            
            if search_config['dataType']:
                params['dataType'] = search_config['dataType']
            
            response = requests.get(f"{USDA_API_URL}/foods/search", params=params, timeout=10)
            
            if response.status_code != 200:
                continue
            
            data = response.json()
            
            if data.get('foods') and len(data['foods']) > 0:
                # Find best match
                best_food = data['foods'][0]
                for food in data['foods']:
                    if search_term.lower() in food.get('description', '').lower():
                        best_food = food
                        break
                
                # Get detailed nutrition data
                detail_response = requests.get(
                    f"{USDA_API_URL}/food/{best_food['fdcId']}",
                    params={'api_key': api_key},
                    timeout=10
                )
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    return _parse_usda_nutrition(detail_data)
        
        return None
        
    except Exception as e:
        logger.error(f"USDA API error: {e}")
        return None

def _fetch_edamam_nutrition(search_term: str, app_id: str, app_key: str) -> Optional[Dict[str, Any]]:
    """Fetch nutrition data from Edamam API"""
    try:
        # Try different portion descriptions
        portions = [
            f"1 serving {search_term}",
            f"1 package {search_term}",
            f"1 can {search_term}",
            f"100g {search_term}"
        ]
        
        for portion in portions:
            params = {
                'app_id': app_id,
                'app_key': app_key,
                'nutrition-type': 'cooking',
                'ingr': portion
            }
            
            response = requests.get(EDAMAM_API_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('calories', 0) > 0:
                    return _parse_edamam_nutrition(data, search_term)
        
        return None
        
    except Exception as e:
        logger.error(f"Edamam API error: {e}")
        return None

def _fetch_spoonacular_nutrition(search_term: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Fetch nutrition data from Spoonacular API"""
    try:
        # Search for products
        search_params = {
            'query': search_term,
            'apiKey': api_key,
            'number': 3
        }
        
        search_response = requests.get(
            f"{SPOONACULAR_API_URL}/products/search",
            params=search_params,
            timeout=10
        )
        
        if search_response.status_code != 200:
            return None
        
        search_data = search_response.json()
        
        if search_data.get('products'):
            for product in search_data['products'][:3]:
                # Get detailed nutrition info
                detail_response = requests.get(
                    f"{SPOONACULAR_API_URL}/products/{product['id']}",
                    params={'apiKey': api_key},
                    timeout=10
                )
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    if detail_data.get('nutrition') and detail_data['nutrition'].get('nutrients'):
                        return _parse_spoonacular_nutrition(detail_data)
        
        return None
        
    except Exception as e:
        logger.error(f"Spoonacular API error: {e}")
        return None

def _fetch_fooddata_fallback(search_term: str) -> Optional[Dict[str, Any]]:
    """Fetch from FoodData Central without API key (limited)"""
    try:
        params = {
            'query': search_term,
            'pageSize': 1
        }
        
        response = requests.get(
            'https://api.nal.usda.gov/fdc/v1/foods/search',
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('foods') and len(data['foods']) > 0:
                return _parse_usda_nutrition(data['foods'][0])
        
        return None
        
    except Exception as e:
        logger.error(f"FoodData fallback error: {e}")
        return None

def _parse_usda_nutrition(usda_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse USDA nutrition data into standard format"""
    nutrients = {}
    
    if usda_data.get('foodNutrients'):
        for nutrient in usda_data['foodNutrients']:
            name = nutrient.get('nutrient', {}).get('name', '').lower()
            value = nutrient.get('amount', 0)
            unit = nutrient.get('nutrient', {}).get('unitName', '')
            
            if 'energy' in name or 'caloric' in name:
                nutrients['calories'] = round(value)
            elif 'protein' in name:
                nutrients['protein'] = f"{round(value)}{unit}"
            elif 'carbohydrate' in name:
                nutrients['carbs'] = f"{round(value)}{unit}"
            elif 'total lipid' in name or 'fat, total' in name:
                nutrients['fat'] = f"{round(value)}{unit}"
            elif 'fiber' in name:
                nutrients['fiber'] = f"{round(value)}{unit}"
            elif 'sugars, total' in name:
                nutrients['sugar'] = f"{round(value)}{unit}"
            elif 'sodium' in name:
                nutrients['sodium'] = f"{round(value)}{unit}"
    
    serving_size = _get_serving_size(usda_data)
    
    return {
        'name': usda_data.get('description', usda_data.get('lowercaseDescription', 'Unknown')),
        'serving_size': serving_size,
        'calories': nutrients.get('calories', 0),
        'protein': nutrients.get('protein', 'N/A'),
        'carbs': nutrients.get('carbs', 'N/A'),
        'fat': nutrients.get('fat', 'N/A'),
        'fiber': nutrients.get('fiber', 'N/A'),
        'sugar': nutrients.get('sugar', 'N/A'),
        'sodium': nutrients.get('sodium', 'N/A'),
        'health_score': _calculate_health_score(nutrients),
        'source': 'USDA FoodData Central'
    }

def _parse_edamam_nutrition(edamam_data: Dict[str, Any], product_name: str) -> Dict[str, Any]:
    """Parse Edamam nutrition data into standard format"""
    nutrients = edamam_data.get('totalNutrients', {})
    
    calories = round(edamam_data.get('calories', 0))
    protein = round(nutrients.get('PROCNT', {}).get('quantity', 0)) if 'PROCNT' in nutrients else 0
    carbs = round(nutrients.get('CHOCDF', {}).get('quantity', 0)) if 'CHOCDF' in nutrients else 0
    fat = round(nutrients.get('FAT', {}).get('quantity', 0)) if 'FAT' in nutrients else 0
    fiber = round(nutrients.get('FIBTG', {}).get('quantity', 0)) if 'FIBTG' in nutrients else 0
    sugar = round(nutrients.get('SUGAR', {}).get('quantity', 0)) if 'SUGAR' in nutrients else 0
    sodium = round(nutrients.get('NA', {}).get('quantity', 0)) if 'NA' in nutrients else 0
    
    nutrient_dict = {
        'calories': calories,
        'protein': protein,
        'fiber': fiber,
        'sugar': sugar,
        'sodium': sodium
    }
    
    return {
        'name': product_name,
        'serving_size': '1 serving',
        'calories': calories,
        'protein': f"{protein}g",
        'carbs': f"{carbs}g",
        'fat': f"{fat}g",
        'fiber': f"{fiber}g",
        'sugar': f"{sugar}g",
        'sodium': f"{sodium}mg",
        'health_score': _calculate_health_score(nutrient_dict),
        'source': 'Edamam Nutrition API'
    }

def _parse_spoonacular_nutrition(spoon_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse Spoonacular nutrition data into standard format"""
    nutrition = spoon_data.get('nutrition', {})
    nutrients = nutrition.get('nutrients', [])
    
    def get_nutrient(name):
        for nutrient in nutrients:
            if name.lower() in nutrient.get('name', '').lower():
                return round(nutrient.get('amount', 0))
        return 0
    
    calories = get_nutrient('calories')
    protein = get_nutrient('protein')
    carbs = get_nutrient('carbohydrates')
    fat = get_nutrient('fat')
    fiber = get_nutrient('fiber')
    sugar = get_nutrient('sugar')
    sodium = get_nutrient('sodium')
    
    nutrient_dict = {
        'calories': calories,
        'protein': protein,
        'fiber': fiber,
        'sugar': sugar,
        'sodium': sodium
    }
    
    servings = spoon_data.get('servings', {})
    serving_size = f"{servings.get('size', 1)} {servings.get('unit', 'serving')}" if servings else '1 serving'
    
    return {
        'name': spoon_data.get('title', 'Unknown Product'),
        'serving_size': serving_size,
        'calories': calories,
        'protein': f"{protein}g",
        'carbs': f"{carbs}g",
        'fat': f"{fat}g",
        'fiber': f"{fiber}g",
        'sugar': f"{sugar}g",
        'sodium': f"{sodium}mg",
        'health_score': _calculate_health_score(nutrient_dict),
        'source': 'Spoonacular API'
    }

def _get_serving_size(usda_data: Dict[str, Any]) -> str:
    """Extract serving size from USDA data"""
    if usda_data.get('servingSize') and usda_data.get('servingSizeUnit'):
        return f"{usda_data['servingSize']} {usda_data['servingSizeUnit']}"
    elif usda_data.get('householdServingFullText'):
        return usda_data['householdServingFullText']
    else:
        return '1 serving'

def _calculate_health_score(nutrients: Dict[str, Any]) -> int:
    """Calculate health score from 1-10 based on nutritional content"""
    score = 5  # Start neutral
    
    # Positive factors
    protein_val = _extract_number(nutrients.get('protein', 0))
    fiber_val = _extract_number(nutrients.get('fiber', 0))
    calories_val = _extract_number(nutrients.get('calories', 0))
    
    if protein_val > 3:
        score += 1
    if fiber_val > 2:
        score += 1
    if calories_val < 100:
        score += 1
    
    # Negative factors
    sugar_val = _extract_number(nutrients.get('sugar', 0))
    sodium_val = _extract_number(nutrients.get('sodium', 0))
    fat_val = _extract_number(nutrients.get('fat', 0))
    
    if sugar_val > 15:
        score -= 1
    if sodium_val > 200:
        score -= 1
    if calories_val > 200:
        score -= 1
    if fat_val > 10:
        score -= 1
    
    return max(1, min(10, score))

def _extract_number(value: Any) -> float:
    """Extract numeric value from string or return the number"""
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, str):
        # Extract first number from string
        import re
        match = re.search(r'\d+\.?\d*', value)
        return float(match.group()) if match else 0
    else:
        return 0

def _get_enhanced_mock_data(product_name: str) -> Dict[str, Any]:
    """Get enhanced mock nutrition data for common vending machine products"""
    
    # Comprehensive mock database
    mock_database = {
        # Beverages - Sodas
        'coca-cola classic': {'name': 'Coca-Cola Classic', 'serving_size': '12 fl oz (355ml)', 'calories': 140, 'protein': '0g', 'carbs': '39g', 'fat': '0g', 'fiber': '0g', 'sugar': '39g', 'sodium': '45mg', 'health_score': 2},
        'diet coke': {'name': 'Diet Coke', 'serving_size': '12 fl oz (355ml)', 'calories': 0, 'protein': '0g', 'carbs': '0g', 'fat': '0g', 'fiber': '0g', 'sugar': '0g', 'sodium': '40mg', 'health_score': 6},
        'pepsi cola': {'name': 'Pepsi Cola', 'serving_size': '12 fl oz (355ml)', 'calories': 150, 'protein': '0g', 'carbs': '41g', 'fat': '0g', 'fiber': '0g', 'sugar': '41g', 'sodium': '30mg', 'health_score': 2},
        'mountain dew': {'name': 'Mountain Dew', 'serving_size': '12 fl oz (355ml)', 'calories': 170, 'protein': '0g', 'carbs': '46g', 'fat': '0g', 'fiber': '0g', 'sugar': '46g', 'sodium': '60mg', 'health_score': 1},
        'dr pepper': {'name': 'Dr Pepper', 'serving_size': '12 fl oz (355ml)', 'calories': 150, 'protein': '0g', 'carbs': '40g', 'fat': '0g', 'fiber': '0g', 'sugar': '40g', 'sodium': '55mg', 'health_score': 2},
        'sprite lemon-lime soda': {'name': 'Sprite', 'serving_size': '12 fl oz (355ml)', 'calories': 140, 'protein': '0g', 'carbs': '38g', 'fat': '0g', 'fiber': '0g', 'sugar': '38g', 'sodium': '65mg', 'health_score': 2},
        
        # Candy & Chocolate
        'snickers chocolate bar': {'name': 'Snickers Bar', 'serving_size': '1.86 oz (52.7g)', 'calories': 250, 'protein': '4g', 'carbs': '33g', 'fat': '12g', 'fiber': '1g', 'sugar': '27g', 'sodium': '120mg', 'health_score': 3},
        'm&ms milk chocolate': {'name': 'M&Ms Milk Chocolate', 'serving_size': '1.69 oz (47.9g)', 'calories': 240, 'protein': '2g', 'carbs': '34g', 'fat': '10g', 'fiber': '1g', 'sugar': '31g', 'sodium': '15mg', 'health_score': 2},
        'reeses peanut butter cups': {'name': 'Reeses Peanut Butter Cups', 'serving_size': '1.5 oz (42g)', 'calories': 210, 'protein': '5g', 'carbs': '24g', 'fat': '13g', 'fiber': '2g', 'sugar': '21g', 'sodium': '135mg', 'health_score': 3},
        'kit kat wafer bar': {'name': 'Kit Kat', 'serving_size': '1.5 oz (42g)', 'calories': 210, 'protein': '3g', 'carbs': '27g', 'fat': '11g', 'fiber': '1g', 'sugar': '22g', 'sodium': '16mg', 'health_score': 2},
        
        # Chips & Snacks
        'lays classic potato chips': {'name': 'Lays Classic Chips', 'serving_size': '1 oz (28g)', 'calories': 160, 'protein': '2g', 'carbs': '15g', 'fat': '10g', 'fiber': '1g', 'sugar': '0g', 'sodium': '170mg', 'health_score': 3},
        'doritos nacho cheese': {'name': 'Doritos Nacho Cheese', 'serving_size': '1 oz (28g)', 'calories': 150, 'protein': '2g', 'carbs': '18g', 'fat': '8g', 'fiber': '1g', 'sugar': '1g', 'sodium': '210mg', 'health_score': 3},
        'cheetos crunchy': {'name': 'Cheetos Crunchy', 'serving_size': '1 oz (28g)', 'calories': 160, 'protein': '2g', 'carbs': '13g', 'fat': '10g', 'fiber': '1g', 'sugar': '1g', 'sodium': '250mg', 'health_score': 2},
        
        # Healthy Options
        'nature valley granola bar': {'name': 'Nature Valley Granola Bar', 'serving_size': '1 bar (42g)', 'calories': 190, 'protein': '4g', 'carbs': '29g', 'fat': '7g', 'fiber': '3g', 'sugar': '11g', 'sodium': '160mg', 'health_score': 6},
        'clif energy bar': {'name': 'Clif Bar', 'serving_size': '1 bar (68g)', 'calories': 250, 'protein': '9g', 'carbs': '44g', 'fat': '5g', 'fiber': '5g', 'sugar': '21g', 'sodium': '200mg', 'health_score': 7},
        'planters roasted peanuts': {'name': 'Planters Peanuts', 'serving_size': '1 oz (28g)', 'calories': 170, 'protein': '7g', 'carbs': '5g', 'fat': '14g', 'fiber': '2g', 'sugar': '1g', 'sodium': '115mg', 'health_score': 7},
        
        # Water & Beverages
        'dasani bottled water': {'name': 'Dasani Water', 'serving_size': '16.9 fl oz (500ml)', 'calories': 0, 'protein': '0g', 'carbs': '0g', 'fat': '0g', 'fiber': '0g', 'sugar': '0g', 'sodium': '0mg', 'health_score': 10},
        'gatorade sports drink': {'name': 'Gatorade', 'serving_size': '12 fl oz (355ml)', 'calories': 80, 'protein': '0g', 'carbs': '21g', 'fat': '0g', 'fiber': '0g', 'sugar': '21g', 'sodium': '160mg', 'health_score': 5},
    }
    
    # Normalize product name for lookup
    key = product_name.lower().replace('-', ' ').replace('_', ' ').strip()
    
    # Try exact match
    if key in mock_database:
        result = mock_database[key].copy()
        result['source'] = 'Enhanced Vending Database'
        return result
    
    # Try partial matching
    for mock_key, mock_data in mock_database.items():
        if any(word in mock_key for word in key.split()) or any(word in key for word in mock_key.split()):
            result = mock_data.copy()
            result['source'] = 'Enhanced Vending Database'
            return result
    
    # Generic fallback
    return {
        'name': product_name,
        'serving_size': '1 serving',
        'calories': 150,
        'protein': '2g',
        'carbs': '20g',
        'fat': '6g',
        'fiber': '1g',
        'sugar': '12g',
        'sodium': '100mg',
        'health_score': 4,
        'source': 'Estimated Values'
    }