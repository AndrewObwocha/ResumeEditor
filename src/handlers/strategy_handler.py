"""
Strategy handler for generating application strategies from job descriptions.
"""
import logging
from typing import TYPE_CHECKING

from src.events.events import JobDescriptionFetchedEvent, StrategyGeneratedEvent, ApplicationErrorEvent
from src.services.gemini_service import GeminiService
from src.prompts import APPLICATION_STRATEGY_PROMPT

if TYPE_CHECKING:
    from src.infra.event_bus import EventBus

logger = logging.getLogger(__name__)


class StrategyHandler:
    """Handles generation of application strategies from job descriptions."""
    
    def __init__(self, event_bus: 'EventBus', gemini_service: GeminiService):
        """
        Initialize handler and subscribe to events.
        
        Args:
            event_bus: Event bus for pub/sub
            gemini_service: Gemini service for AI generation
        """
        self.event_bus = event_bus
        self.gemini_service = gemini_service
        event_bus.subscribe(JobDescriptionFetchedEvent, self.handle)
        logger.info("StrategyHandler initialized")
    
    async def handle(self, event: JobDescriptionFetchedEvent) -> None:
        """
        Handle job description fetched event by generating strategy.
        
        Args:
            event: Event containing job description
        """
        try:
            logger.info("Analyzing job strategy...")
            
            # Format prompt with job description
            prompt = APPLICATION_STRATEGY_PROMPT.format(
                job_description=event.content
            )
            
            # Generate strategy
            strategy = await self.gemini_service.generate_content(prompt)
            
            # Publish success event
            self.event_bus.publish(StrategyGeneratedEvent(
                strategy=strategy,
                job_description=event.content
            ))
            
            logger.info("[OK] Strategy generation complete")
            
        except Exception as e:
            error_msg = f"Failed to generate strategy: {e}"
            logger.error(error_msg)
            self.event_bus.publish(ApplicationErrorEvent(
                stage="strategy_generation",
                error_message=error_msg,
                timestamp=str(None),  # Will be set by event
                recoverable=False
            ))
