"""
Configuration tests for ResumeEditor.
"""
import unittest
import os
from unittest.mock import patch

from src.config import Settings


class TestSettings(unittest.TestCase):
    """Test Settings configuration loading."""
    
    @patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test_key_12345',
        'MODEL_NAME': 'test-model',
        'OUTPUT_DIR': 'test_output',
        'LOG_LEVEL': 'DEBUG'
    })
    def test_settings_load_from_env(self):
        """Test that settings load correctly from environment variables."""
        settings = Settings.load()
        
        self.assertEqual(settings.GEMINI_API_KEY, 'test_key_12345')
        self.assertEqual(settings.MODEL_NAME, 'test-model')
        self.assertEqual(settings.OUTPUT_DIR, 'test_output')
        self.assertEqual(settings.LOG_LEVEL, 'DEBUG')
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}, clear=True)
    def test_settings_default_values(self):
        """Test that default values are used when env vars not set."""
        settings = Settings.load()
        
        self.assertEqual(settings.MODEL_NAME, 'gemini-2.0-flash')
        self.assertEqual(settings.OUTPUT_DIR, 'output')
        self.assertEqual(settings.LOG_LEVEL, 'INFO')
    
    @patch.dict(os.environ, {}, clear=True)
    def test_settings_missing_api_key_raises(self):
        """Test that missing API key raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Settings.load()
        
        self.assertIn('GEMINI_API_KEY', str(context.exception))


if __name__ == '__main__':
    unittest.main()