import os
from pathlib import Path
from dotenv import load_dotenv

# Find root .env file
root_dir = Path(__file__).resolve().parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8088))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 5174))
HOST = os.getenv("HOST", "0.0.0.0")
