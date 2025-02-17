from typing import Dict, Any, Optional
from .ai_service import AIService
from .video_service import VideoService
from .scholarship_service import ScholarshipService
from database import Database

class ServiceManager:
    def __init__(self):
        self.db = Database()
        self._services: Dict[str, Any] = {}
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all backend services"""
        self._services = {
            'ai': AIService(self.db),
            'video': VideoService(),
            'scholarship': ScholarshipService()
        }

    def get_service(self, service_name: str) -> Optional[Any]:
        """Get a service instance by name"""
        return self._services.get(service_name)

    async def process_ai_request(self, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process AI-related requests"""
        ai_service = self.get_service('ai')
        if request_type == 'fashion_analysis':
            return await ai_service.analyze_fashion(data['image'])
        elif request_type == 'outfit_recommendations':
            return await ai_service.generate_outfit_recommendations(data['preferences'])
        raise ValueError(f"Unknown AI request type: {request_type}")

    async def process_video_request(self, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process video-related requests"""
        video_service = self.get_service('video')
        if request_type == 'upload':
            return await video_service.upload_video(data['video'], data['metadata'])
        elif request_type == 'process':
            return await video_service.process_video(data['video_id'], data['options'])
        raise ValueError(f"Unknown video request type: {request_type}")

    async def process_scholarship_request(self, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process scholarship-related requests"""
        scholarship_service = self.get_service('scholarship')
        if request_type == 'search':
            return await scholarship_service.search_scholarships(data['criteria'])
        elif request_type == 'apply':
            return await scholarship_service.apply_for_scholarship(data['scholarship_id'], data['application'])
        raise ValueError(f"Unknown scholarship request type: {request_type}")

    def cleanup(self):
        """Cleanup service resources"""
        self.db.close()
        # Add any other cleanup needed for services

# Create a global service manager instance
service_manager = ServiceManager()
