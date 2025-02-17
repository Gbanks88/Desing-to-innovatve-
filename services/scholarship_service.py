from flask import current_app
from bson import ObjectId
from datetime import datetime

class ScholarshipService:
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
            self._collection = self.db.scholarships
        return self._collection
    
    def create_scholarship(self, data):
        data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        
        # Index in Elasticsearch
        self.es.index(index='scholarships', id=str(result.inserted_id), body=data)
        return data
    
    def search_scholarships(self, query, filters, page, limit):
        skip = (page - 1) * limit
        
        # Build Elasticsearch query
        es_query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            }
        }
        
        # Add text search if query provided
        if query:
            es_query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description", "requirements"]
                }
            })
        
        # Add filters
        if filters.get('min_amount'):
            es_query["query"]["bool"]["filter"].append({
                "range": {"amount": {"gte": filters['min_amount']}}
            })
        
        if filters.get('max_amount'):
            es_query["query"]["bool"]["filter"].append({
                "range": {"amount": {"lte": filters['max_amount']}}
            })
        
        if filters.get('deadline_after'):
            es_query["query"]["bool"]["filter"].append({
                "range": {"deadline": {"gte": filters['deadline_after']}}
            })
        
        if filters.get('tags'):
            es_query["query"]["bool"]["filter"].append({
                "terms": {"tags": filters['tags']}
            })
        
        # Execute search
        es_result = self.es.search(
            index='scholarships',
            body=es_query,
            from_=skip,
            size=limit,
            sort=[{"deadline": {"order": "asc"}}]
        )
        
        return {
            "items": [hit["_source"] for hit in es_result["hits"]["hits"]],
            "total": es_result["hits"]["total"]["value"]
        }
    
    def get_scholarship_by_id(self, scholarship_id):
        try:
            scholarship = self.collection.find_one({"_id": ObjectId(scholarship_id)})
            if scholarship:
                scholarship["_id"] = str(scholarship["_id"])
            return scholarship
        except:
            return None
    
    def update_scholarship(self, scholarship_id, data):
        try:
            data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {"_id": ObjectId(scholarship_id)},
                {"$set": data}
            )
            
            if result.modified_count:
                # Update Elasticsearch
                self.es.update(index='scholarships', id=scholarship_id, body={"doc": data})
                return self.get_scholarship_by_id(scholarship_id)
            return None
        except:
            return None
    
    def delete_scholarship(self, scholarship_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(scholarship_id)})
            if result.deleted_count:
                # Delete from Elasticsearch
                self.es.delete(index='scholarships', id=scholarship_id)
                return True
            return False
        except:
            return False
