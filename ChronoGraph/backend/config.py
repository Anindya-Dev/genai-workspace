import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
MOCK_DATA_DIR = DATA_DIR / "mock"
NORMALIZED_DATA_DIR = DATA_DIR / "normalized"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
