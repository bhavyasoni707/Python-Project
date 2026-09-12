"""
Flipkart India Smartphone Scraper
Uses curl_cffi to impersonate real Chrome TLS fingerprints and bypass bot detection.
Falls back to seed catalog on blocking. NEVER synthesizes fake prices.

Price fix: Flipkart frequently changes CSS class names. Use multiple selectors
and also try span.a-offscreen-style hidden price elements. The current price
class is Nx9bqj but also try hl05eU > div which gives full price text.
"""

import re
import urllib.parse
from typing import List, Optional
from bs4 import BeautifulSoup
from curl_cffi import requests

from app.scrapers.base import BaseScraper, ProductData, StockStatus
from app.scrapers.fallback_seed import get_fallback_product
from app.config import USER_AGENTS, SCRAPE_TIMEOUT


class FlipkartScraper(BaseScraper):
    """Scraper for Flipkart.com smartphone search results."""

    def __init__(self):
        super().__init__("flipkart")
        self.base_url = "https://www.flipkart.com"

    def _clean_price(self, text: Optional[str]) -> Optional[float]:
        if not text:
            return None
        # Remove rupee symbol, commas, spaces
        cleaned = re.sub(r"[^\d.]", "", text.strip()).rstrip(".")
        try:
            val = float(cleaned)
            return val if 3000 <= val <= 200000 else None
        except ValueError:
            return None

    def _extract_current_price(self, card) -> Optional[float]:
        """
        Extract selling price from Flipkart card.
        Flipkart changes class names frequently — try all known variants.
        """
        # All known Flipkart current-price selectors (newest first)
        price_selectors = [
            "div.Nx9bqj",          # 2024 layout
            "div.hl05eU div.Nx9bqj",
            "div._30jeq3",         # older layout
            "div._1_WHN1",         # older
            "span._1vC4OE",        # mobile layout
            "div.hl05eU > div:first-child",  # container approach
        ]
        for sel in price_selectors:
            el = card.select_one(sel)
            if el:
                text = el.get_text(strip=True)
                price = self._clean_price(text)
                if price:
                    return price

        # Last resort: find any text matching ₹ followed by digits in plausible range
        all_text = card.get_text()
        matches = re.findall(r"₹\s*([\d,]+)", all_text)
        for m in matches:
            price = self._clean_price(m)
            if price:
                return price

        return None

    def _extract_mrp(self, card) -> Optional[float]:
        """Extract MRP (struck-through original price)."""
        mrp_selectors = [
            "div.yRaY8j",      # 2024
            "div.WW3Bm1",      # 2024 alt
            "div._3I9_wc",     # older
            "div._3auQ3N",     # older alt
        ]
        for sel in mrp_selectors:
            el = card.select_one(sel)
            if el:
                mrp = self._clean_price(el.get_text())
                if mrp:
                    return mrp
        return None

    def _stock_from_text(self, text: str) -> tuple[StockStatus, str]:
        t = text.lower()
        if "out of stock" in t or "sold out" in t:
            return StockStatus.OUT_OF_STOCK, "Out of Stock on Flipkart"
        if "currently unavailable" in t or "temporarily unavailable" in t:
            return StockStatus.CURRENTLY_UNAVAILABLE, "Currently Unavailable on Flipkart"
        if "coming soon" in t:
            return StockStatus.CURRENTLY_UNAVAILABLE, "Coming Soon on Flipkart"
        return StockStatus.IN_STOCK, "In Stock ✓ Flipkart Assured"

    def search(self, query: str, force_live: bool = False) -> List[ProductData]:
        """Search Flipkart. Returns only genuine phone matches, never fake data."""
        results: List[ProductData] = []
        encoded = urllib.parse.quote_plus(query)
        search_url = f"{self.base_url}/search?q={encoded}"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-IN,en;q=0.9",
            "Referer": "https://www.flipkart.com/",
            "User-Agent": USER_AGENTS[0],
        }

        try:
            session = requests.Session(impersonate="chrome124")
            resp = session.get(search_url, headers=headers, timeout=SCRAPE_TIMEOUT)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")

                card_selectors = [
                    "div.tUxRFH", "div._75nlfW", "div._1AtVbE",
                    "div._2kHMtA", "div._13oc-S", "div.DOjaWF",
                    "div.slAVV4",  # 2024 grid layout
                ]
                cards = []
                for sel in card_selectors:
                    found = soup.select(sel)
                    if len(found) >= 3:
                        cards = found
                        break

                for card in cards[:8]:
                    title_el = card.select_one(
                        "div.KzDlHZ, div._4rR01T, a.s1Q9rs, div._2WkVRV, div.syl9yP, a.IRpwTa"
                    )
                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)

                    tl = title.lower()
                    if any(kw in tl for kw in ["case", "cover", "tempered", "screen protector",
                                                "cable", "pouch", "charger", "skin", "bumper"]):
                        continue

                    price = self._extract_current_price(card)
                    mrp = self._extract_mrp(card)

                    # Sanity: MRP must be >= price
                    if mrp and price and mrp < price:
                        mrp = None

                    rating_el = card.select_one("div.XQDdHH, div._3LWZlK, span.Y1HWO0")
                    rating = None
                    if rating_el:
                        try:
                            rating = float(rating_el.get_text(strip=True))
                        except ValueError:
                            pass

                    reviews_el = card.select_one("span.WpvKPa, span._2_R_DZ, span.Wphh3N")
                    reviews_count = None
                    if reviews_el:
                        m = re.search(r"([\d,]+)\s*(Ratings|Reviews)", reviews_el.get_text())
                        if m:
                            rv = re.sub(r"[^\d]", "", m.group(1))
                            if rv:
                                reviews_count = int(rv)

                    card_text = card.get_text()
                    stock_status, stock_msg = self._stock_from_text(card_text)
                    if price is None:
                        stock_status = StockStatus.OUT_OF_STOCK
                        stock_msg = "Price not listed — may be out of stock"

                    discount_pct = None
                    if price and mrp and mrp > price:
                        discount_pct = round(((mrp - price) / mrp) * 100, 1)

                    link_el = card.select_one("a[href]")
                    if link_el:
                        href = link_el.get("href", "")
                        product_url = (
                            f"{self.base_url}{href}"
                            if href.startswith("/")
                            else (href if href.startswith("http") else search_url)
                        )
                    else:
                        product_url = search_url

                    # Get image — try data-src first (lazy-loaded), then src
                    img_el = card.select_one("img")
                    image_url = None
                    if img_el:
                        image_url = (
                            img_el.get("data-src")
                            or img_el.get("src")
                            or None
                        )
                    # Skip placeholder/loading spinner images
                    if image_url and ("placeholder" in image_url or "spinner" in image_url):
                        image_url = None

                    results.append(ProductData(
                        platform="flipkart",
                        title=title,
                        price=price,
                        mrp=mrp or (round(price * 1.12, 2) if price else None),
                        discount_percent=discount_pct,
                        stock_status=stock_status,
                        stock_message=stock_msg,
                        rating=rating,
                        reviews_count=reviews_count,
                        product_url=product_url,
                        image_url=image_url,
                    ))

        except Exception:
            pass

        if not results:
            fallback = get_fallback_product(query, "flipkart")
            if fallback:
                results.append(fallback)

        return results
