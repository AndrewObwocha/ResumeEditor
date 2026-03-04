"""
File writer handler for writing LaTeX output files.
"""
import logging
from typing import TYPE_CHECKING
from datetime import datetime

from src.events.events import CoverLetterGeneratedEvent, FilesWrittenEvent, ApplicationCompletedEvent, ApplicationErrorEvent
from src.services.file_writer_service import FileWriterService
from src.models.context import JobMetadata

if TYPE_CHECKING:
    from src.infra.event_bus import EventBus

logger = logging.getLogger(__name__)


class FileWriterHandler:
    """Handles writing resume and cover letter files to disk."""
    
    def __init__(
        self,
        event_bus: 'EventBus',
        file_writer_service: FileWriterService,
        job_metadata: JobMetadata,
        resume_content: str
    ):
        """
        Initialize handler and subscribe to events.
        
        Args:
            event_bus: Event bus for pub/sub
            file_writer_service: Service for file writing
            job_metadata: Job metadata for filename generation
            resume_content: Resume LaTeX content (stored for writing)
        """
        self.event_bus = event_bus
        self.file_writer_service = file_writer_service
        self.job_metadata = job_metadata
        self.resume_content = resume_content
        event_bus.subscribe(CoverLetterGeneratedEvent, self.handle)
        logger.info("FileWriterHandler initialized")
    
    async def handle(self, event: CoverLetterGeneratedEvent) -> None:
        """
        Handle cover letter generated event by writing files.
        
        Args:
            event: Event containing cover letter content
        """
        try:
            logger.info("[PROGRESS] Writing output files")
            
            # Write both files
            resume_path, cover_letter_path = await self.file_writer_service.write_latex_files(
                resume_content=self.resume_content,
                cover_letter_content=event.latex_content,
                metadata=self.job_metadata
            )
            
            # Publish files written event
            self.event_bus.publish(FilesWrittenEvent(
                resume_path=resume_path,
                cover_letter_path=cover_letter_path,
                company=self.job_metadata.company
            ))
            
            # Publish completion event
            self.event_bus.publish(ApplicationCompletedEvent(
                company=self.job_metadata.company,
                success=True,
                timestamp=datetime.now().isoformat()
            ))
            
            print(f"\n[SUCCESS] Generated application materials for {self.job_metadata.company}")
            print(f"  - Resume: {resume_path}")
            print(f"  - Cover Letter: {cover_letter_path}")
            
        except Exception as e:
            error_msg = f"Failed to write files: {e}"
            logger.error(error_msg)
            self.event_bus.publish(ApplicationErrorEvent(
                stage="file_writing",
                error_message=error_msg,
                timestamp=datetime.now().isoformat(),
                recoverable=False
            ))
