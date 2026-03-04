"""
Async service for interacting with Google Gemini API.
Handles content generation with error handling and retry logic.
"""
import asyncio
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai

from src.config import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Async wrapper for Google Gemini API interactions."""
    
    def __init__(self):
        """Initialize the Gemini service with API key from settings."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
        logger.info(f"Initialized GeminiService with model: {settings.MODEL_NAME}")
    
    async def generate_content(
        self,
        prompt: str,
        generation_config: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> str:
        """
        Generate content using Gemini API with retry logic.
        
        Args:
            prompt: The prompt to send to the model
            generation_config: Optional generation configuration
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated text content
            
        Raises:
            Exception: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                # Run the blocking API call in executor to avoid blocking event loop
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.model.generate_content(
                        prompt,
                        generation_config=generation_config
                    )
                )
                return response.text
                
            except Exception as e:
                logger.warning(f"Gemini API attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"All {max_retries} attempts failed for Gemini API call")
                    raise
                # Exponential backoff
                await asyncio.sleep(2 ** attempt)
        
        raise Exception("Unexpected error in generate_content")
    
    async def generate_json(
        self,
        prompt: str,
        max_retries: int = 3
    ) -> str:
        """
        Generate JSON content using Gemini API.
        
        Args:
            prompt: The prompt to send to the model
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated JSON text
            
        Raises:
            Exception: If all retries fail
        """
        generation_config = {"response_mime_type": "application/json"}
        return await self.generate_content(
            prompt,
            generation_config=generation_config,
            max_retries=max_retries
        )
