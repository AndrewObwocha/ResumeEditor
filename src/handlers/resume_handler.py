"""
Resume handler for optimizing resume content against job descriptions.
"""
import logging
from typing import TYPE_CHECKING

from src.events.events import ReadmesLoadedEvent, ResumeOptimizedEvent, ApplicationErrorEvent
from src.services.gemini_service import GeminiService
from src.resume import ResumeOptimizer

if TYPE_CHECKING:
    from src.infra.event_bus import EventBus

logger = logging.getLogger(__name__)


class ResumeHandler:
    """Handles resume optimization based on job requirements."""
    
    def __init__(
        self,
        event_bus: 'EventBus',
        gemini_service: GeminiService,
        job_strategy: str,
        job_description: str
    ):
        """
        Initialize handler and subscribe to events.
        
        Args:
            event_bus: Event bus for pub/sub
            gemini_service: Gemini service for AI generation
            job_strategy: Application strategy for the job
            job_description: Job description text
        """
        self.event_bus = event_bus
        self.gemini_service = gemini_service
        self.job_strategy = job_strategy
        self.job_description = job_description
        self.optimizer = ResumeOptimizer(gemini_service)
        event_bus.subscribe(ReadmesLoadedEvent, self.handle)
        logger.info("ResumeHandler initialized")
    
    async def handle(self, event: ReadmesLoadedEvent) -> None:
        """
        Handle READMEs loaded event by optimizing resume.
        
        Args:
            event: Event containing README documentation
        """
        try:
            logger.info("[PROGRESS] Optimizing resume bullet points")
            
            # Build context for resume optimization
            context = {
                'job_strategy': self.job_strategy,
                'readmes': event.readmes,
                'job_description': self.job_description
            }
            
            # Optimize resume
            optimized_latex, sections_count = await self.optimizer.optimize_resume(context)
            
            # Publish success event
            self.event_bus.publish(ResumeOptimizedEvent(
                latex_content=optimized_latex,
                sections_modified=sections_count
            ))
            
            logger.info(f"[OK] Resume optimization complete - {sections_count} sections")
            
        except Exception as e:
            error_msg = f"Failed to optimize resume: {e}"
            logger.error(error_msg)
            self.event_bus.publish(ApplicationErrorEvent(
                stage="resume_optimization",
                error_message=error_msg,
                timestamp=str(None),
                recoverable=False
            ))
