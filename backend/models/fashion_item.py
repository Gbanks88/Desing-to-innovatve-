from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class FashionItemBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    image_url: str = Field(alias="imageUrl")

class FashionItemCreate(FashionItemBase):
    pass

class FashionItemUpdate(FashionItemBase):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")

class FashionItem(FashionItemBase):
    id: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
