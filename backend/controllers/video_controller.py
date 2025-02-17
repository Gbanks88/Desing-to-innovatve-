from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.video import VideoCreate, VideoUpdate, VideoResponse
from services.video_service import VideoService

router = APIRouter()
video_service = VideoService()

@router.post("/", response_model=VideoResponse)
async def create_video(video: VideoCreate):
    """Create a new video"""
    return await video_service.create_video(video)

@router.get("/", response_model=List[VideoResponse])
async def get_videos():
    """Get all videos"""
    return await video_service.get_videos()

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    """Get a video by ID"""
    video = await video_service.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(video_id: str, video: VideoUpdate):
    """Update a video"""
    updated_video = await video_service.update_video(video_id, video)
    if not updated_video:
        raise HTTPException(status_code=404, detail="Video not found")
    return updated_video

@router.delete("/{video_id}")
async def delete_video(video_id: str):
    """Delete a video"""
    success = await video_service.delete_video(video_id)
    if not success:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"message": "Video deleted successfully"}
