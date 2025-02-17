from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pprint import pprint

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = 'john-allens-fashion'

def connect_db():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print(f"Connected to MongoDB: {DB_NAME}")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def verify_collection(db, collection_name):
    print(f"\nVerifying {collection_name}:")
    print("-" * 50)
    
    try:
        # Get collection count
        count = db[collection_name].count_documents({})
        print(f"Total documents in {collection_name}: {count}")
        
        # Show sample documents
        print(f"\nSample documents from {collection_name}:")
        for doc in db[collection_name].find().limit(2):
            pprint(doc)
            print()
            
    except Exception as e:
        print(f"Error verifying {collection_name}: {e}")

def main():
    db = connect_db()
    if not db:
        return
    
    # Verify each collection
    collections = ['products', 'users', 'orders', 'content']
    for collection in collections:
        verify_collection(db, collection)
    
    print("\nVerification complete!")

if __name__ == "__main__":
    main()
