"""Vercel serverless entry point.
Local development does NOT use this file — run `uvicorn main:app` instead.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  
 