"""Vercel entry point. Vercel's Python runtime looks for a WSGI `app` object
in a file under api/ — this just re-exports the real Flask app from app/main.py
so the actual application code lives in one place."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

from main import app  # noqa: E402
