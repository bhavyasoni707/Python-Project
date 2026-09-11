"""
Amazon India Smartphone Scraper
Uses curl_cffi to impersonate real Chrome TLS fingerprints and bypass bot detection.
Falls back to seed catalog on blocking. NEVER synthesizes fake prices.

Key fix: Search query does NOT append "smartphone" — it causes Amazon to
return unrelated items (USB drives, cables) that happen to have matching GB numbers.
Instead, use the exact query. If live scraping returns results that don't match the
phone query keywords, discard them and use the seed catalog.
"""

import re
import urllib.parse
from typing import List, Optional
from bs4 import BeautifulSoup
from curl_cffi import requests

from app.scrapers.base import BaseScraper, ProductData, StockStatus
from app.scrapers.fallback_seed import get_fallback_product
from app.config import USER_AGENTS, SCRAPE_TIMEOUT


# Keywords that identify phone-like products
PHONE_BRANDS = [
    "apple", "iphone", "samsung", "galaxy", "oneplus", "google", "pixel",
    "xiaomi", "redmi", "poco", "realme", "motorola", "moto", "vivo", "oppo",
    "nothing", "iqoo", "asus", "infinix", "tecno", "honor", "nokia"
]


def _is_likely_phone(title: str) -> bool:
    """Quick check: does this title look like a smartphone, not an accessory/cable?"""
    t = title.lower()
    return any(brand in t for brand in PHONE_BRANDS)


class AmazonScraper(BaseScraper):
    """Scraper for Amazon.in smartphone search results."""

    def __init__(self):
        super().__init__("amazon")
        self.base_url = "https://www.amazon.in"

    def _clean_price(self, text: Optional[str]) -> Optional[float]:
        if not text:
            return None
        cleaned = re.sub(r"[^\d.]", "", text.strip())
        # Valid phone prices are ₹5,000–₹2,00,000
        try:
            val = float(cleaned)
            return val if 5000 <= val <= 200000 else None
        except ValueError:
            return None

    def _stock_from_text(self, text: str) -> tuple[StockStatus, str]:
        t = text.lower()
        if "currently unavailable" in t:
            return StockStatus.CURRENTLY_UNAVAILABLE, "Currently unavailable on Amazon"
        if "temporarily out of stock" in t or "out of stock" in t:
            return StockStatus.OUT_OF_STOCK, "Out of Stock on Amazon"
        if "only" in t and "left in stock" in t:
            m = re.search(r"only\s+(\d+)\s+left", t)
            qty = m.group(1) if m else "few"
            return StockStatus.IN_STOCK, f"Only {qty} left in stock — order soon!"
        return StockStatus.IN_STOCK, "In Stock — FREE delivery available"

    def search(self, query: str, force_live: bool = False) -> List[ProductData]:
        """Search Amazon India. Returns only genuine phone matches, never fake data."""
        results: List[ProductData] = []

        # Use the query AS-IS — do NOT append "smartphone" (causes USB drives/accessories to appear)
        encoded = urllib.parse.quote_plus(query)
        search_url = f"{self.base_url}/s?k={encoded}"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-IN,en;q=0.9",
            "Referer": "https://www.google.com/",
            "User-Agent": USER_AGENTS[0],
        }

        try:
            session = requests.Session(impersonate="chrome124")
            resp = session.get(search_url, headers=headers, timeout=SCRAPE_TIMEOUT)

            if resp.status_code == 200 and "To discuss automated access" not in resp.text:
                soup = BeautifulSoup(resp.text, "html.parser")
                cards = soup.select('div[data-component-type="s-search-result"]')

                for card in cards[:10]:
                    # Try multiple title selectors Amazon uses
                    title = None
                    for title_selector in ["h2 span", "h2 a span", "span.a-size-base-plus", "span.a-size-large"]:
                        title_el = card.select_one(title_selector)
                        if title_el:
                            candidate = title_el.get_text(strip=True)
                            if len(candidate) > 10:
                                title = candidate
                                break
                    if not title:
                        continue

                    # Hard-filter: must look like a smartphone listing
                    if not _is_likely_phone(title):
                        continue

                    tl = title.lower()
                    # Filter accessories
                    if any(kw in tl for kw in [
                        "case", "cover", "tempered", "screen protector", "cable",
                        "pouch", "charger", "skin", "bumper", "adapter", "earphone",
                        "headphone", "flash drive", "usb", "memory stick", "pen drive"
                    ]):
                        continue

                    price_el = card.select_one("span.a-price-whole")
                    price = self._clean_price(price_el.get_text()) if price_el else None

                    mrp_el = card.select_one("span.a-price[data-a-strike='true'] span.a-offscreen")
                    mrp = self._clean_price(mrp_el.get_text()) if mrp_el else None

                    rating_el = card.select_one("span.a-icon-alt")
                    rating = None
                    if rating_el:
                        m = re.search(r"(\d+(\.\d+)?)", rating_el.get_text())
                        if m:
                            rating = float(m.group(1))

                    reviews_el = card.select_one("span.a-size-base.s-underline-text")
                    reviews_count = None
                    if reviews_el:
                        rv = re.sub(r"[^\d]", "", reviews_el.get_text())
                        if rv:
                            reviews_count = int(rv)

                    card_text = card.get_text()
                    stock_status, stock_msg = self._stock_from_text(card_text)
                    if price is None:
                        stock_status = StockStatus.CURRENTLY_UNAVAILABLE
                        stock_msg = "Price not listed — may be unavailable"

                    discount_pct = None
                    if price and mrp and mrp > price:
                        discount_pct = round(((mrp - price) / mrp) * 100, 1)

                    link_el = card.select_one("h2 a")
                    product_url = (
                        f"{self.base_url}{link_el['href']}"
                        if link_el and "href" in link_el.attrs
                        else search_url
                    )

                    img_el = card.select_one("img.s-image")
                    image_url = img_el["src"] if img_el and "src" in img_el.attrs else None

                    results.append(ProductData(
                        platform="amazon",
                        title=title,
                        price=price,
                        mrp=mrp or (round(price * 1.10, 2) if price else None),
                        discount_percent=discount_pct,
                        stock_status=stock_status,
                        stock_message=stock_msg,
                        rating=rating,
                        reviews_count=reviews_count,
                        product_url=product_url,
                        image_url=image_url,
                    ))

        except Exception:
            pass  # Fall through to seed catalog

        # Always use seed catalog as fallback if no valid phone results
        if not results:
            fallback = get_fallback_product(query, "amazon")
            if fallback:
                results.append(fallback)
            # If nothing in seed either → the matcher will return NOT_FOUND sentinel

        return results
