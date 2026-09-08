"""
Database Data Models and PostgreSQL Schema Definitions
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# PostgreSQL-compatible schema (SERIAL, TIMESTAMP WITH TIME ZONE, ON DELETE CASCADE)
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    canonical_name TEXT NOT NULL UNIQUE,
    brand TEXT,
    model TEXT,
    storage TEXT,
    ram TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    title TEXT,
    price NUMERIC(12, 2),
    mrp NUMERIC(12, 2),
    discount_percent NUMERIC(5, 2),
    stock_status TEXT NOT NULL,
    rating NUMERIC(3, 2),
    reviews_count INTEGER,
    product_url TEXT,
    image_url TEXT,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS comparison_logs (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    product_name TEXT NOT NULL,
    amazon_price NUMERIC(12, 2),
    flipkart_price NUMERIC(12, 2),
    price_diff NUMERIC(12, 2),
    savings_amount NUMERIC(12, 2),
    cheaper_platform TEXT,
    amazon_stock TEXT,
    flipkart_stock TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_price_history_prod ON price_history(product_id);
CREATE INDEX IF NOT EXISTS idx_price_history_time ON price_history(recorded_at);
CREATE INDEX IF NOT EXISTS idx_comparison_logs_time ON comparison_logs(created_at);
"""


@dataclass
class ProductRecord:
    id: Optional[int]
    canonical_name: str
    brand: Optional[str]
    model: Optional[str]
    storage: Optional[str]
    ram: Optional[str]
    created_at: Optional[datetime] = None


@dataclass
class PriceRecord:
    id: Optional[int]
    product_id: int
    platform: str
    title: str
    price: Optional[float]
    mrp: Optional[float]
    discount_percent: Optional[float]
    stock_status: str
    rating: Optional[float]
    reviews_count: Optional[int]
    product_url: Optional[str]
    image_url: Optional[str]
    recorded_at: Optional[datetime] = None
