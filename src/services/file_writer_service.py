"""
Async service for writing LaTeX output files.
Handles file system operations with proper error handling.
"""
import asyncio
import logging
import os
from pathlib import Path
from typing import Tuple

from src.config import settings
from src.models.context import JobMetadata
from src.utils.helpers import sanitize_filename

logger = logging.getLogger(__name__)


class FileWriterService:
    """Async service for writing resume and cover letter files."""
    
    def __init__(self):
        """Initialize file writer and ensure output directory exists."""
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {self.output_dir}")
    
    async def write_latex_files(
        self,
        resume_content: str,
        cover_letter_content: str,
        metadata: JobMetadata
    ) -> Tuple[str, str]:
        """
        Write resume and cover letter LaTeX files.
        
        Args:
            resume_content: LaTeX content for resume
            cover_letter_content: LaTeX content for cover letter
            metadata: Job metadata for filename generation
            
        Returns:
            Tuple of (resume_path, cover_letter_path)
            
        Raises:
            IOError: If file writing fails
        """
        # Generate filenames
        company_name = sanitize_filename(metadata.company)
        resume_filename = f"Andrew_Obwocha_Resume_{company_name}.tex"
        cover_letter_filename = f"Andrew_Obwocha_CoverLetter_{company_name}.tex"
        
        resume_path = self.output_dir / resume_filename
        cover_letter_path = self.output_dir / cover_letter_filename
        
        try:
            # Write files in executor to avoid blocking
            loop = asyncio.get_event_loop()
            
            await loop.run_in_executor(
                None,
                self._write_file,
                resume_path,
                resume_content
            )
            
            await loop.run_in_executor(
                None,
                self._write_file,
                cover_letter_path,
                cover_letter_content
            )
            
            logger.debug(f"[DEBUG] Files written: {resume_path} and {cover_letter_path}")
            
            return (str(resume_path), str(cover_letter_path))
            
        except Exception as e:
            logger.error(f"Failed to write files: {e}")
            raise IOError(f"File write failed: {e}")
    
    @staticmethod
    def _write_file(path: Path, content: str) -> None:
        """Synchronous helper to write file content."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
