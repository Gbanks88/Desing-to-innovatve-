from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

class BaseService(ABC):
    def __init__(self, db):
        self.db = db
        self.collection = None

    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate input data"""
        pass

    def create_timestamp(self) -> Dict[str, datetime]:
        """Create timestamp for document tracking"""
        now = datetime.utcnow()
        return {
            'created_at': now,
            'updated_at': now
        }

    def update_timestamp(self) -> Dict[str, datetime]:
        """Update timestamp for document tracking"""
        return {
            'updated_at': datetime.utcnow()
        }

    def add_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata to document"""
        return {
            **data,
            **self.create_timestamp(),
            'is_active': True
        }
