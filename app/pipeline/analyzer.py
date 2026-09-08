"""
Price Difference & Stock Availability Analyzer
Analyzes pricing discrepancies, identifies best deals, and evaluates
stock availability across Amazon and Flipkart.
"""

from typing import Optional, Dict, Any
from app.scrapers.base import ProductData, StockStatus

class ComparisonAnalyzer:
    """Analyzes prices and stock availability between Amazon and Flipkart."""

    @staticmethod
    def analyze(
        amazon: Optional[ProductData],
        flipkart: Optional[ProductData],
        query: str
    ) -> Dict[str, Any]:
        """Perform comprehensive comparative data analysis."""

        # 1. Stock Status Evaluations
        amz_in_stock = (amazon is not None) and (amazon.stock_status == StockStatus.IN_STOCK)
        fpk_in_stock = (flipkart is not None) and (flipkart.stock_status == StockStatus.IN_STOCK)

        amz_price = amazon.price if amazon and amazon.price else None
        fpk_price = flipkart.price if flipkart and flipkart.price else None

        # Stock Scenarios:
        # Case 1: Both In Stock
        # Case 2: Only Amazon In Stock (Flipkart OOS or unavailable)
        # Case 3: Only Flipkart In Stock (Amazon OOS or unavailable)
        # Case 4: Both Out of Stock
        # Case 5: Missing / Not found on one or both

        if amz_in_stock and fpk_in_stock:
            availability_scenario = "BOTH_IN_STOCK"
            stock_summary = "In Stock on both Amazon and Flipkart"
        elif amz_in_stock and not fpk_in_stock:
            availability_scenario = "AMAZON_ONLY_IN_STOCK"
            stock_summary = f"Available only on Amazon ({flipkart.stock_status.value if flipkart else 'Not Found'} on Flipkart)"
        elif not amz_in_stock and fpk_in_stock:
            availability_scenario = "FLIPKART_ONLY_IN_STOCK"
            stock_summary = f"Available only on Flipkart ({amazon.stock_status.value if amazon else 'Not Found'} on Amazon)"
        elif amazon and flipkart:
            availability_scenario = "BOTH_OUT_OF_STOCK"
            stock_summary = "Out of Stock / Unavailable on both Amazon and Flipkart"
        else:
            availability_scenario = "NOT_FOUND"
            stock_summary = "Product not found on one or both platforms"

        # 2. Price Difference & Winner Determination
        price_diff = None
        cheaper_platform = "n/a"
        savings_amount = 0.0
        savings_percent = 0.0
        deal_badge = ""
        deal_summary = ""

        if amz_price is not None and fpk_price is not None:
            # Absolute price difference: Amazon - Flipkart
            diff = amz_price - fpk_price
            price_diff = round(diff, 2)
            abs_diff = round(abs(diff), 2)

            # Check stock logic for deal recommendation
            if amz_in_stock and fpk_in_stock:
                if diff > 0:
                    # Flipkart is cheaper
                    cheaper_platform = "flipkart"
                    savings_amount = abs_diff
                    savings_percent = round((abs_diff / amz_price) * 100, 1)
                    deal_badge = "Flipkart is Cheaper"
                    deal_summary = f"Flipkart is cheaper by ₹{abs_diff:,.0f} ({savings_percent}% less than Amazon)!"
                elif diff < 0:
                    # Amazon is cheaper
                    cheaper_platform = "amazon"
                    savings_amount = abs_diff
                    savings_percent = round((abs_diff / fpk_price) * 100, 1)
                    deal_badge = "Amazon is Cheaper"
                    deal_summary = f"Amazon is cheaper by ₹{abs_diff:,.0f} ({savings_percent}% less than Flipkart)!"
                else:
                    cheaper_platform = "equal"
                    deal_badge = "Equal Price"
                    deal_summary = "Both Amazon and Flipkart offer the exact same price."
            elif amz_in_stock and not fpk_in_stock:
                cheaper_platform = "amazon"
                savings_amount = 0.0
                deal_badge = "Amazon In Stock"
                deal_summary = f"Only Amazon has stock! Flipkart is currently {flipkart.stock_message if flipkart else 'Unavailable'}."
            elif fpk_in_stock and not amz_in_stock:
                cheaper_platform = "flipkart"
                savings_amount = 0.0
                deal_badge = "Flipkart In Stock"
                deal_summary = f"Only Flipkart has stock! Amazon is currently {amazon.stock_message if amazon else 'Unavailable'}."
            else:
                cheaper_platform = "n/a"
                deal_badge = "Out of Stock"
                deal_summary = "Product is currently out of stock or unavailable on both platforms."
        elif amz_price is not None and amz_in_stock:
            cheaper_platform = "amazon"
            deal_badge = "Available on Amazon"
            deal_summary = "Only listed with active price on Amazon."
        elif fpk_price is not None and fpk_in_stock:
            cheaper_platform = "flipkart"
            deal_badge = "Available on Flipkart"
            deal_summary = "Only listed with active price on Flipkart."
        else:
            deal_badge = "Price Unavailable"
            deal_summary = "Unable to compare prices due to stock or listing unavailability."

        # 3. Canonical Phone Name Synthesis
        canonical_name = (
            amazon.title if (amazon and len(amazon.title) > 5)
            else (flipkart.title if (flipkart and len(flipkart.title) > 5) else query.title())
        )

        return {
            "query": query,
            "canonical_name": canonical_name,
            "availability_scenario": availability_scenario,
            "stock_summary": stock_summary,
            "amazon_price": amz_price,
            "flipkart_price": fpk_price,
            "price_diff": price_diff,
            "abs_price_diff": round(abs(price_diff), 2) if price_diff is not None else 0.0,
            "cheaper_platform": cheaper_platform,
            "savings_amount": savings_amount,
            "savings_percent": savings_percent,
            "deal_badge": deal_badge,
            "deal_summary": deal_summary,
            "amazon_stock": amazon.stock_status.value if amazon else "NOT_FOUND",
            "amazon_stock_msg": amazon.stock_message if amazon else "Not found on Amazon",
            "flipkart_stock": flipkart.stock_status.value if flipkart else "NOT_FOUND",
            "flipkart_stock_msg": flipkart.stock_message if flipkart else "Not found on Flipkart",
            "rating_comparison": {
                "amazon_rating": amazon.rating if amazon else None,
                "flipkart_rating": flipkart.rating if flipkart else None,
                "amazon_reviews": amazon.reviews_count if amazon else None,
                "flipkart_reviews": flipkart.reviews_count if flipkart else None,
            }
        }
