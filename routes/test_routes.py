from flask import Blueprint, jsonify
from pymongo import MongoClient
import os
from elasticsearch import Elasticsearch
from google.cloud import storage
import datetime

test_bp = Blueprint('test', __name__)

@test_bp.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@test_bp.route('/test-mongo')
def test_mongo():
    try:
        client = MongoClient(os.getenv('MONGO_URI'))
        db = client[os.getenv('DB_NAME', 'fashion_platform')]
        collections = db.list_collection_names()
        
        return jsonify({
            "status": "success",
            "message": "MongoDB connection successful",
            "collections": collections,
            "database": db.name
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"MongoDB connection failed: {str(e)}"
        }), 500
    finally:
        if 'client' in locals():
            client.close()

@test_bp.route('/test-elasticsearch')
def test_elasticsearch():
    try:
        es = Elasticsearch(os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200'))
        health = es.cluster.health()
        
        return jsonify({
            "status": "success",
            "message": "Elasticsearch connection successful",
            "cluster_health": health
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Elasticsearch connection failed: {str(e)}"
        }), 500

@test_bp.route('/test-gcp')
def test_gcp():
    try:
        storage_client = storage.Client.from_service_account_json(
            os.getenv('GCP_CREDENTIALS_FILE')
        )
        bucket = storage_client.bucket(os.getenv('GCP_BUCKET_NAME'))
        
        return jsonify({
            "status": "success",
            "message": "GCP connection successful",
            "bucket": bucket.name,
            "project": storage_client.project
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"GCP connection failed: {str(e)}"
        }), 500
