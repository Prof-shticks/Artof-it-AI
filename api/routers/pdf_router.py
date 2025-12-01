from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import os

from modules.PDFConverter.PDFConverter import PDFConverter

router = APIRouter()
pdf_converter = PDFConverter()

@router.post("/convert-pdf")
async def convert_pdf_to_text(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Convert uploaded PDF file to text

    Args:
        file (UploadFile): PDF file to convert

    Returns:
        Dict[str, Any]: Response containing the extracted text and metadata
    """
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

    # Convert PDF to text
    conversion_result = pdf_converter.convert_pdf_to_text(file_content)

    if conversion_result is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract text from PDF"
        )

    text_content, file_path = conversion_result

    # Get PDF metadata
    pdf_info = pdf_converter.get_pdf_info(file_content)

    return {
        "filename": file.filename,
        "text_content": text_content,
        "file_path": file_path,
        "metadata": pdf_info,
        "text_length": len(text_content)
    }

@router.post("/pdf-info")
async def get_pdf_info(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Get information about uploaded PDF file

    Args:
        file (UploadFile): PDF file to analyze

    Returns:
        Dict[str, Any]: PDF metadata
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read file content
    file_content = await file.read()

    # Get PDF metadata
    pdf_info = pdf_converter.get_pdf_info(file_content)

    if pdf_info is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to read PDF metadata"
        )

    return {
        "filename": file.filename,
        "metadata": pdf_info
    }
