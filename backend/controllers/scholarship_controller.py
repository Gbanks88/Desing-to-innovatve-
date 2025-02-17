from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.scholarship import ScholarshipCreate, ScholarshipUpdate, ScholarshipResponse
from services.scholarship_service import ScholarshipService

router = APIRouter()
scholarship_service = ScholarshipService()

@router.post("/", response_model=ScholarshipResponse)
async def create_scholarship(scholarship: ScholarshipCreate):
    """Create a new scholarship"""
    return await scholarship_service.create_scholarship(scholarship)

@router.get("/", response_model=List[ScholarshipResponse])
async def get_scholarships():
    """Get all scholarships"""
    return await scholarship_service.get_scholarships()

@router.get("/{scholarship_id}", response_model=ScholarshipResponse)
async def get_scholarship(scholarship_id: str):
    """Get a scholarship by ID"""
    scholarship = await scholarship_service.get_scholarship(scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship

@router.put("/{scholarship_id}", response_model=ScholarshipResponse)
async def update_scholarship(scholarship_id: str, scholarship: ScholarshipUpdate):
    """Update a scholarship"""
    updated_scholarship = await scholarship_service.update_scholarship(scholarship_id, scholarship)
    if not updated_scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return updated_scholarship

@router.delete("/{scholarship_id}")
async def delete_scholarship(scholarship_id: str):
    """Delete a scholarship"""
    success = await scholarship_service.delete_scholarship(scholarship_id)
    if not success:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return {"message": "Scholarship deleted successfully"}
