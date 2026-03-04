"""
Resume optimization module for tailoring resume content to job requirements.
"""
import re
import logging
from typing import Dict, Tuple

from src.templates.templates import RESUME_LATEX
from src.prompts import RESUME_OPTIMIZER_PROMPT
from src.utils.constants import (
    LATEX_SECTION_PATTERN,
    THOUGHTS_START,
    THOUGHTS_END,
    LATEX_START,
    LATEX_END
)
from src.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class ResumeOptimizer:
    """Optimizes resume content using AI and project context."""
    
    def __init__(self, gemini_service: GeminiService):
        """
        Initialize the resume optimizer.
        
        Args:
            gemini_service: Service for AI content generation
        """
        self.gemini_service = gemini_service
        self.sections_modified = 0
    
    async def optimize_resume(self, context: Dict) -> Tuple[str, int]:
        """
        Optimize resume sections based on job strategy and project documentation.
        
        Args:
            context: Dictionary containing:
                - job_strategy: Application strategy text
                - readmes: Dictionary of project README documentation
                - job_description: Job description text
                
        Returns:
            Tuple of (optimized_latex_content, sections_count)
        """
        logger.info("[PROGRESS] Optimizing resume bullet points")
        self.sections_modified = 0
        self.context = context
        
        # Find all resume sections using regex
        async def rewrite_block_async(match):
            return await self._rewrite_block(match)
        
        # Process all sections
        final_latex = RESUME_LATEX
        sections = list(re.finditer(LATEX_SECTION_PATTERN, RESUME_LATEX, flags=re.DOTALL))
        
        for match in sections:
            original_chunk = match.group(0)
            optimized_chunk = await self._rewrite_block_wrapper(original_chunk)
            final_latex = final_latex.replace(original_chunk, optimized_chunk, 1)
            self.sections_modified += 1
        
        logger.debug(f"[DEBUG] Resume optimization: {self.sections_modified} sections processed")
        return final_latex, self.sections_modified
    
    async def _rewrite_block_wrapper(self, original_chunk: str) -> str:
        """
        Wrapper to handle block rewriting with proper context.
        
        Args:
            original_chunk: Original LaTeX section
            
        Returns:
            Optimized LaTeX section
        """
        try:
            rag_context = self._get_rag_context(original_chunk)
            
            prompt = RESUME_OPTIMIZER_PROMPT.format(
                job_strategy=self.context['job_strategy'],
                rag_context=rag_context if rag_context else "No external docs. Rely strictly on the Original Text.",
                original_chunk=original_chunk
            )
            
            response = await self.gemini_service.generate_content(prompt)
            
            return self._parse_ai_response(response, original_chunk)
            
        except Exception as e:
            logger.debug(f"[DEBUG] Error optimizing block - using original: {e}")
            return original_chunk
    
    def _get_rag_context(self, original_chunk: str) -> str:
        """
        Get relevant README context for a resume section.
        
        Args:
            original_chunk: The LaTeX section being optimized
            
        Returns:
            Relevant README content or empty string
        """
        readmes = self.context.get('readmes', {})
        
        for title, doc in readmes.items():
            if title in original_chunk:
                return f"\nPROJECT README (Documentation):\n{doc}\n"
        
        return ""
    
    def _parse_ai_response(self, raw_text: str, original_chunk: str) -> str:
        """
        Parse AI response to extract LaTeX content.
        
        Args:
            raw_text: Raw response from AI
            original_chunk: Original content as fallback
            
        Returns:
            Extracted LaTeX content
        """
        # Extract thoughts (for logging)
        thoughts_pattern = f"{THOUGHTS_START}(.*?){THOUGHTS_END}"
        thoughts_match = re.search(thoughts_pattern, raw_text, re.DOTALL)
        
        if thoughts_match:
            section_preview = original_chunk.splitlines()[1][:40] if len(original_chunk.splitlines()) > 1 else "section"
            logger.debug(f"[DEBUG] AI reasoning for '{section_preview}': {thoughts_match.group(1).strip()[:200]}")
        
        # Extract LaTeX content
        latex_pattern = f"{LATEX_START}(.*?){LATEX_END}"
        latex_match = re.search(latex_pattern, raw_text, re.DOTALL)
        
        if latex_match:
            cleaned_latex = latex_match.group(1).strip()
            # Remove any stray markdown code fences
            cleaned_latex = cleaned_latex.replace("```latex", "").replace("```", "")
            return cleaned_latex
        else:
            logger.debug("[DEBUG] AI response format not recognized - using cleaned raw response")
            return raw_text.replace("```latex", "").replace("```", "").strip()