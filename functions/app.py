from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection
def get_db():
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    cluster_id = "jcmel"
    db_name = os.getenv('DB_NAME', 'fashion_platform')
    mongo_uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.{cluster_id}.mongodb.net/{db_name}?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)
    return client[db_name]

# API Routes
@app.route('/api/fashion', methods=['GET'])
def get_fashion():
    try:
        db = get_db()
        fashion_items = list(db.fashion.find({}, {'_id': False}))
        return jsonify(fashion_items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/videos', methods=['GET'])
def get_videos():
    try:
        db = get_db()
        videos = list(db.videos.find({}, {'_id': False}))
        return jsonify(videos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scholarships', methods=['GET'])
def get_scholarships():
    try:
        db = get_db()
        scholarships = list(db.scholarships.find({}, {'_id': False}))
        return jsonify(scholarships)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Netlify Function Handler
def handler(event, context):
    # Get the HTTP method and path from the event
    http_method = event['httpMethod']
    path = event['path']
    
    # Create a Flask request context
    with app.test_client() as client:
        # Make the request to the Flask app
        response = client.open(
            path,
            method=http_method,
            json=json.loads(event.get('body', '{}')) if event.get('body') else None
        )
        
        # Convert the response to Netlify function format
        return {
            'statusCode': response.status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE'
            },
            'body': response.get_data(as_text=True)
        }

# For local development
if __name__ == '__main__':
    app.run(port=5000)
