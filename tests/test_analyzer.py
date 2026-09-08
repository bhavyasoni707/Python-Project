"""
Unit Tests for Comparison and Stock Availability Analyzer
"""

import pytest
from app.pipeline.analyzer import ComparisonAnalyzer
from app.scrapers.base import ProductData, StockStatus

def create_sample_product(platform: str, price: float, stock_status: StockStatus, title: str = "Test Phone"):
    return ProductData(
        platform=platform,
        title=title,
        price=price,
        mrp=price * 1.1,
        discount_percent=10.0,
        stock_status=stock_status,
        stock_message=f"{stock_status.value} on {platform}",
        rating=4.5,
        reviews_count=100,
        product_url=f"https://{platform}.com",
        image_url=None
    )

def test_flipkart_cheaper_when_both_in_stock():
    amz = create_sample_product("amazon", 70000.0, StockStatus.IN_STOCK)
    fpk = create_sample_product("flipkart", 65000.0, StockStatus.IN_STOCK)

    analysis = ComparisonAnalyzer.analyze(amz, fpk, "Test Phone")

    assert analysis["cheaper_platform"] == "flipkart"
    assert analysis["price_diff"] == 5000.0  # 70000 - 65000
    assert analysis["savings_amount"] == 5000.0
    assert analysis["savings_percent"] == 7.1
    assert analysis["availability_scenario"] == "BOTH_IN_STOCK"
    assert "Flipkart is Cheaper" in analysis["deal_badge"]

def test_amazon_cheaper_when_both_in_stock():
    amz = create_sample_product("amazon", 50000.0, StockStatus.IN_STOCK)
    fpk = create_sample_product("flipkart", 55000.0, StockStatus.IN_STOCK)

    analysis = ComparisonAnalyzer.analyze(amz, fpk, "Test Phone")

    assert analysis["cheaper_platform"] == "amazon"
    assert analysis["price_diff"] == -5000.0
    assert analysis["savings_amount"] == 5000.0
    assert analysis["availability_scenario"] == "BOTH_IN_STOCK"
    assert "Amazon is Cheaper" in analysis["deal_badge"]

def test_stock_handling_only_amazon_in_stock():
    amz = create_sample_product("amazon", 60000.0, StockStatus.IN_STOCK)
    fpk = create_sample_product("flipkart", 58000.0, StockStatus.OUT_OF_STOCK)

    analysis = ComparisonAnalyzer.analyze(amz, fpk, "Test Phone")

    assert analysis["availability_scenario"] == "AMAZON_ONLY_IN_STOCK"
    assert analysis["cheaper_platform"] == "amazon"
    assert "Amazon In Stock" in analysis["deal_badge"]

def test_stock_handling_only_flipkart_in_stock():
    amz = create_sample_product("amazon", 60000.0, StockStatus.CURRENTLY_UNAVAILABLE)
    fpk = create_sample_product("flipkart", 59000.0, StockStatus.IN_STOCK)

    analysis = ComparisonAnalyzer.analyze(amz, fpk, "Test Phone")

    assert analysis["availability_scenario"] == "FLIPKART_ONLY_IN_STOCK"
    assert analysis["cheaper_platform"] == "flipkart"
    assert "Flipkart In Stock" in analysis["deal_badge"]

def test_both_out_of_stock():
    amz = create_sample_product("amazon", 45000.0, StockStatus.OUT_OF_STOCK)
    fpk = create_sample_product("flipkart", 44000.0, StockStatus.OUT_OF_STOCK)

    analysis = ComparisonAnalyzer.analyze(amz, fpk, "Test Phone")

    assert analysis["availability_scenario"] == "BOTH_OUT_OF_STOCK"
    assert analysis["deal_badge"] == "Out of Stock"
