"""
PostgreSQL / Neon Database Operations Layer
Uses psycopg2 to connect via DATABASE_URL environment variable.
No local SQL installation required — the database runs on Neon's cloud servers.
"""

import psycopg2
import psycopg2.extras
from typing import List, Dict, Any, Optional
from app.config import DATABASE_URL
from app.database.models import SCHEMA_SQL


def get_db_connection() -> psycopg2.extensions.connection:
    """
    Connect to Neon PostgreSQL using the DATABASE_URL environment variable.
    psycopg2 handles the TCP connection to Neon's cloud servers automatically.
    """
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def init_db():
    """
    Create all tables and indexes in Neon PostgreSQL if they don't exist.
    Safe to call on every startup (uses IF NOT EXISTS).
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Execute each statement separately for psycopg2 compatibility
            for statement in SCHEMA_SQL.strip().split(";"):
                stmt = statement.strip()
                if stmt:
                    cur.execute(stmt)
        conn.commit()
    finally:
        conn.close()


def get_or_create_product(name: str, brand: Optional[str] = None, model: Optional[str] = None,
                          storage: Optional[str] = None, ram: Optional[str] = None) -> int:
    """Fetch existing product ID or insert a new canonical product record."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM products WHERE canonical_name = %s", (name,))
            row = cur.fetchone()
            if row:
                return row["id"]

            cur.execute(
                """
                INSERT INTO products (canonical_name, brand, model, storage, ram)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (name, brand, model, storage, ram)
            )
            new_id = cur.fetchone()["id"]
            conn.commit()
            return new_id
    finally:
        conn.close()


def insert_price_record(product_id: int, platform: str, title: str, price: Optional[float],
                        mrp: Optional[float], discount_percent: Optional[float],
                        stock_status: str, rating: Optional[float], reviews_count: Optional[int],
                        product_url: Optional[str], image_url: Optional[str]) -> int:
    """Insert a price snapshot observation for Amazon or Flipkart."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO price_history
                  (product_id, platform, title, price, mrp, discount_percent,
                   stock_status, rating, reviews_count, product_url, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (product_id, platform.lower(), title, price, mrp, discount_percent,
                 stock_status, rating, reviews_count, product_url, image_url)
            )
            new_id = cur.fetchone()["id"]
            conn.commit()
            return new_id
    finally:
        conn.close()


def save_comparison_record(query: str, product_name: str, amazon_price: Optional[float],
                           flipkart_price: Optional[float], price_diff: Optional[float],
                           savings_amount: Optional[float], cheaper_platform: str,
                           amazon_stock: str, flipkart_stock: str) -> int:
    """Log a full comparison run result into the comparison_logs table."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO comparison_logs
                  (query, product_name, amazon_price, flipkart_price, price_diff,
                   savings_amount, cheaper_platform, amazon_stock, flipkart_stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (query, product_name, amazon_price, flipkart_price, price_diff,
                 savings_amount, cheaper_platform, amazon_stock, flipkart_stock)
            )
            new_id = cur.fetchone()["id"]
            conn.commit()
            return new_id
    finally:
        conn.close()


def get_price_history(product_name: str) -> Dict[str, Any]:
    """Retrieve historical price timeline for a product from both platforms."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, canonical_name FROM products WHERE canonical_name ILIKE %s ORDER BY id DESC LIMIT 1",
                (f"%{product_name}%",)
            )
            prod = cur.fetchone()
            if not prod:
                return {"canonical_name": product_name, "history": []}

            cur.execute(
                """
                SELECT platform, price, mrp, stock_status, rating,
                       recorded_at::text as recorded_at
                FROM price_history
                WHERE product_id = %s
                ORDER BY recorded_at ASC
                LIMIT 50
                """,
                (prod["id"],)
            )
            rows = cur.fetchall()
            return {
                "canonical_name": prod["canonical_name"],
                "history": [dict(r) for r in rows]
            }
    finally:
        conn.close()


def get_all_products() -> List[Dict[str, Any]]:
    """Fetch all canonical products tracked in the database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products ORDER BY id DESC")
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def get_recent_comparisons(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch most recent comparison search log entries."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, query, product_name, amazon_price, flipkart_price,
                       price_diff, savings_amount, cheaper_platform,
                       amazon_stock, flipkart_stock,
                       created_at::text as created_at
                FROM comparison_logs
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,)
            )
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def get_analytics_summary() -> Dict[str, Any]:
    """Compute aggregate KPI statistics across all comparison records."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total FROM comparison_logs")
            total_runs = cur.fetchone()["total"]

            cur.execute(
                """
                SELECT cheaper_platform, COUNT(*) as count
                FROM comparison_logs
                WHERE cheaper_platform IN ('amazon', 'flipkart', 'equal')
                GROUP BY cheaper_platform
                """
            )
            platform_counts = {r["cheaper_platform"]: r["count"] for r in cur.fetchall()}

            cur.execute(
                """
                SELECT ROUND(AVG(savings_amount)::numeric, 2) as avg_savings,
                       ROUND(MAX(savings_amount)::numeric, 2) as max_savings
                FROM comparison_logs
                WHERE savings_amount > 0
                """
            )
            savings_row = cur.fetchone()
            avg_savings = float(savings_row["avg_savings"] or 0)
            max_savings = float(savings_row["max_savings"] or 0)

            cur.execute(
                """
                SELECT
                    SUM(CASE WHEN stock_status = 'IN_STOCK' THEN 1 ELSE 0 END) as in_stock_count,
                    COUNT(*) as total_checks
                FROM price_history
                """
            )
            stock_row = cur.fetchone()
            total_checks = stock_row["total_checks"] or 1
            in_stock_rate = round(((stock_row["in_stock_count"] or 0) / total_checks) * 100, 1)

            return {
                "total_comparisons": total_runs,
                "cheaper_counts": {
                    "amazon": platform_counts.get("amazon", 0),
                    "flipkart": platform_counts.get("flipkart", 0),
                    "equal": platform_counts.get("equal", 0)
                },
                "average_savings": avg_savings,
                "max_savings": max_savings,
                "in_stock_rate": in_stock_rate
            }
    finally:
        conn.close()
