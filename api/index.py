"""Vercel serverless entry point for FastAPI app."""
import sys
from pathlib import Path

# Ensure project root is on path so backend can be imported
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from backend.main import app
