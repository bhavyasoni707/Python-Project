"""
Single-Click Launcher for Amazon vs Flipkart Smartphone Price Comparison Analyzer
"""

import sys
import uvicorn
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.database.db import init_db

def main():
    print("=" * 70)
    print(" PriceSnap — Amazon vs Flipkart Smartphone Price Comparison ")
    print("=" * 70)
    print("[*] Connecting to Neon PostgreSQL database...")
    init_db()
    print("[*] Database connected & tables ready.")
    print("[*] Starting FastAPI server → http://127.0.0.1:8000")
    print("=" * 70)
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
