from fastapi import APIRouter, Depends, HTTPException
from app.services.genmini_service import GeminiService, get_gemini_service
from typing import List
import json


router = APIRouter(tags=["Genmini"])


@router.get("/correct")
async def correct_text(text, genmini: GeminiService = Depends(get_gemini_service)):
    try:
        corrected = await genmini.correct_text(text)
        return corrected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error correcting text: {str(e)}")


@router.post("/vocabulary")
async def get_vocabulary(
    topics: List[str], genmini: GeminiService = Depends(get_gemini_service)
):
    """
    Get vocabulary lists for given topics at three levels: basic, everyday, and formal.

    Args:
        topics: List of topic strings to generate vocabulary for

    Returns:
        JSON response with vocabulary organized by topics and levels
    """
    try:
        vocabulary_response = await genmini.get_vocabulary_by_topics(topics)

        # Try to parse the response as JSON to ensure it's valid
        try:
            vocabulary_data = json.loads(vocabulary_response)
            return vocabulary_data
        except json.JSONDecodeError:
            # If it's not valid JSON, return it as a string
            return {"data": vocabulary_response}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating vocabulary: {str(e)}"
        )
