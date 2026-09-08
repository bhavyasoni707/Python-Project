"""
Scrapers Package
"""

from .base import BaseScraper, ProductData, StockStatus
from .amazon import AmazonScraper
from .flipkart import FlipkartScraper
from .fallback_seed import FALLBACK_PHONES, get_fallback_product

__all__ = [
    "BaseScraper",
    "ProductData",
    "StockStatus",
    "AmazonScraper",
    "FlipkartScraper",
    "FALLBACK_PHONES",
    "get_fallback_product",
]
