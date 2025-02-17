from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pprint import pprint
import json
from datetime import datetime

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError(f"Unknown type {type(x)}")

def view_collections():
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB connection details
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    cluster_id = "jcmel"
    db_name = os.getenv('DB_NAME', 'fashion_platform')
    
    # Construct MongoDB URI
    mongo_uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.{cluster_id}.mongodb.net/{db_name}?retryWrites=true&w=majority"
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        collections = ['fashion', 'videos', 'scholarships']
        
        for collection_name in collections:
            print(f"\n{'='*50}")
            print(f"Collection: {collection_name}")
            print('='*50)
            
            collection = db[collection_name]
            documents = list(collection.find())
            
            if not documents:
                print("No documents found in this collection")
                continue
            
            for doc in documents:
                # Convert ObjectId to string for better readability
                doc['_id'] = str(doc['_id'])
                # Convert to JSON and back to handle datetime objects
                doc_str = json.dumps(doc, default=datetime_handler, indent=2)
                print("\nDocument:")
                print(doc_str)
            
            print(f"\nTotal documents in {collection_name}: {len(documents)}")
        
    except Exception as e:
        print(f"Error viewing collections: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    view_collections()
