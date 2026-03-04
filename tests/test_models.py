"""
Tests for domain models.
"""
import pytest
from src.models.context import (
    JobDescription,
    JobStrategy,
    JobMetadata,
    ApplicationContext
)


class TestJobDescription:
    """Test JobDescription model."""
    
    def test_create_from_content(self):
        """Test JobDescription creation from content."""
        content = "Software Engineer needed for cloud infrastructure."
        job_desc = JobDescription.from_content(content, source="url")
        
        assert job_desc.source == "url"
        assert job_desc.content == content
        assert job_desc.length == len(content)
    
    def test_frozen_dataclass(self):
        """Test that JobDescription is immutable."""
        job_desc = JobDescription.from_content("Test content")
        
        with pytest.raises(AttributeError):
            job_desc.content = "Modified content"


class TestJobMetadata:
    """Test JobMetadata model."""
    
    def test_create_metadata(self):
        """Test JobMetadata creation."""
        metadata = JobMetadata(
            company="Google",
            role="Senior Software Engineer",
            address="Mountain View, CA"
        )
        
        assert metadata.company == "Google"
        assert metadata.role == "Senior Software Engineer"
        assert metadata.address == "Mountain View, CA"
    
    def test_default_metadata(self):
        """Test default metadata creation."""
        metadata = JobMetadata.default()
        
        assert metadata.company == "Company"
        assert metadata.role == "Software Engineer"
        assert metadata.address == ""


class TestApplicationContext:
    """Test ApplicationContext model."""
    
    def test_empty_context(self):
        """Test creating empty application context."""
        context = ApplicationContext()
        
        assert context.job_description is None
        assert context.job_strategy is None
        assert context.job_metadata is None
        assert context.readmes == {}
        assert context.resume_content is None
        assert context.cover_letter_content is None
    
    def test_is_ready_for_resume(self):
        """Test ready check for resume generation."""
        context = ApplicationContext()
        assert not context.is_ready_for_resume()
        
        # Add required fields
        context.job_description = JobDescription.from_content("Test job")
        context.job_strategy = JobStrategy(
            strategy_text="Focus on cloud",
            job_description="Test"
        )
        context.job_metadata = JobMetadata.default()
        context.readmes = {"Project": "README content"}
        
        assert context.is_ready_for_resume()
    
    def test_is_ready_for_cover_letter(self):
        """Test ready check for cover letter generation."""
        context = ApplicationContext()
        assert not context.is_ready_for_cover_letter()
        
        # Add all required fields
        context.job_description = JobDescription.from_content("Test job")
        context.job_strategy = JobStrategy(
            strategy_text="Focus on cloud",
            job_description="Test"
        )
        context.job_metadata = JobMetadata.default()
        context.readmes = {"Project": "README content"}
        context.resume_content = "Resume LaTeX"
        
        assert context.is_ready_for_cover_letter()
    
    def test_is_complete(self):
        """Test complete check for entire workflow."""
        context = ApplicationContext()
        assert not context.is_complete()
        
        context.resume_content = "Resume LaTeX"
        context.cover_letter_content = "Cover letter LaTeX"
        
        assert context.is_complete()
