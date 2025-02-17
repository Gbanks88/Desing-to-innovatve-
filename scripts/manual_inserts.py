from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Atlas connection
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME', 'fashion_platform')
MONGODB_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster1.jcmel.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&appName=Cluster1"

def connect_db():
    try:
        print(f"Connecting to MongoDB with URI: {MONGODB_URI.replace(DB_PASSWORD, '*' * len(DB_PASSWORD))}")
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        print(f"Connected to MongoDB Atlas: {DB_NAME}")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def insert_fashion():
    try:
        db = connect_db()
        if db is None:
            return
        fashion_items = [
            {
                "name": "Designer Suit Collection 2025",
                "description": "Exclusive hand-tailored designer suits",
                "category": "Suits",
                "price": 1299.99,
                "images": [
                    "https://cdn.johnallens.com/images/design.png",
                    "https://cdn.johnallens.com/images/design(1).png"
                ],
                "sizes": ["S", "M", "L", "XL"],
                "colors": ["Black", "Navy", "Charcoal"],
                "inStock": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Premium Fashion Line",
                "description": "Contemporary fashion pieces for the modern professional",
                "category": "Fashion",
                "price": 899.99,
                "images": [
                    "https://cdn.johnallens.com/images/design(2).png",
                    "https://cdn.johnallens.com/images/design(3).png"
                ],
                "sizes": ["S", "M", "L"],
                "colors": ["White", "Blue", "Gray"],
                "inStock": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = db.fashion.insert_many(fashion_items)
        print(f"Inserted {len(result.inserted_ids)} fashion items")
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting fashion items: {e}")

def insert_ai_services():
    try:
        db = connect_db()
        if db is None:
            return
        services = [
            {
                "name": "Fashion Style Analysis",
                "description": "AI-powered fashion style analysis and recommendations",
                "type": "style_analysis",
                "parameters": {
                    "color_analysis": True,
                    "style_matching": True,
                    "trend_prediction": True
                },
                "active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Personal Fashion Assistant",
                "description": "AI assistant for personalized fashion advice",
                "type": "personal_assistant",
                "parameters": {
                    "wardrobe_analysis": True,
                    "outfit_suggestions": True,
                    "shopping_recommendations": True
                },
                "active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = db.ai_services.insert_many(services)
        print(f"Inserted {len(result.inserted_ids)} AI services")
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting AI services: {e}")

def insert_video_services():
    try:
        db = connect_db()
        if db is None:
            return
        videos = [
            {
                "title": "Fashion Collection Showcase",
                "description": "Spring 2025 Collection Preview",
                "url": "https://cdn.johnallens.com/videos/video_full.mp4",
                "type": "showcase",
                "duration": 180,
                "thumbnail": "https://cdn.johnallens.com/images/design.png",
                "active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = db.video_services.insert_many(videos)
        print(f"Inserted {len(result.inserted_ids)} video services")
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting video services: {e}")

def insert_scholarships():
    try:
        db = connect_db()
        if db is None:
            return
        scholarships = [
            {
                "name": "Fashion Innovation Scholarship",
                "description": "Scholarship for innovative fashion design students",
                "amount": 5000,
                "deadline": "2025-06-01",
                "requirements": [
                    "Portfolio submission",
                    "Design proposal",
                    "Academic transcripts"
                ],
                "status": "active",
                "created_at": datetime.utcnow()
            }
        ]

        result = db.scholarships.insert_many(scholarships)
        print(f"Inserted {len(result.inserted_ids)} scholarships")
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting scholarships: {e}")

def insert_users():
    try:
        db = connect_db()
        if db is None:
            return
        users = [
            {
                "email": "admin@johnallens.com",
                "role": "admin",
                "profile": {
                    "firstName": "John",
                    "lastName": "Allen",
                    "phone": "+1-555-0123"
                },
                "preferences": {
                    "newsletter": True,
                    "notifications": True
                },
                "created_at": datetime.utcnow()
            }
        ]

        result = db.users.insert_many(users)
        print(f"Inserted {len(result.inserted_ids)} users")
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting users: {e}")

def insert_analytics():
    try:
        db = connect_db()
        if db is None:
            return
        analytics = [
            {
                "type": "page_view",
                "page": "homepage",
                "count": 0,
                "created_at": datetime.utcnow()
            },
            {
                "type": "service_usage",
                "service": "style_analysis",
                "count": 0,
                "created_at": datetime.utcnow()
            }
        ]

        result = db.analytics.insert_many(analytics)
        print(f"Inserted {len(result.inserted_ids)} analytics records")
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting analytics: {e}")

def main():
    print("Starting manual database inserts...")
    
    print("\nInserting Fashion Items:")
    insert_fashion()
    
    print("\nInserting AI Services:")
    insert_ai_services()
    
    print("\nInserting Video Services:")
    insert_video_services()
    
    print("\nInserting Scholarships:")
    insert_scholarships()
    
    print("\nInserting Users:")
    insert_users()
    
    print("\nInserting Analytics:")
    insert_analytics()
    
    print("\nDatabase inserts completed!")

if __name__ == "__main__":
    main()
