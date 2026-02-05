"""
Local run entry point. Use: python app.py (from project root).
Vercel uses api/app.py; this file is for localhost only.
"""
import sys
import os

# Run from project root so api/app resolves templates and static correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from api.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
