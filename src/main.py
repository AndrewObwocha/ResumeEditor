"""
ResumeEditor - AI-powered resume and cover letter generator.
Main entry point with event-driven architecture.
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional

from src.config import settings
from src.utils.helpers import setup_logging
from src.infra.event_bus import EventBus
from src.events.events import (
    ApplicationStartedEvent,
    JobDescriptionFetchedEvent,
    JobDescriptionFetchFailedEvent,
    ApplicationErrorEvent,
    ApplicationCompletedEvent,
)
from src.models.context import JobMetadata
from src.services import (
    GeminiService,
    JobFetcherService,
    ReadmeService,
    FileWriterService,
)
from src.handlers import (
    StrategyHandler,
    MetadataHandler,
    ReadmeHandler,
    ResumeHandler,
    CoverLetterHandler,
    FileWriterHandler,
)

logger = logging.getLogger(__name__)


class ResumeEditorApp:
    """Main application orchestrator for ResumeEditor."""
    
    def __init__(self):
        """Initialize the application components."""
        # Setup logging
        setup_logging(settings.LOG_LEVEL)
        
        # Initialize event bus
        self.event_bus = EventBus()
        
        # Initialize services
        self.gemini_service = GeminiService()
        self.job_fetcher_service = JobFetcherService()
        self.readme_service = ReadmeService()
        self.file_writer_service = FileWriterService()
        
        # State for passing between handlers
        self.job_strategy: Optional[str] = None
        self.job_description: Optional[str] = None
        self.job_metadata: Optional[JobMetadata] = None
        self.readmes: dict = {}
        self.resume_content: Optional[str] = None
        
        logger.info("ResumeEditor initialized")
    
    async def run(self) -> None:
        """Main application workflow."""
        try:
            logger.info("[START] ResumeEditor application started")
            
            # Publish start event
            self.event_bus.publish(ApplicationStartedEvent(
                timestamp=datetime.now().isoformat()
            ))
            
            # Step 1: Fetch job description
            job_desc = await self._fetch_job_description()
            if not job_desc:
                logger.error("Failed to fetch job description")
                return
            
            self.job_description = job_desc.content
            
            # Step 2: Generate strategy
            logger.info("[STAGE] Analyzing job strategy")
            
            self.job_strategy = await self._generate_strategy(job_desc)
            
            # Step 3: Extract metadata
            logger.info("[STAGE] Extracting job metadata")
            
            self.job_metadata = await self._extract_metadata()
            
            # Step 4: Load READMEs
            logger.info("[STAGE] Loading project documentation")
            
            self.readmes = await self.readme_service.fetch_all_readmes()
            
            # Step 5: Optimize resume
            logger.info("[STAGE] Optimizing resume")
            
            self.resume_content = await self._optimize_resume()
            
            # Step 6: Generate cover letter
            logger.info("[STAGE] Generating cover letter")
            
            cover_letter_content = await self._generate_cover_letter()
            
            # Step 7: Write files
            logger.info("[STAGE] Writing output files")
            
            await self._write_files(cover_letter_content)
            
            logger.info("[SUCCESS] Application completed")
            
        except Exception as e:
            error_msg = f"Application failed: {e}"
            logger.error(error_msg, exc_info=True)
            self.event_bus.publish(ApplicationErrorEvent(
                stage="main",
                error_message=error_msg,
                timestamp=datetime.now().isoformat(),
                recoverable=False
            ))
            raise
    
    async def _fetch_job_description(self):
        """Fetch job description from URL or manual input."""
        print("\n[INPUT] Provide job description")
        
        choice = input("\nHow would you like to provide the job description?\n"
                      "  1. URL (via Jina Reader)\n"
                      "  2. Manual paste\n"
                      "Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            url = input("\nEnter Job URL: ").strip()
            logger.info(f"Fetching via Jina Reader...")
            job_desc = await self.job_fetcher_service.fetch_from_url(url)
            
            if not job_desc:
                logger.warning("URL fetching failed. Falling back to manual input.")
                job_desc = await self.job_fetcher_service.fetch_from_input()
        else:
            job_desc = await self.job_fetcher_service.fetch_from_input()
        
        if job_desc:
            await self.event_bus.publish_async(JobDescriptionFetchedEvent(
                source=job_desc.source,
                content=job_desc.content,
                length=job_desc.length
            ))
        
        return job_desc
    
    async def _generate_strategy(self, job_desc):
        """Generate application strategy."""
        from src.prompts import APPLICATION_STRATEGY_PROMPT
        
        prompt = APPLICATION_STRATEGY_PROMPT.format(
            job_description=job_desc.content
        )
        
        strategy = await self.gemini_service.generate_content(prompt)
        logger.info("[OK] Strategy generation complete")
        return strategy
    
    async def _extract_metadata(self):
        """Extract job metadata."""
        from src.prompts import JOB_METADATA_EXTRACTION_PROMPT
        from src.utils.helpers import parse_json_safe
        
        prompt = JOB_METADATA_EXTRACTION_PROMPT.format(
            job_description=self.job_description
        )
        
        json_response = await self.gemini_service.generate_json(prompt)
        metadata_dict = parse_json_safe(json_response)
        
        metadata = JobMetadata(
            company=metadata_dict.get("company", "Company"),
            role=metadata_dict.get("role", "Software Engineer"),
            address=metadata_dict.get("address", "")
        )
        
        logger.info(f"[OK] Metadata extracted: {metadata.company} - {metadata.role}")
        return metadata
    
    async def _optimize_resume(self):
        """Optimize resume content."""
        from src.resume import ResumeOptimizer
        
        optimizer = ResumeOptimizer(self.gemini_service)
        context = {
            'job_strategy': self.job_strategy,
            'readmes': self.readmes,
            'job_description': self.job_description
        }
        
        resume_latex, sections_count = await optimizer.optimize_resume(context)
        logger.info(f"[OK] Resume optimization complete - {sections_count} sections")
        return resume_latex
    
    async def _generate_cover_letter(self):
        """Generate cover letter."""
        from src.cover_letter import CoverLetterGenerator
        
        generator = CoverLetterGenerator(self.gemini_service)
        context = {
            'job_strategy': self.job_strategy,
            'job_description': self.job_description,
            'readmes': self.readmes,
            'metadata': self.job_metadata
        }
        
        cover_letter = await generator.generate_cover_letter(context)
        logger.info("[OK] Cover letter generation complete")
        return cover_letter
    
    async def _write_files(self, cover_letter_content):
        """Write output files."""
        resume_path, cl_path = await self.file_writer_service.write_latex_files(
            resume_content=self.resume_content,
            cover_letter_content=cover_letter_content,
            metadata=self.job_metadata
        )
        
        print(f"\n[SUCCESS] Generated application materials for {self.job_metadata.company}")
        print(f"  - Resume: {resume_path}")
        print(f"  - Cover Letter: {cl_path}\n")
        
        self.event_bus.publish(ApplicationCompletedEvent(
            company=self.job_metadata.company,
            success=True,
            timestamp=datetime.now().isoformat()
        ))


async def async_main():
    """Async entry point."""
    app = ResumeEditorApp()
    await app.run()


def main():
    """Synchronous entry point for the application."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("\n\nApplication interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
