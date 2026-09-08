"""
Unit Tests for Scrapers & Fallback Mechanisms
"""

import pytest
from app.scrapers.amazon import AmazonScraper
from app.scrapers.flipkart import FlipkartScraper
from app.scrapers.base import StockStatus
from app.scrapers.fallback_seed import FALLBACK_PHONES

def test_fallback_seed_structure():
    assert "iphone 15" in FALLBACK_PHONES
    assert "amazon" in FALLBACK_PHONES["iphone 15"]
    assert "flipkart" in FALLBACK_PHONES["iphone 15"]

    # Verify out of stock test case is present
    assert "oneplus 12" in FALLBACK_PHONES
    assert FALLBACK_PHONES["oneplus 12"]["flipkart"].stock_status == StockStatus.OUT_OF_STOCK

    # Verify unavailable test case is present
    assert "pixel 8" in FALLBACK_PHONES
    assert FALLBACK_PHONES["pixel 8"]["amazon"].stock_status == StockStatus.CURRENTLY_UNAVAILABLE

def test_amazon_scraper_fallback():
    scraper = AmazonScraper()
    results = scraper.search("iPhone 15", force_live=False)
    assert len(results) > 0
    item = results[0]
    assert item.platform == "amazon"
    assert item.price is not None
    assert item.stock_status in [StockStatus.IN_STOCK, StockStatus.OUT_OF_STOCK, StockStatus.CURRENTLY_UNAVAILABLE]

def test_flipkart_scraper_fallback():
    scraper = FlipkartScraper()
    results = scraper.search("iPhone 15", force_live=False)
    assert len(results) > 0
    item = results[0]
    assert item.platform == "flipkart"
    assert item.price is not None
    assert item.stock_status in [StockStatus.IN_STOCK, StockStatus.OUT_OF_STOCK, StockStatus.CURRENTLY_UNAVAILABLE]
