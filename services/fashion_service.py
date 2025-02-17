from flask import current_app
from bson import ObjectId
from datetime import datetime

class FashionService:
    def __init__(self):
        self._db = None
        self._es = None
        self._collection = None
    
    @property
    def db(self):
        if self._db is None:
            self._db = current_app.mongo_db
        return self._db
    
    @property
    def es(self):
        if self._es is None:
            self._es = current_app.es
        return self._es
    
    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.db.fashion_posts
        return self._collection
    
    def create_post(self, data):
        data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        
        # Index in Elasticsearch for search
        self.es.index(index='fashion', id=str(result.inserted_id), body=data)
        return data
    
    def get_posts(self, page, limit, category=None, search_query=None):
        skip = (page - 1) * limit
        
        if search_query:
            # Search in Elasticsearch
            es_query = {
                "query": {
                    "bool": {
                        "must": [{"multi_match": {
                            "query": search_query,
                            "fields": ["title", "description", "tags"]
                        }}]
                    }
                }
            }
            
            if category:
                es_query["query"]["bool"]["filter"] = [{"term": {"category": category}}]
            
            es_result = self.es.search(index='fashion', body=es_query, from_=skip, size=limit)
            return {
                "items": [hit["_source"] for hit in es_result["hits"]["hits"]],
                "total": es_result["hits"]["total"]["value"]
            }
        
        # Regular MongoDB query
        query = {}
        if category:
            query["category"] = category
        
        total = self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        
        return {
            "items": [{**item, "_id": str(item["_id"])} for item in cursor],
            "total": total
        }
    
    def get_post_by_id(self, post_id):
        try:
            post = self.collection.find_one({"_id": ObjectId(post_id)})
            if post:
                post["_id"] = str(post["_id"])
            return post
        except:
            return None
    
    def update_post(self, post_id, data):
        try:
            data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$set": data}
            )
            
            if result.modified_count:
                # Update Elasticsearch
                self.es.update(index='fashion', id=post_id, body={"doc": data})
                return self.get_post_by_id(post_id)
            return None
        except:
            return None
    
    def delete_post(self, post_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(post_id)})
            if result.deleted_count:
                # Delete from Elasticsearch
                self.es.delete(index='fashion', id=post_id)
                return True
            return False
        except:
            return False
