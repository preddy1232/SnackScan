#!/usr/bin/env python3
"""
SnackScan Backend Runner
Simple script to start the Flask development server
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

if __name__ == '__main__':
    from app import app
    
    # Configuration
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true' 
    
    print(f"Starting SnackScan Backend API")
    print(f"Server: http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Working directory: {backend_dir}")
    print("=" * 50)
    
    # Start the Flask app
    app.run(host=host, port=port, debug=debug)