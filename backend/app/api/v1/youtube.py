from fastapi import APIRouter, Depends, HTTPException
from app.services.youtube_service import YouTubeService, get_youtube_service
from typing import Optional, List
from app.core.logger import logger
from urllib.parse import urlparse, parse_qs

router = APIRouter(tags=["YouTube"])


@router.get("/transcript")
async def get_transcript(
    video_id: Optional[str] = None,
    url: Optional[str] = None,
    language: Optional[str] = None,
    youtube: YouTubeService = Depends(get_youtube_service),
):
    """
    Get transcript for a YouTube video

    Args:
        video_id: YouTube video ID
        url: Alternative - full YouTube URL to extract video ID from
        language: Optional language code (e.g., 'en', 'vi')

    Returns:
        JSON response with transcript data
    """
    try:
        # Validate inputs - need either video_id or url
        if not video_id and not url:
            raise ValueError("Either video_id or url parameter is required")

        # Extract video ID from URL if provided
        if url and not video_id:

            def extract_video_id(youtube_url):
                parsed_url = urlparse(youtube_url)

                if parsed_url.netloc == "youtu.be":
                    return parsed_url.path[1:]

                if parsed_url.netloc in ("www.youtube.com", "youtube.com"):
                    if parsed_url.path == "/watch":
                        query = parse_qs(parsed_url.query)
                        if "v" in query:
                            return query["v"][0]
                    elif parsed_url.path.startswith("/embed/"):
                        return parsed_url.path.split("/")[2]
                    elif parsed_url.path.startswith("/v/"):
                        return parsed_url.path.split("/")[2]
                    elif parsed_url.path.startswith("/shorts/"):
                        return parsed_url.path.split("/")[2]

                # If no match found
                raise ValueError(f"Could not extract video ID from URL: {youtube_url}")

            video_id = extract_video_id(url)
            logger.info(f"Extracted video ID: {video_id} from URL: {url}")

        # Clean video ID (remove any playlist parameters)
        if "&" in video_id:
            original_id = video_id
            video_id = video_id.split("&")[0]
            logger.info(f"Cleaned video ID from {original_id} to {video_id}")

        logger.info(
            f"Requesting transcript for video ID: {video_id}, language: {language}"
        )

        transcript_data = await youtube.get_video_transcript(video_id, language)

        # Return with additional metadata for better context
        response = {
            "video_id": video_id,
            "language": language or "default",
            "watch_url": f"https://www.youtube.com/watch?v={video_id}",
            **transcript_data,  # Include all transcript data
        }

        return response

    except ValueError as e:
        logger.error(f"Transcript not available: {str(e)}")
        raise HTTPException(
            status_code=404, detail={"error": str(e), "video_id": video_id}
        )
    except Exception as e:
        logger.error(f"Error getting transcript: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving transcript: {str(e)}"
        )


@router.get("/languages/{video_id}")
async def get_available_languages(
    video_id: str, youtube: YouTubeService = Depends(get_youtube_service)
):
    """
    Get available transcript languages for a YouTube video

    Args:
        video_id: YouTube video ID

    Returns:
        List of available language codes and names
    """
    try:
        logger.info(f"Requesting available languages for video ID: {video_id}")
        languages = await youtube.get_available_languages(video_id)
        return {"video_id": video_id, "languages": languages}
    except Exception as e:
        logger.error(f"Error getting available languages: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving available languages: {str(e)}"
        )


@router.get("/translate/{video_id}")
async def translate_transcript(
    video_id: str,
    target_language: str,
    youtube: YouTubeService = Depends(get_youtube_service),
):
    """
    Get a transcript translated to a specific language

    Args:
        video_id: YouTube video ID
        target_language: Target language code (e.g., 'en', 'vi')

    Returns:
        JSON response with translated transcript data
    """
    try:
        logger.info(
            f"Requesting transcript translation for video ID: {video_id} to {target_language}"
        )
        translated_data = await youtube.translate_transcript(video_id, target_language)
        return translated_data
    except ValueError as e:
        logger.error(f"Transcript not available: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error translating transcript: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error translating transcript: {str(e)}"
        )


@router.get("/extract-id")
async def extract_video_id(url: str):
    """
    Extract YouTube video ID from various URL formats

    Args:
        url: YouTube URL (can be standard, shortened, or embed format)

    Returns:
        Extracted video ID
    """
    try:

        def extract_video_id(youtube_url):
            """Extract the video ID from a YouTube URL."""
            parsed_url = urlparse(youtube_url)

            if parsed_url.netloc == "youtu.be":
                return parsed_url.path[1:]

            if parsed_url.netloc in ("www.youtube.com", "youtube.com"):
                if parsed_url.path == "/watch":
                    query = parse_qs(parsed_url.query)
                    if "v" in query:
                        return query["v"][0]
                elif parsed_url.path.startswith("/embed/"):
                    return parsed_url.path.split("/")[2]
                elif parsed_url.path.startswith("/v/"):
                    return parsed_url.path.split("/")[2]
                elif parsed_url.path.startswith("/shorts/"):
                    return parsed_url.path.split("/")[2]

            # If the input is just the 11-character video ID
            if len(youtube_url) == 11 and all(
                c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
                for c in youtube_url
            ):
                return youtube_url

            # If no match found
            raise ValueError(f"Could not extract video ID from URL: {youtube_url}")

        video_id = extract_video_id(url)

        return {
            "url": url,
            "video_id": video_id,
            "watch_url": f"https://www.youtube.com/watch?v={video_id}",
        }
    except ValueError as e:
        logger.error(f"Error extracting video ID: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error extracting video ID: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")
