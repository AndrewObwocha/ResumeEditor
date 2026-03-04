"""
Utility helper functions for ResumeEditor.
"""
import json
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be used as a filename.
    Removes special characters and replaces spaces with underscores.
    
    Example:
        "Google Inc." -> "Google_Inc"
    
    Args:
        name: Raw string to sanitize
        
    Returns:
        Sanitized filename-safe string
    """
    clean = re.sub(r'[^\w\s-]', '', name)
    return clean.strip().replace(' ', '_')


def parse_json_safe(json_text: str) -> Dict[str, Any]:
    """
    Robust JSON parser that handles markdown code fences and lists.
    Falls back to default metadata if parsing fails.
    
    Args:
        json_text: Raw JSON string, possibly with markdown formatting
        
    Returns:
        Parsed JSON dictionary, or default values on failure
    """
    try:
        # Remove markdown code fences
        clean_text = json_text.replace("```json", "").replace("```", "").strip()
        
        # Parse JSON
        data = json.loads(clean_text)
        
        # Handle case where AI returns a list instead of object
        if isinstance(data, list):
            if len(data) > 0:
                return data[0]
            else:
                return _default_metadata()
        
        return data
        
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parsing failed: {e}")
        return _default_metadata()
    except Exception as e:
        logger.error(f"Unexpected error parsing JSON: {e}")
        return _default_metadata()


def _default_metadata() -> Dict[str, str]:
    """Return default metadata when parsing fails."""
    return {
        "company": "Company",
        "role": "Software Engineer",
        "address": ""
    }


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


__all__ = [
    'sanitize_filename',
    'parse_json_safe',
    'setup_logging',
    'setup_logging',
]