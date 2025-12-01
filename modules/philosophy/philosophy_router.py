from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any
import os
import uuid
from fastapi import Request, Depends
from modules.LLaMa.LLaMAManager import LLaMAManager

router = APIRouter()

def get_llama_manager(request: Request) -> LLaMAManager:
    return request.app.state.llama_manager
@router.post("/process-text/{file_uuid}")
async def process_text_file(file_uuid: str, llama_manager: LLaMAManager = Depends(get_llama_manager)) -> Dict[str, Any]:

    try:
        uuid.UUID(file_uuid)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid UUID format"
        )

    file_path = f"files_txt_view/{file_uuid}.txt"

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Text file with UUID {file_uuid} not found"
        )

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read file: {str(e)}"
        )

    if not text_content.strip():
        raise HTTPException(
            status_code=400,
            detail="Text file is empty"
        )

    system_prompt = """Ты - эксперт по философии и анализу текстов.
    Проанализируй предоставленный текст и дай глубокий философский анализ.
    Обрати внимание на:
    - Основные философские концепции и идеи
    - Этические аспекты
    - Социальные и культурные последствия
    - Связь с современными проблемами человечества
    - Возможные интерпретации и выводы

    Дай структурированный, глубокий анализ на русском языке."""

    prompt = f"Проанализируй следующий текст с философской точки зрения:\n\n{text_content[:8000]}"  # Ограничиваем длину для модели 4000 символов

    try:
        analysis_result = llama_manager.chat(prompt, system_prompt=system_prompt)

        return {
            "file_uuid": file_uuid,
            "analysis": analysis_result,
            "text_length": len(text_content),
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process text with LLaMA: {str(e)}"
        )

