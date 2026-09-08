"""
Master Comparison & Analytics Pipeline Orchestrator
Coordinates parallel scraping, fuzzy matching, stock checking,
price discrepancy analysis, and database persistence.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.scrapers.amazon import AmazonScraper
from app.scrapers.flipkart import FlipkartScraper
from app.scrapers.base import ProductData, StockStatus
from app.pipeline.matcher import SmartphoneMatcher
from app.pipeline.analyzer import ComparisonAnalyzer
from app.database.db import get_or_create_product, insert_price_record, save_comparison_record, get_price_history

class ComparisonPipeline:
    """End-to-end Pipeline for smartphone price comparison and analysis."""

    def __init__(self):
        self.amazon_scraper = AmazonScraper()
        self.flipkart_scraper = FlipkartScraper()

    def run(self, query: str, force_live: bool = False) -> Dict[str, Any]:
        """
        Execute the comparison pipeline for a query.
        Returns complete analysis payload along with step-by-step pipeline telemetry.
        """
        start_time = time.time()
        pipeline_telemetry: List[Dict[str, Any]] = []

        def log_stage(stage_id: int, name: str, status: str, details: str, duration_ms: float):
            pipeline_telemetry.append({
                "stage": stage_id,
                "name": name,
                "status": status,
                "details": details,
                "duration_ms": round(duration_ms, 1),
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
            })

        # --- Stage 1: Ingestion & Normalization ---
        s1_start = time.time()
        cleaned_query = query.strip()
        storage = SmartphoneMatcher.normalize_storage(cleaned_query)
        ram = SmartphoneMatcher.normalize_ram(cleaned_query)
        log_stage(
            stage_id=1,
            name="Query Normalization",
            status="SUCCESS",
            details=f"Query parsed: '{cleaned_query}' (Storage: {storage or 'N/A'}, RAM: {ram or 'N/A'})",
            duration_ms=(time.time() - s1_start) * 1000
        )

        # --- Stage 2: Concurrent Multi-Platform Scraping ---
        s2_start = time.time()
        amazon_results: List[ProductData] = []
        flipkart_results: List[ProductData] = []

        with ThreadPoolExecutor(max_workers=2) as executor:
            amz_future = executor.submit(self.amazon_scraper.search, cleaned_query, force_live)
            fpk_future = executor.submit(self.flipkart_scraper.search, cleaned_query, force_live)

            try:
                amazon_results = amz_future.result()
            except Exception as e:
                amazon_results = []

            try:
                flipkart_results = fpk_future.result()
            except Exception as e:
                flipkart_results = []

        log_stage(
            stage_id=2,
            name="Concurrent Scraping",
            status="SUCCESS",
            details=f"Scraped {len(amazon_results)} Amazon candidates, {len(flipkart_results)} Flipkart candidates",
            duration_ms=(time.time() - s2_start) * 1000
        )

        # --- Stage 3: Fuzzy Matching & Variant Alignment ---
        s3_start = time.time()
        matched_amz, matched_fpk, match_score = SmartphoneMatcher.match_best_pair(
            amazon_results, flipkart_results, cleaned_query
        )
        log_stage(
            stage_id=3,
            name="Fuzzy Variant Matching",
            status="SUCCESS",
            details=f"Variant alignment confidence: {match_score}% similarity",
            duration_ms=(time.time() - s3_start) * 1000
        )

        # --- Stage 4: Stock & Price Delta Analysis ---
        s4_start = time.time()
        analysis = ComparisonAnalyzer.analyze(matched_amz, matched_fpk, cleaned_query)
        log_stage(
            stage_id=4,
            name="Stock & Price Delta Analytics",
            status="SUCCESS",
            details=f"{analysis['deal_badge']} | Savings: ₹{analysis['savings_amount']:,.0f} | Stock: {analysis['availability_scenario']}",
            duration_ms=(time.time() - s4_start) * 1000
        )

        # --- Stage 5: Database Persistence & History Logging ---
        s5_start = time.time()
        product_id = get_or_create_product(
            name=analysis["canonical_name"],
            storage=storage,
            ram=ram
        )

        # Record Amazon observation
        if matched_amz:
            insert_price_record(
                product_id=product_id,
                platform="amazon",
                title=matched_amz.title,
                price=matched_amz.price,
                mrp=matched_amz.mrp,
                discount_percent=matched_amz.discount_percent,
                stock_status=matched_amz.stock_status.value,
                rating=matched_amz.rating,
                reviews_count=matched_amz.reviews_count,
                product_url=matched_amz.product_url,
                image_url=matched_amz.image_url
            )

        # Record Flipkart observation
        if matched_fpk:
            insert_price_record(
                product_id=product_id,
                platform="flipkart",
                title=matched_fpk.title,
                price=matched_fpk.price,
                mrp=matched_fpk.mrp,
                discount_percent=matched_fpk.discount_percent,
                stock_status=matched_fpk.stock_status.value,
                rating=matched_fpk.rating,
                reviews_count=matched_fpk.reviews_count,
                product_url=matched_fpk.product_url,
                image_url=matched_fpk.image_url
            )

        # Record Comparison Log
        save_comparison_record(
            query=cleaned_query,
            product_name=analysis["canonical_name"],
            amazon_price=analysis["amazon_price"],
            flipkart_price=analysis["flipkart_price"],
            price_diff=analysis["price_diff"],
            savings_amount=analysis["savings_amount"],
            cheaper_platform=analysis["cheaper_platform"],
            amazon_stock=analysis["amazon_stock"],
            flipkart_stock=analysis["flipkart_stock"]
        )

        # Fetch updated price history for chart rendering
        price_history = get_price_history(analysis["canonical_name"])

        log_stage(
            stage_id=5,
            name="Database Persistence",
            status="SUCCESS",
            details=f"Saved price snapshots and comparison log into SQLite (Product ID: {product_id})",
            duration_ms=(time.time() - s5_start) * 1000
        )

        total_execution_time = round((time.time() - start_time), 2)

        return {
            "success": True,
            "query": cleaned_query,
            "analysis": analysis,
            "match_confidence": match_score,
            "amazon": matched_amz.to_dict() if matched_amz else None,
            "flipkart": matched_fpk.to_dict() if matched_fpk else None,
            "price_history": price_history["history"],
            "pipeline_telemetry": pipeline_telemetry,
            "total_execution_time_sec": total_execution_time
        }
