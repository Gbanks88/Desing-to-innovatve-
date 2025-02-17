from flask import current_app
from google.cloud import storage
from datetime import datetime
import magic
import os
from bson import ObjectId

class VideoService:
    def __init__(self):
        self._db = None
        self._es = None
        self._storage_client = None
        self._bucket = None
    
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
    def storage_client(self):
        if self._storage_client is None:
            self._storage_client = storage.Client.from_service_account_json(
                current_app.config['GCP_CREDENTIALS_FILE']
            )
        return self._storage_client
    
    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = self.storage_client.bucket(current_app.config['GCP_BUCKET_NAME'])
        return self._bucket
    
    def upload_video(self, video_file, data):
        # Verify file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(video_file.read())
        video_file.seek(0)
        
        if not file_type.startswith('video/'):
            raise ValueError("Invalid file type. Only video files are allowed.")
        
        # Generate unique filename
        filename = f"videos/{datetime.utcnow().timestamp()}_{video_file.filename}"
        
        # Create a blob and upload the file
        blob = self.bucket.blob(filename)
        blob.upload_from_file(
            video_file,
            content_type=file_type
        )
        
        # Make the blob publicly accessible
        blob.make_public()
        
        # Create video document
        video_data = {
            **data,
            'filename': filename,
            'file_type': file_type,
            'url': blob.public_url,
            'created_at': datetime.utcnow()
        }
        
        result = self.db.videos.insert_one(video_data)
        video_data['_id'] = str(result.inserted_id)
        
        # Index in Elasticsearch
        self.es.index(index='videos', id=str(result.inserted_id), body=video_data)
        return video_data
    
    def get_videos(self, page, limit, category=None, search_query=None):
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
            
            es_result = self.es.search(index='videos', body=es_query, from_=skip, size=limit)
            return {
                "items": [hit["_source"] for hit in es_result["hits"]["hits"]],
                "total": es_result["hits"]["total"]["value"]
            }
        
        # Regular MongoDB query
        query = {}
        if category:
            query["category"] = category
        
        total = self.db.videos.count_documents(query)
        cursor = self.db.videos.find(query).skip(skip).limit(limit)
        
        return {
            "items": [{**item, "_id": str(item["_id"])} for item in cursor],
            "total": total
        }
    
    def get_video_by_id(self, video_id):
        try:
            video = self.db.videos.find_one({"_id": ObjectId(video_id)})
            if video:
                video["_id"] = str(video["_id"])
            return video
        except:
            return None
    
    def update_video(self, video_id, data):
        try:
            data['updated_at'] = datetime.utcnow()
            result = self.db.videos.update_one(
                {"_id": ObjectId(video_id)},
                {"$set": data}
            )
            
            if result.modified_count:
                # Update Elasticsearch
                self.es.update(index='videos', id=video_id, body={"doc": data})
                return self.get_video_by_id(video_id)
            return None
        except:
            return None
    
    def delete_video(self, video_id):
        try:
            video = self.get_video_by_id(video_id)
            if not video:
                return False
            
            # Delete from Google Cloud Storage
            blob = self.bucket.blob(video['filename'])
            blob.delete()
            
            # Delete from MongoDB
            result = self.db.videos.delete_one({"_id": ObjectId(video_id)})
            if result.deleted_count:
                # Delete from Elasticsearch
                self.es.delete(index='videos', id=video_id)
                return True
            return False
        except:
            return None
