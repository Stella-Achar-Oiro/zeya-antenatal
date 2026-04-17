"""Uvicorn entrypoint.

Import the app object here so uvicorn can find it:
    uv run uvicorn app.main:app --reload --port 8000
"""

from dotenv import load_dotenv

load_dotenv()

from app.factory import create_app  # noqa: E402

app = create_app()
