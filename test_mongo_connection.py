import os
from dotenv import load_dotenv
from pymongo import MongoClient
import sys

def test_mongodb_connection():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB connection string
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            print("[ERROR] MONGO_URI environment variable not found")
            return False
            
        print(f"Attempting to connect to MongoDB...")
        
        # Create MongoDB client
        client = MongoClient(mongo_uri)
        
        # Test connection by listing database names
        dbs = client.list_database_names()
        print(f"[SUCCESS] Connected to MongoDB Atlas!")
        print(f"Available databases: {dbs}")
        
        # Get the fashion platform database
        db = client[os.getenv('DB_NAME', 'fashion_platform')]
        
        # List collections in the database
        collections = db.list_collection_names()
        print(f"\nCollections in {db.name}:")
        for collection in collections:
            print(f"- {collection}")
            # Get count of documents in collection
            count = db[collection].count_documents({})
            print(f"  Documents: {count}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {str(e)}")
        return False
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
