"""
README handler for fetching project documentation from GitHub.
"""
import logging
from typing import TYPE_CHECKING

from src.events.events import JobMetadataExtractedEvent, ReadmesLoadedEvent, ApplicationErrorEvent
from src.services.readme_service import ReadmeService

if TYPE_CHECKING:
    from src.infra.event_bus import EventBus

logger = logging.getLogger(__name__)


class ReadmeHandler:
    """Handles fetching README documentation from configured repositories."""
    
    def __init__(self, event_bus: 'EventBus', readme_service: ReadmeService):
        """
        Initialize handler and subscribe to events.
        
        Args:
            event_bus: Event bus for pub/sub
            readme_service: Service for fetching READMEs
        """
        self.event_bus = event_bus
        self.readme_service = readme_service
        event_bus.subscribe(JobMetadataExtractedEvent, self.handle)
        logger.info("ReadmeHandler initialized")
    
    async def handle(self, event: JobMetadataExtractedEvent) -> None:
        """
        Handle metadata extracted event by fetching READMEs.
        
        Args:
            event: Event containing job metadata
        """
        try:
            # Fetch all READMEs concurrently
            readmes = await self.readme_service.fetch_all_readmes()
            
            # Publish success event even if some READMEs failed
            self.event_bus.publish(ReadmesLoadedEvent(
                readmes=readmes,
                count=len(readmes)
            ))
            
            if len(readmes) == 0:
                logger.warning("[WARN] No READMEs loaded - continuing without project context")
            else:
                logger.info(f"[OK] Loaded {len(readmes)} README files")
            
        except Exception as e:
            error_msg = f"Failed to load READMEs: {e}"
            logger.error(error_msg)
            
            # Publish event with empty readmes to continue workflow
            self.event_bus.publish(ReadmesLoadedEvent(
                readmes={},
                count=0
            ))
            logger.warning("[WARN] Continuing without README context")
