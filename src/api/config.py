import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_IMAGE_DIR = PROJECT_ROOT / "data" / "raw"

EVALUATION_RESULTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "results.json"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")