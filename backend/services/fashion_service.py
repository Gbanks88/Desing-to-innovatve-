from typing import List, Optional
from repositories.fashion_repository import FashionRepository
from models.fashion_item import FashionItem, FashionItemCreate, FashionItemUpdate

class FashionService:
    def __init__(self, repository: FashionRepository):
        self.repository = repository

    async def get_all_items(self) -> List[FashionItem]:
        return await self.repository.find_all()

    async def get_item_by_id(self, id: str) -> Optional[FashionItem]:
        return await self.repository.find_by_id(id)

    async def create_item(self, item: FashionItemCreate) -> FashionItem:
        return await self.repository.create(item)

    async def update_item(self, id: str, item: FashionItemUpdate) -> Optional[FashionItem]:
        return await self.repository.update(id, item)

    async def delete_item(self, id: str) -> bool:
        return await self.repository.delete(id)

    async def search_items(self, query: str) -> List[FashionItem]:
        # Add search logic here
        items = await self.repository.find_all()
        return [
            item for item in items
            if query.lower() in item.name.lower() or
               query.lower() in item.description.lower() or
               query.lower() in item.category.lower()
        ]
