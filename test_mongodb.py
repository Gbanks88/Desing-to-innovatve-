from pymongo import MongoClient
from dotenv import load_dotenv
import os

def test_mongodb_connection():
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB connection details
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    cluster_id = "jcmel"  # Using your cluster ID
    db_name = os.getenv('DB_NAME', 'fashion_platform')
    
    # Construct MongoDB URI
    mongo_uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.{cluster_id}.mongodb.net/{db_name}?retryWrites=true&w=majority"
    
    print("\n[INFO] Testing MongoDB Connection")
    print(f"Database: {db_name}")
    print(f"Cluster: cluster0.{cluster_id}.mongodb.net")
    print(f"Connection URI: {mongo_uri}")
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        
        # Test the connection by listing databases
        print("\n[TEST] Listing databases...")
        databases = client.list_database_names()
        print(f"Available databases: {databases}")
        
        print("\n[SUCCESS] Successfully connected to MongoDB!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error connecting to MongoDB: {str(e)}")
        return False
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    success = test_mongodb_connection()
    exit(0 if success else 1)
