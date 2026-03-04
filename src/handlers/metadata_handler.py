"""
Metadata handler for extracting company, role, and address from job descriptions.
"""
import logging
from typing import TYPE_CHECKING
from datetime import datetime

from src.events.events import StrategyGeneratedEvent, JobMetadataExtractedEvent, ApplicationErrorEvent
from src.services.gemini_service import GeminiService
from src.prompts import JOB_METADATA_EXTRACTION_PROMPT
from src.utils.helpers import parse_json_safe
from src.models.context import JobMetadata

if TYPE_CHECKING:
    from src.infra.event_bus import EventBus

logger = logging.getLogger(__name__)


class MetadataHandler:
    """Handles extraction of metadata from job descriptions."""
    
    def __init__(self, event_bus: 'EventBus', gemini_service: GeminiService):
        """
        Initialize handler and subscribe to events.
        
        Args:
            event_bus: Event bus for pub/sub
            gemini_service: Gemini service for AI generation
        """
        self.event_bus = event_bus
        self.gemini_service = gemini_service
        event_bus.subscribe(StrategyGeneratedEvent, self.handle)
        logger.info("MetadataHandler initialized")
    
    async def handle(self, event: StrategyGeneratedEvent) -> None:
        """
        Handle strategy generated event by extracting metadata.
        
        Args:
            event: Event containing strategy and job description
        """
        try:
            logger.info("Extracting job metadata (Company/Role)...")
            
            # Format prompt with job description
            prompt = JOB_METADATA_EXTRACTION_PROMPT.format(
                job_description=event.job_description
            )
            
            # Generate JSON metadata
            json_response = await self.gemini_service.generate_json(prompt)
            
            # Parse JSON safely
            metadata_dict = parse_json_safe(json_response)
            
            # Create JobMetadata object
            metadata = JobMetadata(
                company=metadata_dict.get("company", "Company"),
                role=metadata_dict.get("role", "Software Engineer"),
                address=metadata_dict.get("address", "")
            )
            
            # Publish success event
            self.event_bus.publish(JobMetadataExtractedEvent(
                company=metadata.company,
                role=metadata.role,
                address=metadata.address
            ))
            
            logger.info(f"[OK] Metadata extracted: {metadata.company} - {metadata.role}")
            
        except Exception as e:
            error_msg = f"Failed to extract metadata: {e}"
            logger.warning(error_msg)
            
            # Use default metadata and continue
            default_meta = JobMetadata.default()
            self.event_bus.publish(JobMetadataExtractedEvent(
                company=default_meta.company,
                role=default_meta.role,
                address=default_meta.address
            ))
            logger.info("[OK] Using default metadata")
