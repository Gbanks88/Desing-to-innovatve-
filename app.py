from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config import Config
from routes.fashion_routes import fashion_bp
from routes.video_routes import video_bp
from routes.scholarship_routes import scholarship_bp
from routes.test_routes import test_bp
from database import init_db

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(fashion_bp, url_prefix=f"{Config.BASE_URL}/fashion")
    app.register_blueprint(video_bp, url_prefix=f"{Config.BASE_URL}/videos")
    app.register_blueprint(scholarship_bp, url_prefix=f"{Config.BASE_URL}/scholarships")
    app.register_blueprint(test_bp, url_prefix=f"{Config.BASE_URL}/test")
    
    @app.route('/')
    def hello():
        return jsonify({
            "message": "Welcome to Fun Life Backend!",
            "version": Config.API_VERSION,
            "endpoints": [
                f"{Config.BASE_URL}/fashion",
                f"{Config.BASE_URL}/videos",
                f"{Config.BASE_URL}/scholarships",
                f"{Config.BASE_URL}/test"
            ]
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
