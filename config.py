# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your chosen LLM's API key
# Using Gemini as an example
API_KEY = os.getenv("GEMINI_API_KEY")