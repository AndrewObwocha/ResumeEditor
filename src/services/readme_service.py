"""
Async service for fetching README files from GitHub repositories.
Uses concurrent fetching for improved performance.
"""
import asyncio
import logging
from typing import Dict, Optional
import aiohttp

from src.config import settings

logger = logging.getLogger(__name__)


class ReadmeService:
    """Async service for fetching README files from GitHub."""
    
    BRANCHES = ["main", "master"]
    README_TIMEOUT = 10  # seconds
    MAX_README_LENGTH = 8000  # characters to include
    
    async def fetch_readme(self, title: str, repo_url: str) -> Optional[tuple[str, str]]:
        """
        Fetch a single README file from a GitHub repository.
        
        Args:
            title: Project title for the README
            repo_url: GitHub repository URL
            
        Returns:
            Tuple of (title, content) if successful, None if failed
        """
        path = repo_url.replace("https://github.com/", "").strip("/")
        
        for branch in self.BRANCHES:
            try:
                raw_url = f"https://raw.githubusercontent.com/{path}/{branch}/README.md"
                timeout = aiohttp.ClientTimeout(total=self.README_TIMEOUT)
                
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(raw_url) as response:
                        if response.status == 200:
                            content = await response.text()
                            # Truncate to reasonable length
                            truncated_content = content[:self.MAX_README_LENGTH]
                            logger.info(f"[LOADED] {title} ({len(truncated_content)} chars)")
                            return (title, truncated_content)
                            
            except asyncio.TimeoutError:
                logger.debug(f"Timeout fetching {title} from branch {branch}")
                continue
            except Exception as e:
                logger.debug(f"Error fetching {title} from branch {branch}: {e}")
                continue
        
        logger.warning(f"[FAILED] Unable to load: {title}")
        return None
    
    async def fetch_all_readmes(self) -> Dict[str, str]:
        """
        Fetch all README files from configured repositories concurrently.
        
        Returns:
            Dictionary mapping project titles to README content
        """
        logger.info("Fetching GitHub READMEs in parallel...")
        
        # Create tasks for all repositories
        tasks = [
            self.fetch_readme(title, url)
            for title, url in settings.PROJECT_REPO_MAP.items()
        ]
        
        # Fetch all concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Build dictionary from successful results
        readmes = {}
        for result in results:
            if isinstance(result, tuple):
                title, content = result
                readmes[title] = content
            elif isinstance(result, Exception):
                logger.warning(f"Exception during README fetch: {result}")
        
        logger.info(f"Successfully loaded {len(readmes)}/{len(settings.PROJECT_REPO_MAP)} READMEs")
        return readmes
