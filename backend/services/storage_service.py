import os
import swiftclient
from fastapi import HTTPException
from typing import Optional
import mimetypes

class StorageService:
    def __init__(self):
        self.conn = swiftclient.Connection(
            authurl='https://auth.cloud.ovh.net/v3',
            user=os.getenv('OVH_USERNAME'),
            key=os.getenv('OVH_PASSWORD'),
            tenant_name=os.getenv('OVH_TENANT_NAME'),
            auth_version='3'
        )
        self.container = 'fashion-platform'
        self._ensure_container_exists()

    def _ensure_container_exists(self):
        """Ensure the container exists, create if it doesn't"""
        try:
            self.conn.head_container(self.container)
        except swiftclient.ClientException:
            self.conn.put_container(self.container)

    async def upload_file(self, file_data: bytes, filename: str) -> str:
        """Upload a file to OVH Object Storage"""
        try:
            # Determine content type
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            
            # Upload file
            self.conn.put_object(
                self.container,
                filename,
                contents=file_data,
                content_type=content_type
            )

            # Generate public URL
            region = os.getenv('OVH_REGION', 'gra')
            tenant_id = os.getenv('OVH_TENANT_ID')
            url = f"https://storage.{region}.cloud.ovh.net/v1/AUTH_{tenant_id}/{self.container}/{filename}"
            
            return url

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    async def delete_file(self, filename: str) -> bool:
        """Delete a file from OVH Object Storage"""
        try:
            self.conn.delete_object(self.container, filename)
            return True
        except swiftclient.ClientException:
            return False

    async def get_file_url(self, filename: str) -> Optional[str]:
        """Get the public URL for a file"""
        try:
            self.conn.head_object(self.container, filename)
            region = os.getenv('OVH_REGION', 'gra')
            tenant_id = os.getenv('OVH_TENANT_ID')
            return f"https://storage.{region}.cloud.ovh.net/v1/AUTH_{tenant_id}/{self.container}/{filename}"
        except swiftclient.ClientException:
            return None

    async def list_files(self, prefix: Optional[str] = None) -> list:
        """List files in the storage with optional prefix"""
        try:
            _, objects = self.conn.get_container(
                self.container,
                prefix=prefix
            )
            return [
                {
                    'name': obj['name'],
                    'size': obj['bytes'],
                    'content_type': obj['content_type'],
                    'last_modified': obj['last_modified']
                }
                for obj in objects
            ]
        except swiftclient.ClientException as e:
            raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

    def __del__(self):
        """Clean up the connection when the service is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()
