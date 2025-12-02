import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

MODEL_NAME = 'gemini-2.0-flash'

PROJECT_REPO_MAP = {
    "Knowledge Graph": "https://github.com/AndrewObwocha/GraphMind",
    "Tokenized Note System": "https://github.com/AndrewObwocha/UniNotes",
    "House Forecaster": "https://github.com/AndrewObwocha/HouseValuator",
}

SKIP_KEYWORDS = [
    "Bachelor of Science", 
    "The University of Alberta", 
    "GPA:", 
    "Valedictorian",
    "Technical Skills"
]