import google.generativeai as genai
from app.core.config import get_settings
from app.core.logger import logger

settings = get_settings()


class GeminiService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not GeminiService._initialized:
            self.model = None
            GeminiService._initialized = True

    def initialize(self):
        if not settings.GENMINI_API_KEY:
            raise ValueError("GENMINI_API_KEY is not set in environment variables")
        genai.configure(api_key=settings.GENMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        logger.info("Gemini model initialized successfully")

    async def correct_text(self, text: str) -> dict:
        """ """
        if not self.model:
            raise RuntimeError("Gemini model not initialized")

        prompt = f"""Correct the following English text for grammar, spelling, and stylistic mistakes.
            
        Format your response with TWO clearly separated sections delimited by special markers:
        
        [HTML_START]
        <div class="corrected-text">
            <p>Your corrected text here, with corrected parts highlighted using <span style="color:red">corrected text</span> for each error fixed</p>
        </div>
        [HTML_END]
        
        [MARKDOWN_START]
        ## Errors Fixed
        - **Original**: "[Original error]"
        **Corrected**: "[Corrected version]"
        **Explanation**: [Brief explanation of why the correction was made]
        
        ## Suggestions for Improvement
        - **Original**: "[Original sentence/phrase]"
        **Suggestion**: "[Suggested alternative]"
        **Reason**: [Reason for suggestion]
        [MARKDOWN_END]
        
        Input Text: "{text}"
        
        IMPORTANT INSTRUCTIONS:
        1. First section (HTML): Provide ONLY the corrected text with corrections highlighted in red spans.
        2. Second section (Markdown): Provide detailed error analysis and suggestions using proper Markdown formatting.
        3. Use the exact markers [HTML_START], [HTML_END], [MARKDOWN_START], and [MARKDOWN_END] to delimit the sections.
        4. Do not include any text outside these sections.
            """

        response = await self.model.generate_content_async(prompt)
        response_text = response.text.strip()

        # Parse the response to extract HTML and Markdown parts
        html_part = ""
        markdown_part = ""

        # Extract HTML part
        if "[HTML_START]" in response_text and "[HTML_END]" in response_text:
            html_start = response_text.find("[HTML_START]") + len("[HTML_START]")
            html_end = response_text.find("[HTML_END]")
            html_part = response_text[html_start:html_end].strip()

        # Extract Markdown part
        if "[MARKDOWN_START]" in response_text and "[MARKDOWN_END]" in response_text:
            md_start = response_text.find("[MARKDOWN_START]") + len("[MARKDOWN_START]")
            md_end = response_text.find("[MARKDOWN_END]")
            markdown_part = response_text[md_start:md_end].strip()

        return {"html": html_part, "markdown": markdown_part}

    async def get_vocabulary_by_topics(self, topics: list[str]) -> dict:
        """
        Generate vocabulary lists for given topics at three levels:
        basic, everyday conversation, and formal/academic.

        Args:
            topics: A list of topic strings

        Returns:
            Dictionary containing structured vocabulary data
        """
        if not self.model:
            raise RuntimeError("Gemini model not initialized")

        topics_text = ", ".join(topics)

        prompt = f"""Generate vocabulary lists for the following topics: {topics_text}.
        
        For each topic, provide vocabulary at THREE distinct levels:
        1. Basic vocabulary (for beginners)
        2. Everyday conversation vocabulary (intermediate)
        3. Formal/academic vocabulary (advanced)
        
        Format your response using the following JSON structure:
        
        ```json
        {{
          "topics": [
            {{
              "topic": "Topic name",
              "vocabulary": {{
                "basic": [
                  {{ "word": "word1", "meaning": "meaning in Vietnamese", "example": "example sentence" }},
                  {{ "word": "word2", "meaning": "meaning in Vietnamese", "example": "example sentence" }}
                ],
                "everyday": [
                  {{ "word": "word1", "meaning": "meaning in Vietnamese", "example": "example sentence" }},
                  {{ "word": "word2", "meaning": "meaning in Vietnamese", "example": "example sentence" }}
                ],
                "formal": [
                  {{ "word": "word1", "meaning": "meaning in Vietnamese", "example": "example sentence" }},
                  {{ "word": "word2", "meaning": "meaning in Vietnamese", "example": "example sentence" }}
                ]
              }}
            }}
          ]
        }}
        ```
        
        IMPORTANT INSTRUCTIONS:
        1. Provide 10 words for each level
        2. Give accurate Vietnamese translations for the meanings
        3. Include a simple example sentence for each word
        4. Ensure the words are truly representative of each level (basic, everyday, formal)
        5. Return ONLY the JSON object with no additional text
        """

        response = await self.model.generate_content_async(prompt)
        response_text = response.text.strip()

        # Extract JSON content from response if needed
        if "```json" in response_text and "```" in response_text:
            json_start = response_text.find("```json") + len("```json")
            json_end = response_text.rfind("```")
            response_text = response_text[json_start:json_end].strip()

        # The response should be valid JSON at this point
        return response_text


gemini_service = GeminiService()


def get_gemini_service() -> GeminiService:
    if gemini_service.model is None:
        raise RuntimeError("Gemini service was not properly initialized")
    return gemini_service
