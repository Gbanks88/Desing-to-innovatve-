import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Get base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    # Base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # API Configuration
    API_VERSION = "v1"
    BASE_URL = f"/api/{API_VERSION}"
    
    # Google Cloud Storage Configuration
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'john-allens-fashion')
    GCP_BUCKET_NAME = os.getenv('GCP_BUCKET_NAME', 'john-allens-fashion-storage')
    GCP_CREDENTIALS_FILE = os.path.join(BASE_DIR, os.getenv('GCP_CREDENTIALS_FILE', 'credentials/service-account.json'))
    
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/fashion_platform')
    DB_NAME = os.getenv('DB_NAME', 'fashion_platform')
    
    # Elasticsearch Configuration
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # File Upload Configuration
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
