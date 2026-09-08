"""
Unit Tests for Smartphone Fuzzy Matcher
"""

import pytest
from app.pipeline.matcher import SmartphoneMatcher
from app.scrapers.base import ProductData, StockStatus

def test_extract_storage():
    assert SmartphoneMatcher.extract_storage("iPhone 15 128GB Black") == "128GB"
    assert SmartphoneMatcher.extract_storage("Samsung Galaxy S24 (256 GB)") == "256GB"
    assert SmartphoneMatcher.extract_storage("OnePlus 12 512 gb") == "512GB"
    assert SmartphoneMatcher.extract_storage("iPhone 15 Pro Max 1TB") == "1TB"
    assert SmartphoneMatcher.extract_storage("Simple Phone without storage") is None

def test_extract_ram():
    assert SmartphoneMatcher.extract_ram("Samsung S24 8GB RAM 256GB") == "8GBRAM"
    assert SmartphoneMatcher.extract_ram("OnePlus 12 12 GB RAM") == "12GBRAM"
    assert SmartphoneMatcher.extract_ram("iPhone 15 128GB") is None

def test_clean_title():
    cleaned = SmartphoneMatcher.clean_title("Apple iPhone 15 5G Smartphone (Black, 128GB)")
    assert "5G" not in cleaned
    assert "Smartphone" not in cleaned
    assert "(" not in cleaned
    assert ")" not in cleaned

def test_match_best_pair_exact_storage():
    amz_list = [
        ProductData(
            platform="amazon",
            title="Apple iPhone 15 (128 GB) - Blue",
            price=70999.0,
            mrp=79600.0,
            discount_percent=11.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock",
            rating=4.5,
            reviews_count=1000,
            product_url="https://amazon.in",
            image_url=None
        ),
        ProductData(
            platform="amazon",
            title="Apple iPhone 15 (256 GB) - Blue",
            price=79999.0,
            mrp=89600.0,
            discount_percent=10.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock",
            rating=4.5,
            reviews_count=500,
            product_url="https://amazon.in",
            image_url=None
        )
    ]

    fpk_list = [
        ProductData(
            platform="flipkart",
            title="Apple iPhone 15 (Blue, 128 GB)",
            price=65999.0,
            mrp=79600.0,
            discount_percent=17.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock",
            rating=4.6,
            reviews_count=2000,
            product_url="https://flipkart.com",
            image_url=None
        )
    ]

    matched_amz, matched_fpk, score = SmartphoneMatcher.match_best_pair(
        amz_list, fpk_list, "iPhone 15 128GB"
    )

    assert matched_amz is not None
    assert matched_fpk is not None
    assert "128 GB" in matched_amz.title
    assert "128 GB" in matched_fpk.title
    assert score > 70.0
