from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import os

from modules.SkillMatcher.SkillMatcherManager import SkillMatcherManager

router = APIRouter()
skill_matcher = SkillMatcherManager()

@router.post("/process-resume")
async def process_resume_pdf(file: UploadFile = File(...)) -> Dict[str, Any]:

    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Validate file size (max 10MB)
    file_content = await file.read()
    max_size = 10 * 1024 * 1024  # 10MB
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum limit of 10MB"
        )

    # Process the resume PDF
    result = skill_matcher.process_resume_pdf(file_content, file.filename)

    if result is None or not result.get('success', False):
        error_msg = result.get('error', 'Failed to process resume PDF') if result else 'Failed to process resume PDF'
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

    return result

@router.get("/resume/{file_uuid}")
async def get_resume_text(file_uuid: str) -> Dict[str, Any]:

    text_content = skill_matcher.get_resume_text(file_uuid)

    if text_content is None:
        raise HTTPException(
            status_code=404,
            detail=f"Resume with UUID '{file_uuid}' not found"
        )

    return {
        "uuid": file_uuid,
        "text_content": text_content,
        "text_length": len(text_content)
    }

@router.get("/resumes")
async def list_processed_resumes() -> Dict[str, Any]:

    resumes = skill_matcher.list_processed_resumes()

    return {
        "total_count": len(resumes),
        "resumes": resumes
    }

@router.get("/resume/{file_uuid}/exists")
async def check_resume_exists(file_uuid: str) -> Dict[str, Any]:

    text_content = skill_matcher.get_resume_text(file_uuid)
    exists = text_content is not None

    return {
        "uuid": file_uuid,
        "exists": exists,
        "text_length": len(text_content) if exists else 0
    }
