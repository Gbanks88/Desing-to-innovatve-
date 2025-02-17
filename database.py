from pymongo import MongoClient
from elasticsearch import Elasticsearch
from config.config import Config
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['john-allens-fashion']
        
        # Initialize collections
        self.fashion = self.db['fashion']
        self.ai_services = self.db['ai_services']
        self.video_services = self.db['video_services']
        self.scholarships = self.db['scholarships']
        self.users = self.db['users']
        self.analytics = self.db['analytics']

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()

# Collection names constants
COLLECTIONS = {
    'FASHION': 'fashion',
    'AI_SERVICES': 'ai_services',
    'VIDEO_SERVICES': 'video_services',
    'SCHOLARSHIPS': 'scholarships',
    'USERS': 'users',
    'ANALYTICS': 'analytics'
}

def init_db(app):
    # Initialize Elasticsearch
    try:
        es_client = Elasticsearch([Config.ELASTICSEARCH_URL])
        app.es_client = es_client
        print("Elasticsearch connection successful!")
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {str(e)}")
        raise e

def init_elasticsearch_indices(app):
    # Create fashion index
    app.es_client.indices.create(
        index="fashion",
        ignore=400,  # ignore 400 Index Already Exists exception
        body={
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "tags": {"type": "keyword"},
                    "created_at": {"type": "date"}
                }
            }
        }
    )

    # Create videos index
    app.es_client.indices.create(
        index="videos",
        ignore=400,
        body={
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "tags": {"type": "keyword"},
                    "created_at": {"type": "date"}
                }
            }
        }
    )

    # Create scholarships index
    app.es_client.indices.create(
        index="scholarships",
        ignore=400,
        body={
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "requirements": {"type": "text"},
                    "amount": {"type": "float"},
                    "deadline": {"type": "date"},
                    "tags": {"type": "keyword"},
                    "created_at": {"type": "date"}
                }
            }
        }
    )

# This is added so that many files can reuse the function
db = None

def get_db():
    global db
    if db is None:
        db = Database()
    return db
