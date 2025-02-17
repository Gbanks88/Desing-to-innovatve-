from google.cloud import storage
from config.config import Config
import os
from datetime import datetime

class TestConfig:
    # Database Configuration
    MONGODB_URI = os.getenv('TEST_MONGODB_URI', 'mongodb://localhost:27017/')
    DB_NAME = 'john-allens-fashion-test'
    
    # API Configuration
    API_VERSION = 'v1'
    API_PREFIX = '/api/john-allens-fashion'
    
    # Test Server Configuration
    TEST_SERVER_HOST = 'localhost'
    TEST_SERVER_PORT = 5001
    
    # Test Data Paths
    TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
    
    # Service Configurations
    AI_SERVICE_ENDPOINT = f"{API_PREFIX}/ai"
    VIDEO_SERVICE_ENDPOINT = f"{API_PREFIX}/video"
    SCHOLARSHIP_SERVICE_ENDPOINT = f"{API_PREFIX}/scholarships"
    
    # Test User Credentials
    TEST_USER = {
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test@john-allens-fashion.com'
    }
    
    # Test API Keys
    TEST_API_KEY = os.getenv('TEST_API_KEY', 'test-api-key')

def test_gcp_connection():
    try:
        print(f"Using credentials file: {Config.GCP_CREDENTIALS_FILE}")
        print(f"Using bucket name: {Config.GCP_BUCKET_NAME}")
        
        # Initialize the storage client
        storage_client = storage.Client.from_service_account_json(Config.GCP_CREDENTIALS_FILE)
        
        # Get the bucket
        bucket = storage_client.bucket(Config.GCP_BUCKET_NAME)
        
        # Create a test file
        test_blob_name = f"test/test-{datetime.utcnow().timestamp()}.txt"
        blob = bucket.blob(test_blob_name)
        
        # Upload some test content
        blob.upload_from_string('Hello, World!')
        print(f"[PASS] Successfully uploaded test file to GCS: {test_blob_name}")
        
        # Download the content
        content = blob.download_as_string()
        print(f"[PASS] Successfully downloaded test file content: {content}")
        
        # Delete the test file
        blob.delete()
        print(f"[PASS] Successfully deleted test file")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Testing GCP connection: {str(e)}")
        return False

def test_mongodb_connection():
    try:
        from pymongo import MongoClient
        
        print(f"Using MongoDB URI: {TestConfig.MONGODB_URI}")
        
        # Create MongoDB client
        client = MongoClient(TestConfig.MONGODB_URI)
        
        # Test connection by listing database names
        dbs = client.list_database_names()
        print(f"[PASS] Successfully connected to MongoDB. Available databases: {dbs}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Testing MongoDB connection: {str(e)}")
        return False

def test_elasticsearch_connection():
    try:
        from elasticsearch import Elasticsearch
        
        print(f"Using Elasticsearch URL: {Config.ELASTICSEARCH_URL}")
        
        # Create Elasticsearch client
        es = Elasticsearch(Config.ELASTICSEARCH_URL)
        
        # Test connection
        if es.ping():
            print("[PASS] Successfully connected to Elasticsearch")
            return True
        else:
            print("[ERROR] Could not connect to Elasticsearch")
            return False
            
    except Exception as e:
        print(f"[ERROR] Testing Elasticsearch connection: {str(e)}")
        return False

if __name__ == "__main__":
    print("\nTesting configuration...\n")
    
    # Test GCP
    print("Testing Google Cloud Storage connection:")
    gcp_success = test_gcp_connection()
    print()
    
    # Test MongoDB
    print("Testing MongoDB connection:")
    mongo_success = test_mongodb_connection()
    print()
    
    # Test Elasticsearch
    print("Testing Elasticsearch connection:")
    es_success = test_elasticsearch_connection()
    print()
    
    # Summary
    print("\nTest Summary:")
    print(f"[{'PASS' if gcp_success else 'FAIL'}] Google Cloud Storage")
    print(f"[{'PASS' if mongo_success else 'FAIL'}] MongoDB")
    print(f"[{'PASS' if es_success else 'FAIL'}] Elasticsearch")
    
    # Exit with appropriate status code
    exit(0 if all([gcp_success, mongo_success, es_success]) else 1)
