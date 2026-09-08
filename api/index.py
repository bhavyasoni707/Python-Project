"""
Vercel Serverless Entry Point
This file is detected by Vercel's @vercel/python builder.
It imports and exposes the FastAPI app as 'app'.
"""

import sys
from pathlib import Path

# Add project root to Python path so imports work on Vercel
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: F401 — Vercel needs 'app' in this module's namespace
