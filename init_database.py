from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

def init_database():
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
        
        # Create collections with sample data
        # 1. Fashion Collection
        fashion_collection = db['fashion']
        fashion_items = [
            {
                "title": "Summer Collection 2025",
                "description": "Latest trending summer fashion items",
                "category": "seasonal",
                "tags": ["summer", "trending", "2025"],
                "items": [
                    {"name": "Floral Dress", "price": 89.99},
                    {"name": "Linen Shorts", "price": 45.99}
                ],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Sustainable Fashion",
                "description": "Eco-friendly fashion collection",
                "category": "sustainable",
                "tags": ["eco-friendly", "sustainable", "organic"],
                "items": [
                    {"name": "Organic Cotton T-Shirt", "price": 29.99},
                    {"name": "Recycled Denim Jeans", "price": 79.99}
                ],
                "created_at": datetime.utcnow()
            }
        ]
        fashion_collection.insert_many(fashion_items)
        print("Created fashion collection with sample data")
        
        # 2. Videos Collection
        videos_collection = db['videos']
        video_items = [
            {
                "title": "Summer Fashion Tips 2025",
                "description": "Learn the latest summer fashion trends",
                "url": "https://example.com/videos/summer-fashion-2025",
                "duration": "10:30",
                "tags": ["fashion", "tutorial", "summer"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Sustainable Fashion Guide",
                "description": "Complete guide to sustainable fashion",
                "url": "https://example.com/videos/sustainable-fashion",
                "duration": "15:45",
                "tags": ["sustainable", "guide", "eco-friendly"],
                "created_at": datetime.utcnow()
            }
        ]
        videos_collection.insert_many(video_items)
        print("Created videos collection with sample data")
        
        # 3. Scholarships Collection
        scholarships_collection = db['scholarships']
        scholarship_items = [
            {
                "title": "Fashion Design Excellence Scholarship",
                "description": "Scholarship for aspiring fashion designers",
                "amount": 5000.00,
                "deadline": datetime(2025, 8, 31),
                "requirements": [
                    "Portfolio submission",
                    "3.5 GPA minimum",
                    "Letter of recommendation"
                ],
                "tags": ["design", "undergraduate", "fashion"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Sustainable Fashion Innovation Grant",
                "description": "Grant for sustainable fashion projects",
                "amount": 7500.00,
                "deadline": datetime(2025, 9, 30),
                "requirements": [
                    "Project proposal",
                    "Sustainability impact statement",
                    "Budget plan"
                ],
                "tags": ["sustainable", "innovation", "grant"],
                "created_at": datetime.utcnow()
            }
        ]
        scholarships_collection.insert_many(scholarship_items)
        print("Created scholarships collection with sample data")
        
        print("\nDatabase initialization completed successfully!")
        
        # Print collection statistics
        print("\nCollection Statistics:")
        print(f"Fashion items: {fashion_collection.count_documents({})}")
        print(f"Videos: {videos_collection.count_documents({})}")
        print(f"Scholarships: {scholarships_collection.count_documents({})}")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    init_database()
