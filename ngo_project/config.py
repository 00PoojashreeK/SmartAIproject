"""
Configuration module for environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Application Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Validate Gemini API Key
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    raise ValueError(
        "GEMINI_API_KEY not found in .env file. "
        "Please set your Gemini API key in .env file."
    )
