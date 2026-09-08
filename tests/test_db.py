"""
Unit Tests for Database Layer
"""

import sqlite3
import pytest
from pathlib import Path
from app.database import db

def test_db_init_and_operations(tmp_path, monkeypatch):
    # Use temporary database file for test isolation
    test_db = tmp_path / "test_phones.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)

    # Initialize tables
    db.init_db()
    assert test_db.exists()

    # Insert Product
    prod_id = db.get_or_create_product("Apple iPhone 15 128GB", "Apple", "iPhone 15", "128GB")
    assert prod_id > 0

    # Ensure idempotency
    same_id = db.get_or_create_product("Apple iPhone 15 128GB")
    assert same_id == prod_id

    # Insert Price Records
    amz_rec = db.insert_price_record(
        product_id=prod_id,
        platform="amazon",
        title="Apple iPhone 15 (128GB) - Black",
        price=70999.0,
        mrp=79900.0,
        discount_percent=11.0,
        stock_status="IN_STOCK",
        rating=4.5,
        reviews_count=2000,
        product_url="https://amazon.in/dp/xyz",
        image_url="https://image.com/amz.jpg"
    )
    assert amz_rec > 0

    fpk_rec = db.insert_price_record(
        product_id=prod_id,
        platform="flipkart",
        title="Apple iPhone 15 (Black, 128 GB)",
        price=65999.0,
        mrp=79900.0,
        discount_percent=17.0,
        stock_status="IN_STOCK",
        rating=4.6,
        reviews_count=8000,
        product_url="https://flipkart.com/xyz",
        image_url="https://image.com/fpk.jpg"
    )
    assert fpk_rec > 0

    # Save Comparison Log
    log_id = db.save_comparison_record(
        query="iPhone 15",
        product_name="Apple iPhone 15 128GB",
        amazon_price=70999.0,
        flipkart_price=65999.0,
        price_diff=5000.0,
        savings_amount=5000.0,
        cheaper_platform="flipkart",
        amazon_stock="IN_STOCK",
        flipkart_stock="IN_STOCK"
    )
    assert log_id > 0

    # Fetch History
    history = db.get_price_history("iPhone 15")
    assert len(history["history"]) == 2

    # Fetch Analytics Summary
    summary = db.get_analytics_summary()
    assert summary["total_comparisons"] == 1
    assert summary["cheaper_counts"]["flipkart"] == 1
    assert summary["average_savings"] == 5000.0
    assert summary["in_stock_rate"] == 100.0
