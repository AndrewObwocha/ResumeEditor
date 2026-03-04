"""
Async service for fetching job descriptions from URLs or manual input.
Uses Jina Reader API for URL fetching.
"""
import asyncio
import logging
from typing import Optional
import aiohttp

from src.models.context import JobDescription

logger = logging.getLogger(__name__)


class JobFetcherService:
    """Async service for fetching job descriptions."""
    
    JINA_BASE_URL = "https://r.jina.ai/"
    MIN_CONTENT_LENGTH = 500
    REQUEST_TIMEOUT = 30  # seconds
    
    async def fetch_from_url(self, url: str) -> Optional[JobDescription]:
        """
        Fetch job description from URL using Jina Reader API.
        
        Args:
            url: The job posting URL
            
        Returns:
            JobDescription if successful, None if failed
        """
        logger.info(f"Fetching job description via Jina Reader from: {url}")
        
        try:
            jina_url = f"{self.JINA_BASE_URL}{url}"
            timeout = aiohttp.ClientTimeout(total=self.REQUEST_TIMEOUT)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(jina_url) as response:
                    content = await response.text()
                    
                    if response.status != 200:
                        logger.warning(f"Jina Reader returned status {response.status}")
                        return None
                    
                    if len(content) < self.MIN_CONTENT_LENGTH:
                        logger.warning(
                            f"Content too short ({len(content)} chars). "
                            "Link may be blocked."
                        )
                        return None
                    
                    logger.info(f"Successfully fetched {len(content)} characters")
                    return JobDescription.from_content(content, source="url")
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching from URL: {url}")
            return None
        except Exception as e:
            logger.error(f"Error fetching job description: {e}")
            return None
    
    @staticmethod
    async def fetch_from_input() -> JobDescription:
        """
        Capture multi-line manual input from terminal.
        Runs in executor to avoid blocking async event loop.
        
        Returns:
            JobDescription from manual input
        """
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, JobFetcherService._capture_input)
        return JobDescription.from_content(content, source="manual")
    
    @staticmethod
    def _capture_input() -> str:
        """
        Synchronous helper to capture multi-line input.
        Stops when user types 'DONE' on a new line.
        """
        print("\n")
        print("  PASTE JOB DESCRIPTION BELOW.")
        print("  When finished, type 'DONE' on a new line and hit Enter.")
        print("-" * 40 + "\n")
        
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip().upper() == "DONE":
                break
            lines.append(line)
        
        text = "\n".join(lines)
        logger.info(f"Captured {len(text)} characters from manual input")
        return text
