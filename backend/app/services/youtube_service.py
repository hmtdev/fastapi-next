from youtube_transcript_api import YouTubeTranscriptApi
from app.core.logger import logger
import json


class YouTubeService:
    def __init__(self):
        logger.info("YouTube Transcript Service initialized")
        self.api_instance = YouTubeTranscriptApi()

    async def get_video_transcript(self, video_id: str, language: str = None) -> dict:
        try:
            if "&" in video_id:
                video_id = video_id.split("&")[0]

            try:
                if language:
                    transcript_data = self.api_instance.fetch(
                        video_id, languages=[language]
                    )
                else:
                    transcript_data = self.api_instance.fetch(video_id)
                processed_transcript = []
                total_words = 0
                total_duration = 0
                for segment in transcript_data:
                    text = segment.text
                    word_count = len(text.split())
                    duration = segment.duration

                    total_words += word_count
                    total_duration += duration

                    processed_segment = {
                        "start": segment.start,
                        "duration": duration,
                        "text": text,
                        "word_count": word_count,
                    }
                    processed_transcript.append(processed_segment)

                logger.info(f"Successfully retrieved transcript for video {video_id}")
                return {
                    "transcript": processed_transcript,
                    "total_words": total_words,
                    "total_duration": total_duration,
                    "total_segments": len(processed_transcript),
                }
            except Exception as e:
                logger.error(f"Error getting transcript: {str(e)}")
                raise ValueError(f"Failed to get transcript: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting transcript for video ID {video_id}: {str(e)}")
            raise RuntimeError(f"Failed to get transcript: {str(e)}")

    async def get_available_languages(self, video_id: str) -> list:
        try:
            if "&" in video_id:
                video_id = video_id.split("&")[0]

            common_languages = [
                "en",
                "es",
                "fr",
                "de",
                "it",
                "ja",
                "ko",
                "pt",
                "ru",
                "zh-Hans",
                "zh-Hant",
                "ar",
                "hi",
                "vi",
            ]

            available_languages = []

            try:
                default_transcript = YouTubeTranscriptApi.get_transcript(video_id)
                if default_transcript:
                    available_languages.append(
                        {
                            "code": "default",
                            "name": "Default (Auto-detected)",
                            "is_available": True,
                        }
                    )
            except:
                pass

            for lang in common_languages:
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(
                        video_id, languages=[lang]
                    )
                    if transcript:
                        available_languages.append(
                            {
                                "code": lang,
                                "name": self._get_language_name(lang),
                                "is_available": True,
                            }
                        )
                except:
                    pass

            logger.info(
                f"Found {len(available_languages)} available languages for video ID: {video_id}"
            )
            return available_languages
        except Exception as e:
            logger.error(
                f"Error getting available languages for video ID {video_id}: {str(e)}"
            )
            return []

    def _get_language_name(self, language_code: str) -> str:
        language_map = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "ja": "Japanese",
            "ko": "Korean",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh-Hans": "Chinese (Simplified)",
            "zh-Hant": "Chinese (Traditional)",
            "ar": "Arabic",
            "hi": "Hindi",
            "vi": "Vietnamese",
        }
        return language_map.get(language_code, language_code)

    async def extract_video_id(self, url: str) -> str:
        try:
            import re

            patterns = [
                r"(?:youtube\.com\/watch\?v=)([^&\s]{11})",
                r"(?:youtu\.be\/)([^?\s]{11})",
                r"(?:youtube\.com\/embed\/)([^?\s]{11})",
                r"(?:youtube\.com\/shorts\/)([^?\s]{11})",
                r"(?:youtube\.com\/.+?\/?)(?:.+\/)?([^&\s]{11})",
            ]
            url = url.strip()
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            if re.match(r"^[A-Za-z0-9_-]{11}$", url):
                return url
            raise ValueError(f"Could not extract video ID from URL: {url}")
        except Exception as e:
            logger.error(f"Error extracting video ID from '{url}': {str(e)}")
            raise ValueError(f"Failed to extract video ID: {str(e)}")


def get_youtube_service() -> YouTubeService:
    return YouTubeService()
