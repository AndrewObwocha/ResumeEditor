"""
Cover letter handler for generating personalized cover letters.
"""
import logging
from typing import TYPE_CHECKING

from src.events.events import ResumeOptimizedEvent, CoverLetterGeneratedEvent, ApplicationErrorEvent
from src.services.gemini_service import GeminiService
from src.cover_letter import CoverLetterGenerator
from src.models.context import JobMetadata

if TYPE_CHECKING:
    from src.infra.event_bus import EventBus

logger = logging.getLogger(__name__)


class CoverLetterHandler:
    """Handles cover letter generation based on job requirements."""
    
    def __init__(
        self,
        event_bus: 'EventBus',
        gemini_service: GeminiService,
        job_strategy: str,
        job_description: str,
        job_metadata: JobMetadata,
        readmes: dict
    ):
        """
        Initialize handler and subscribe to events.
        
        Args:
            event_bus: Event bus for pub/sub
            gemini_service: Gemini service for AI generation
            job_strategy: Application strategy for the job
            job_description: Job description text
            job_metadata: Job metadata (company, role, address)
            readmes: Project README documentation
        """
        self.event_bus = event_bus
        self.gemini_service = gemini_service
        self.job_strategy = job_strategy
        self.job_description = job_description
        self.job_metadata = job_metadata
        self.readmes = readmes
        self.generator = CoverLetterGenerator(gemini_service)
        event_bus.subscribe(ResumeOptimizedEvent, self.handle)
        logger.info("CoverLetterHandler initialized")
    
    async def handle(self, event: ResumeOptimizedEvent) -> None:
        """
        Handle resume optimized event by generating cover letter.
        
        Args:
            event: Event containing optimized resume
        """
        try:
            logger.info("[PROGRESS] Generating cover letter")
            
            context = {
                'job_strategy': self.job_strategy,
                'job_description': self.job_description,
                'readmes': self.readmes,
                'metadata': self.job_metadata
            }
            
            cover_letter_latex = await self.generator.generate_cover_letter(context)
            
            self.event_bus.publish(CoverLetterGeneratedEvent(
                latex_content=cover_letter_latex
            ))
            
            logger.info("[OK] Cover letter generation complete")
            
        except Exception as e:
            error_msg = f"Failed to generate cover letter: {e}"
            logger.error(error_msg)
            self.event_bus.publish(ApplicationErrorEvent(
                stage="cover_letter_generation",
                error_message=error_msg,
                timestamp=str(None),
                recoverable=False
            ))
