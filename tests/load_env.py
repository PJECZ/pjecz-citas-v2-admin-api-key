"""
Load environment variables
"""
import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "api_key": os.getenv("API_KEY", ""),
    "host": os.getenv("HOST", "http://127.0.0.1:8000"),
    "timeout": int(os.getenv("TIMEOUT", "10")),
}
