"""
Flipkart India Smartphone Scraper
Uses curl_cffi to impersonate real Chrome TLS fingerprints and bypass bot detection.
Falls back to seed catalog on blocking. NEVER synthesizes fake prices.

Flipkart frequently changes CSS class names, so cards and prices are located
structurally (product-page links, image alt text, "₹" amounts) rather than by class.
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

    def _stock_from_text(self, text: str) -> tuple[StockStatus, str]:
        t = text.lower()
        if "out of stock" in t or "sold out" in t:
            return StockStatus.OUT_OF_STOCK, "Out of Stock on Flipkart"
        if "currently unavailable" in t or "temporarily unavailable" in t:
            return StockStatus.CURRENTLY_UNAVAILABLE, "Currently Unavailable on Flipkart"
        if "coming soon" in t:
            return StockStatus.CURRENTLY_UNAVAILABLE, "Coming Soon on Flipkart"
        return StockStatus.IN_STOCK, "In Stock ✓ Flipkart Assured"

    # Price text like "₹59,900" or "₹1,34,900" — nothing else in the element
    _PRICE_TEXT_RE = re.compile(r"^₹\s?[\d,]+$")

    def _find_cards(self, soup) -> list:
        """
        Locate product cards. Flipkart renames its CSS classes every few months,
        so cards are found structurally: each result is an <a> linking to a
        product page (/p/itm...) that holds a titled <img>.
        """
        cards = []
        seen = set()
        for a in soup.select('a[href*="/p/itm"]'):
            if not a.select_one("img[alt]"):
                continue
            href = a.get("href", "").split("?")[0]
            if href in seen:
                continue
            seen.add(href)
            cards.append(a)
        return cards

    def _price_elements(self, card) -> list:
        """Leaf elements whose entire text is a single rupee amount."""
        return [
            el for el in card.find_all(["div", "span"])
            if not el.find(["div", "span"])
            and self._PRICE_TEXT_RE.match(el.get_text(strip=True))
        ]

    def _parse_card(self, card, search_url: str) -> Optional[ProductData]:
        img_el = card.select_one("img[alt]")
        title = img_el.get("alt", "").strip() if img_el else ""
        if not title:
            return None

        tl = title.lower()
        if any(kw in tl for kw in ["case", "cover", "tempered", "screen protector",
                                    "cable", "pouch", "charger", "skin", "bumper",
                                    "back panel", "display combo"]):
            return None

        # First standalone ₹ amount is the selling price. The MRP (struck-through)
        # sits in the same container; exchange/bank offers ("Upto ₹42,800 Off on
        # Exchange") live in a different container and must be ignored.
        price, mrp = None, None
        price_els = self._price_elements(card)
        if price_els:
            price = self._clean_price(price_els[0].get_text())
            for el in price_els[1:]:
                if el.parent is price_els[0].parent:
                    mrp = self._clean_price(el.get_text())
                    break
        if mrp and price and mrp < price:
            mrp = None

        card_text = card.get_text(" ", strip=True)

        rating = None
        for el in card.find_all(["div", "span"]):
            if not el.find(["div", "span"]) and re.fullmatch(r"[1-5]\.\d", el.get_text(strip=True)):
                rating = float(el.get_text(strip=True))
                break

        reviews_count = None
        m = re.search(r"([\d,]+)\s*Ratings", card_text)
        if m:
            reviews_count = int(m.group(1).replace(",", ""))

        stock_status, stock_msg = self._stock_from_text(card_text)
        if price is None:
            stock_status = StockStatus.OUT_OF_STOCK
            stock_msg = "Price not listed — may be out of stock"

        discount_pct = None
        if price and mrp and mrp > price:
            discount_pct = round(((mrp - price) / mrp) * 100, 1)

        href = card.get("href", "")
        product_url = (
            f"{self.base_url}{href.split('?')[0]}" if href.startswith("/")
            else (href if href.startswith("http") else search_url)
        )

        image_url = img_el.get("data-src") or img_el.get("src") or None
        if image_url and ("placeholder" in image_url or "spinner" in image_url
                          or image_url.startswith("data:")):
            image_url = None
        if image_url:
            # Request a larger rendition than the 312px search thumbnail
            image_url = re.sub(r"/image/\d+/\d+/", "/image/832/832/", image_url)

        return ProductData(
            platform="flipkart",
            title=title,
            price=price,
            mrp=mrp or price,
            discount_percent=discount_pct,
            stock_status=stock_status,
            stock_message=stock_msg,
            rating=rating,
            reviews_count=reviews_count,
            product_url=product_url,
            image_url=image_url,
        )

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
                for card in self._find_cards(soup)[:12]:
                    product = self._parse_card(card, search_url)
                    if product:
                        results.append(product)

        except Exception:
            pass

        if not results:
            fallback = get_fallback_product(query, "flipkart")
            if fallback:
                results.append(fallback)

        return results
