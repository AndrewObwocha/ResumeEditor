"""
Tests for utility functions.
"""
import pytest
import json
from src.utils.helpers import sanitize_filename, parse_json_safe


class TestSanitizeFilename:
    """Test filename sanitization."""
    
    def test_sanitize_simple_name(self):
        """Test sanitizing a simple company name."""
        result = sanitize_filename("Google")
        assert result == "Google"
    
    def test_sanitize_name_with_spaces(self):
        """Test sanitizing name with spaces."""
        result = sanitize_filename("Google Inc")
        assert result == "Google_Inc"
    
    def test_sanitize_name_with_special_chars(self):
        """Test sanitizing name with special characters."""
        result = sanitize_filename("Google, Inc.")
        assert result == "Google_Inc"
    
    def test_sanitize_complex_name(self):
        """Test sanitizing complex company name."""
        result = sanitize_filename("Acme Corp. & Co., Ltd.")
        assert result == "Acme_Corp__Co_Ltd"


class TestParseJsonSafe:
    """Test safe JSON parsing."""
    
    def test_parse_valid_json(self):
        """Test parsing valid JSON."""
        json_str = '{"company": "Google", "role": "Engineer"}'
        result = parse_json_safe(json_str)
        
        assert result["company"] == "Google"
        assert result["role"] == "Engineer"
    
    def test_parse_json_with_markdown_fences(self):
        """Test parsing JSON wrapped in markdown code fences."""
        json_str = '```json\n{"company": "Google", "role": "Engineer"}\n```'
        result = parse_json_safe(json_str)
        
        assert result["company"] == "Google"
        assert result["role"] == "Engineer"
    
    def test_parse_json_list_returns_first_element(self):
        """Test that JSON list returns first element."""
        json_str = '[{"company": "Google"}, {"company": "Amazon"}]'
        result = parse_json_safe(json_str)
        
        assert result["company"] == "Google"
    
    def test_parse_empty_list_returns_default(self):
        """Test that empty list returns default metadata."""
        json_str = '[]'
        result = parse_json_safe(json_str)
        
        assert result["company"] == "Company"
        assert result["role"] == "Software Engineer"
    
    def test_parse_invalid_json_returns_default(self):
        """Test that invalid JSON returns default metadata."""
        json_str = 'not valid json at all'
        result = parse_json_safe(json_str)
        
        assert result["company"] == "Company"
        assert result["role"] == "Software Engineer"
        assert result["address"] == ""
    
    def test_parse_malformed_json_returns_default(self):
        """Test that malformed JSON returns default metadata."""
        json_str = '{"company": "Google", role: Engineer}'  # Missing quotes
        result = parse_json_safe(json_str)
        
        assert result["company"] == "Company"
        assert result["role"] == "Software Engineer"
