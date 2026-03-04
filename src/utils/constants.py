"""
Application constants for ResumeEditor.
These are non-configurable constants used throughout the application.
"""

# Jina Reader API
JINA_BASE_URL = "https://r.jina.ai/"

# GitHub raw content base
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/"

# File extensions
LATEX_EXTENSION = ".tex"

# LaTeX regex patterns
LATEX_SECTION_PATTERN = r"((?:\\noindent\s*)?\\textbf\{.*?\}.*?\\begin\{itemize\}.*?\\end\{itemize\})"

# Output markers for AI responses
THOUGHTS_START = ":::THOUGHTS:::"
THOUGHTS_END = ":::END_THOUGHTS:::"
LATEX_START = ":::LATEX:::"
LATEX_END = ":::END_LATEX:::"

__all__ = [
    'JINA_BASE_URL',
    'GITHUB_RAW_BASE',
    'LATEX_EXTENSION',
    'LATEX_SECTION_PATTERN',
    'THOUGHTS_START',
    'THOUGHTS_END',
    'LATEX_START',
    'LATEX_END',
]