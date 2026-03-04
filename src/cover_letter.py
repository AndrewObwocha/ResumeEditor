"""
Cover letter generation module for creating personalized cover letters.
"""
import logging
from typing import Dict

from src.templates.templates import COVER_LETTER_LATEX
from src.prompts import COVER_LETTER_PROMPT
from src.services.gemini_service import GeminiService
from src.models.context import JobMetadata

logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    """Generates personalized cover letters using AI and project context."""
    
    def __init__(self, gemini_service: GeminiService):
        """
        Initialize the cover letter generator.
        
        Args:
            gemini_service: Service for AI content generation
        """
        self.gemini_service = gemini_service
    
    async def generate_cover_letter(self, context: Dict) -> str:
        """
        Generate a personalized cover letter based on job requirements.
        
        Args:
            context: Dictionary containing:
                - job_strategy: Application strategy text
                - job_description: Job description text
                - readmes: Dictionary of project README documentation
                - metadata: JobMetadata object
                
        Returns:
            Complete LaTeX cover letter content
        """
        logger.info("[PROGRESS] Generating cover letter")
        
        metadata: JobMetadata = context['metadata']
        
        # Build RAG context from READMEs
        rag_context = self._build_rag_context(context.get('readmes', {}))
        
        # Get job description excerpt (first 1000 chars)
        job_desc_excerpt = context['job_description'][:1000]
        
        # Format prompt
        prompt = COVER_LETTER_PROMPT.format(
            job_strategy=context['job_strategy'],
            company=metadata.company,
            role=metadata.role,
            address=metadata.address if metadata.address else "N/A",
            rag_context=rag_context,
            job_description_excerpt=job_desc_excerpt
        )
        
        # Generate cover letter body
        body_content = await self.gemini_service.generate_content(prompt)
        
        # Fill in template
        cover_letter = self._fill_template(
            body_content=body_content,
            metadata=metadata
        )
        
        logger.debug("[DEBUG] Cover letter generation complete")
        return cover_letter
    
    def _build_rag_context(self, readmes: Dict[str, str]) -> str:
        """
        Build project context from README files.
        
        Args:
            readmes: Dictionary of project titles to README content
            
        Returns:
            Formatted project context string
        """
        if not readmes:
            return "No project documentation available."
        
        context_parts = []
        for title, content in list(readmes.items())[:3]:  # Use top 3 projects
            # Truncate each README to 1000 chars
            truncated = content[:1000]
            context_parts.append(f"**{title}**\n{truncated}")
        
        return "\n\n".join(context_parts)
    
    def _fill_template(self, body_content: str, metadata: JobMetadata) -> str:
        """
        Fill cover letter template with generated content and metadata.
        
        Args:
            body_content: AI-generated cover letter body
            metadata: Job metadata for placeholders
            
        Returns:
            Complete LaTeX document
        """
        # Start with template
        cover_letter = COVER_LETTER_LATEX
        
        # Replace placeholders
        cover_letter = cover_letter.replace("%COMPANY_NAME%", metadata.company)
        cover_letter = cover_letter.replace("%COMPANY_ADDRESS%", metadata.address if metadata.address else "")
        cover_letter = cover_letter.replace("%JOB_TITLE%", metadata.role)
        cover_letter = cover_letter.replace("%BODY_CONTENT%", body_content)
        
        return cover_letter
