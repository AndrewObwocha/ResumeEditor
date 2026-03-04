"""
Domain models for ResumeEditor application context.
These dataclasses represent the core data structures passed between handlers.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class JobDescription:
    """Represents a fetched job description."""
    
    source: str  # "url" or "manual"
    content: str
    length: int
    
    @classmethod
    def from_content(cls, content: str, source: str = "manual") -> 'JobDescription':
        """Create a JobDescription from content string."""
        return cls(
            source=source,
            content=content,
            length=len(content)
        )


@dataclass(frozen=True)
class JobStrategy:
    """Represents the application strategy for a job."""
    
    strategy_text: str
    job_description: str


@dataclass(frozen=True)
class JobMetadata:
    """Metadata extracted from job description."""
    
    company: str
    role: str
    address: str = ""
    
    @classmethod
    def default(cls) -> 'JobMetadata':
        """Return default metadata when extraction fails."""
        return cls(
            company="Company",
            role="Software Engineer",
            address=""
        )


@dataclass
class ApplicationContext:
    """
    Complete application context passed through the event-driven workflow.
    Mutable to allow handlers to add data incrementally.
    """
    
    job_description: Optional[JobDescription] = None
    job_strategy: Optional[JobStrategy] = None
    job_metadata: Optional[JobMetadata] = None
    readmes: Dict[str, str] = field(default_factory=dict)
    resume_content: Optional[str] = None
    cover_letter_content: Optional[str] = None
    
    def is_ready_for_resume(self) -> bool:
        """Check if context has all required data for resume generation."""
        return all([
            self.job_description is not None,
            self.job_strategy is not None,
            self.job_metadata is not None,
            len(self.readmes) > 0
        ])
    
    def is_ready_for_cover_letter(self) -> bool:
        """Check if context has all required data for cover letter generation."""
        return self.is_ready_for_resume() and self.resume_content is not None
    
    def is_complete(self) -> bool:
        """Check if all content has been generated."""
        return all([
            self.resume_content is not None,
            self.cover_letter_content is not None
        ])
