"""
Event definitions for ResumeEditor application.
All events are immutable dataclasses representing state changes in the workflow.
"""
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime


@dataclass(frozen=True)
class ApplicationStartedEvent:
    """Triggered when the application begins processing."""
    timestamp: str


@dataclass(frozen=True)
class JobDescriptionFetchedEvent:
    """Triggered when job description is successfully fetched."""
    source: str  # "url" or "manual"
    content: str
    length: int


@dataclass(frozen=True)
class JobDescriptionFetchFailedEvent:
    """Triggered when job description fetching fails."""
    error: str
    source: str


@dataclass(frozen=True)
class StrategyGeneratedEvent:
    """Triggered when application strategy is generated."""
    strategy: str
    job_description: str


@dataclass(frozen=True)
class JobMetadataExtractedEvent:
    """Triggered when job metadata (company, role) is extracted."""
    company: str
    role: str
    address: str


@dataclass(frozen=True)
class ReadmesLoadedEvent:
    """Triggered when README documents are fetched."""
    readmes: Dict[str, str]
    count: int


@dataclass(frozen=True)
class ResumeOptimizedEvent:
    """Triggered when resume is optimized."""
    latex_content: str
    sections_modified: int


@dataclass(frozen=True)
class CoverLetterGeneratedEvent:
    """Triggered when cover letter is generated."""
    latex_content: str


@dataclass(frozen=True)
class FilesWrittenEvent:
    """Triggered when output files are written."""
    resume_path: str
    cover_letter_path: str
    company: str


@dataclass(frozen=True)
class ApplicationCompletedEvent:
    """Triggered when the entire application process completes."""
    company: str
    success: bool
    timestamp: str


@dataclass(frozen=True)
class ApplicationErrorEvent:
    """Triggered when a critical error occurs."""
    stage: str
    error_message: str
    timestamp: str
    recoverable: bool = False