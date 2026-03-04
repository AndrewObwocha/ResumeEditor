"""
Configuration management for ResumeEditor.
Loads settings from environment variables and provides application-wide constants.
"""
import os
from dataclasses import dataclass
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""
    
    GEMINI_API_KEY: str
    MODEL_NAME: str
    OUTPUT_DIR: str
    PROJECT_REPO_MAP: Dict[str, str]
    LOG_LEVEL: str
    
    @classmethod
    def load(cls) -> 'Settings':
        """Load settings from environment variables."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        return cls(
            GEMINI_API_KEY=api_key,
            MODEL_NAME=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
            OUTPUT_DIR=os.getenv("OUTPUT_DIR", "output"),
            PROJECT_REPO_MAP={
                "Knowledge Graph": "https://github.com/AndrewObwocha/GraphMind",
                "Tokenized Note System": "https://github.com/AndrewObwocha/UniNotes",
                "House Forecaster": "https://github.com/AndrewObwocha/HouseValuator",
            },
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        )


# Singleton settings instance
settings = Settings.load()
