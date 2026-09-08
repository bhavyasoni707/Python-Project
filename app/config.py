"""
Application Configuration and Constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"

# PostgreSQL / Neon Database Connection URL
# Set via .env locally or Vercel Environment Variables in production
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    ""  # Will raise clear error if not set
)

if not DATABASE_URL:
    raise EnvironmentError(
        "DATABASE_URL environment variable is not set.\n"
        "Create a .env file with: DATABASE_URL=postgresql://..."
    )

# Scraping Settings
SCRAPE_TIMEOUT = 12  # seconds
SCRAPE_MAX_RETRIES = 2
FUZZY_MATCH_THRESHOLD = 70  # RapidFuzz similarity threshold (raised for strictness)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

# Popular Smartphone Presets for Quick Search
POPULAR_PHONES = [
    {"name": "Apple iPhone 15 (128 GB)", "brand": "Apple", "query": "Apple iPhone 15 128GB"},
    {"name": "Samsung Galaxy S24 (256 GB)", "brand": "Samsung", "query": "Samsung Galaxy S24 256GB"},
    {"name": "OnePlus 12 5G (256 GB)", "brand": "OnePlus", "query": "OnePlus 12 256GB"},
    {"name": "Google Pixel 8 (128 GB)", "brand": "Google", "query": "Google Pixel 8 128GB"},
    {"name": "Nothing Phone (2) (128 GB)", "brand": "Nothing", "query": "Nothing Phone 2 128GB"},
    {"name": "Redmi Note 13 Pro+ (256 GB)", "brand": "Xiaomi", "query": "Redmi Note 13 Pro Plus 256GB"},
    {"name": "iPhone 15 Pro Max (256 GB)", "brand": "Apple", "query": "Apple iPhone 15 Pro Max 256GB"},
    {"name": "Samsung Galaxy A55 (128 GB)", "brand": "Samsung", "query": "Samsung Galaxy A55 128GB"},
]
