from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from models.fashion_item import FashionItem, FashionItemCreate, FashionItemUpdate

class FashionRepository:
    def __init__(self, database):
        self.db = database
        self.collection = database.fashion_items

    async def find_all(self) -> List[FashionItem]:
        cursor = self.collection.find()
        items = await cursor.to_list(length=None)
        return [self._map_to_model(item) for item in items]

    async def find_by_id(self, id: str) -> Optional[FashionItem]:
        item = await self.collection.find_one({"_id": ObjectId(id)})
        return self._map_to_model(item) if item else None

    async def create(self, item: FashionItemCreate) -> FashionItem:
        now = datetime.utcnow()
        doc = {
            **item.model_dump(by_alias=True),
            "created_at": now,
            "updated_at": now
        }
        result = await self.collection.insert_one(doc)
        return await self.find_by_id(str(result.inserted_id))

    async def update(self, id: str, item: FashionItemUpdate) -> Optional[FashionItem]:
        update_data = {
            "$set": {
                **item.model_dump(exclude_unset=True, by_alias=True),
                "updated_at": datetime.utcnow()
            }
        }
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, update_data
        )
        if result.modified_count:
            return await self.find_by_id(id)
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    def _map_to_model(self, doc: dict) -> FashionItem:
        return FashionItem(
            id=str(doc["_id"]),
            name=doc["name"],
            description=doc["description"],
            category=doc["category"],
            price=doc["price"],
            imageUrl=doc["image_url"],
            createdAt=doc["created_at"],
            updatedAt=doc["updated_at"]
        )
