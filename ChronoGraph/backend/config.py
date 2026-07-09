from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MOCK_DATA_DIR = DATA_DIR / "mock"
NORMALIZED_DATA_DIR = DATA_DIR / "normalized"

load_dotenv(BASE_DIR / ".env")

