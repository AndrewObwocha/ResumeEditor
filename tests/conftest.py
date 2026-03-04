"""
Pytest configuration for ResumeEditor tests.
"""
import pytest
import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


@pytest.fixture
def sample_job_description():
    """Sample job description for testing."""
    return """
    Senior Software Engineer - Cloud Infrastructure
    
    Google is seeking an experienced Software Engineer to join our cloud team.
    
    Requirements:
    - 5+ years of experience with Python and cloud platforms
    - Strong knowledge of AWS, GCP, or Azure
    - Experience with Kubernetes and Docker
    - Excellent communication skills
    
    Location: Mountain View, CA
    """


@pytest.fixture
def sample_strategy():
    """Sample application strategy for testing."""
    return """
    Focus on cloud infrastructure experience and Python expertise.
    Highlight containerization skills (Docker, Kubernetes).
    Emphasize distributed systems knowledge.
    Demonstrate strong problem-solving abilities.
    """


@pytest.fixture
def sample_metadata():
    """Sample job metadata for testing."""
    from src.models.context import JobMetadata
    return JobMetadata(
        company="Google",
        role="Senior Software Engineer",
        address="Mountain View, CA"
    )


@pytest.fixture
def sample_readmes():
    """Sample README content for testing."""
    return {
        "Cloud Project": "# Cloud Infrastructure\n\nBuilt scalable cloud platform using AWS...",
        "API Gateway": "# API Gateway Service\n\nMicroservices architecture with Docker...",
    }
