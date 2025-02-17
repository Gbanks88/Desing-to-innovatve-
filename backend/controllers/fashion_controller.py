from typing import List
from fastapi import APIRouter, HTTPException, Depends
from services.fashion_service import FashionService
from models.fashion_item import FashionItem, FashionItemCreate, FashionItemUpdate
from dependencies import get_fashion_service

router = APIRouter()

@router.get("/", response_model=List[FashionItem])
async def get_fashion_items(
    service: FashionService = Depends(get_fashion_service)
):
    return await service.get_all_items()

@router.get("/{item_id}", response_model=FashionItem)
async def get_fashion_item(
    item_id: str,
    service: FashionService = Depends(get_fashion_service)
):
    item = await service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Fashion item not found")
    return item

@router.post("/", response_model=FashionItem)
async def create_fashion_item(
    item: FashionItemCreate,
    service: FashionService = Depends(get_fashion_service)
):
    return await service.create_item(item)

@router.put("/{item_id}", response_model=FashionItem)
async def update_fashion_item(
    item_id: str,
    item: FashionItemUpdate,
    service: FashionService = Depends(get_fashion_service)
):
    updated_item = await service.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Fashion item not found")
    return updated_item

@router.delete("/{item_id}")
async def delete_fashion_item(
    item_id: str,
    service: FashionService = Depends(get_fashion_service)
):
    success = await service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fashion item not found")
    return {"status": "success", "message": "Item deleted successfully"}
