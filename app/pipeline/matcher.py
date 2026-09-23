"""
Strict Smartphone Variant Matching Engine
Ensures we compare the EXACT same phone model and storage variant
between Amazon and Flipkart. No substitutions. No wrong phone matches.

Key principle: If a phone is NOT found on a platform → return NOT_FOUND.
NEVER fall back to a different phone model.
"""

import re
from typing import List, Optional, Tuple
from rapidfuzz import fuzz

from app.scrapers.base import ProductData, StockStatus
from app.config import FUZZY_MATCH_THRESHOLD


class SmartphoneMatcher:
    """Strictly matches and pairs smartphone listings from Amazon and Flipkart."""

    # Known storage sizes (in priority order)
    STORAGE_PATTERNS = [
        r"\b(1\s*TB|1TB)\b",
        r"\b(512\s*GB|512GB)\b",
        r"\b(256\s*GB|256GB)\b",
        r"\b(128\s*GB|128GB)\b",
        r"\b(64\s*GB|64GB)\b",
        r"\b(32\s*GB|32GB)\b",
    ]

    # Accessories to always filter out
    ACCESSORY_KEYWORDS = [
        "case", "cover", "tempered glass", "screen protector", "cable",
        "pouch", "charger", "adapter", "earphone", "headphone", "skin",
        "back cover", "flip cover", "wallet case", "bumper", "stylus",
        "stand", "holder", "mount", "powerbank", "power bank", "back panel",
        "display combo", "battery replacement"
    ]

    # Known brand names — used for brand-first filtering
    KNOWN_BRANDS = [
        "apple", "iphone",
        "samsung", "galaxy",
        "oneplus", "nord",
        "google", "pixel",
        "xiaomi", "redmi", "poco",
        "realme",
        "motorola", "moto",
        "vivo",
        "oppo",
        "nothing",
        "iqoo",
        "asus",
        "infinix",
        "tecno",
        "honor",
        "lava"
    ]

    @staticmethod
    def normalize_storage(text: str) -> Optional[str]:
        """
        Extract and normalize storage from text.
        Returns canonical form e.g. '128GB', '256GB', '1TB'.
        """
        tb_match = re.search(r"\b(\d+)\s*TB\b", text, re.IGNORECASE)
        if tb_match:
            return f"{tb_match.group(1)}TB"

        # GB — but ignore RAM mentions like "8GB RAM"
        gb_matches = re.findall(r"\b(\d+)\s*GB(?!\s*RAM)", text, re.IGNORECASE)
        if gb_matches:
            values = [int(x) for x in gb_matches]
            valid = [v for v in values if v in (16, 32, 64, 128, 256, 512)]
            if valid:
                return f"{max(valid)}GB"

        return None

    @staticmethod
    def normalize_ram(text: str) -> Optional[str]:
        """Extract RAM size, only when explicitly mentioned as RAM."""
        match = re.search(r"\b(\d+)\s*GB\s*RAM\b", text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}GB"
        return None

    @staticmethod
    def extract_model_keywords(query: str) -> List[str]:
        """
        Extract meaningful model keywords from a search query.
        e.g. 'Apple iPhone 15 Pro Max 256GB' → ['apple', 'iphone', '15', 'pro', 'max']

        CRITICAL: Keywords extracted here must ALL appear in a title for it to match.
        This prevents cross-model contamination.
        """
        # Normalize variations
        query = query.replace("+", " plus").replace("pro+", "pro plus")

        # Remove storage/RAM specs
        cleaned = re.sub(r"\b\d+\s*(GB|TB)\b", "", query, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bRAM\b", "", cleaned, flags=re.IGNORECASE)

        # Extract word tokens (include numbers — e.g. "15", "12", "S24")
        tokens = re.findall(r"\b[a-zA-Z0-9]+\b", cleaned)

        # Filter trivial words
        stopwords = {
            "the", "a", "an", "and", "or", "for", "of", "in", "with",
            "smartphone", "mobile", "phone", "5g", "4g", "india", "in",
            "buy", "best", "new", "latest", "official", "original"
        }
        # Single digits are kept: they are model numbers ("Pixel 8", "Nothing Phone 2")
        keywords = [t.lower() for t in tokens
                    if t.lower() not in stopwords and (len(t) > 1 or t.isdigit())]
        return keywords

    @staticmethod
    def is_accessory(title: str) -> bool:
        """Returns True if the title appears to be an accessory, not a phone."""
        title_lower = title.lower()
        return any(kw in title_lower for kw in SmartphoneMatcher.ACCESSORY_KEYWORDS)

    # Words that denote a different model tier. A title carrying one of these
    # that the query doesn't ask for is a different phone
    # (e.g. "iPhone 15 Plus" for "iPhone 15", "CMF Phone 2 Pro" for "Nothing Phone 2").
    VARIANT_WORDS = {"pro", "max", "plus", "ultra", "lite", "mini", "fe", "se",
                     "neo", "prime", "cmf", "fold", "flip", "edge"}

    @staticmethod
    def _tokens(text: str) -> List[str]:
        text = text.lower().replace("+", " plus ")
        return re.findall(r"[a-z0-9]+", text)

    @classmethod
    def title_matches_query(cls, title: str, query_keywords: List[str]) -> bool:
        """
        Returns True ONLY if ALL query keywords appear in the product title
        as whole words, and the title names no extra model tier.
        This is the core strict matching gate — prevents wrong phone matches.

        - '15' must be a whole word: it does not match '150' or '15e'
        - 'pro max' in query → title must contain BOTH 'pro' AND 'max'
        - 'iphone 15' does NOT match 'iPhone 15 Plus' / 'iPhone 15 Pro'
        """
        title_tokens = set(cls._tokens(title))
        if not all(kw in title_tokens for kw in query_keywords):
            return False
        extra_variants = (title_tokens & cls.VARIANT_WORDS) - set(query_keywords)
        return not extra_variants

    @classmethod
    def storage_matches(cls, title: str, query_storage: Optional[str]) -> bool:
        """
        If the query specifies a storage size, the title MUST contain it.
        Returns True if no storage in query, or if storage matches exactly.
        """
        if not query_storage:
            return True  # No storage constraint in query — anything goes
        title_storage = cls.normalize_storage(title)
        return title_storage == query_storage

    @classmethod
    def filter_candidates(
        cls,
        candidates: List[ProductData],
        query_keywords: List[str],
        query_storage: Optional[str]
    ) -> List[ProductData]:
        """
        Pre-filter scraped candidates to only those matching ALL query keywords
        AND storage variant. Returns empty list if nothing matches.

        Empty list means NOT_FOUND for that platform — do NOT substitute.
        """
        filtered = []
        for product in candidates:
            if cls.is_accessory(product.title):
                continue
            if not cls.title_matches_query(product.title, query_keywords):
                continue
            if not cls.storage_matches(product.title, query_storage):
                continue
            filtered.append(product)
        # A buyable listing of the same model/storage beats an unavailable colour variant
        in_stock = [p for p in filtered if p.stock_status == StockStatus.IN_STOCK]
        return in_stock or filtered

    @classmethod
    def match_best_pair(
        cls,
        amazon_list: List[ProductData],
        flipkart_list: List[ProductData],
        target_query: str
    ) -> Tuple[Optional[ProductData], Optional[ProductData], float]:
        """
        Strictly match the best same-variant pair from Amazon and Flipkart.

        Strategy:
        1. Extract query keywords + storage.
        2. Pre-filter each platform's candidates — ALL keywords must match.
        3. If a platform has NO valid candidates after filtering → NOT_FOUND for that slot.
           NEVER substitute a different phone model.
        4. Pick the highest fuzzy-similarity pair from the filtered sets.

        Returns: (amazon_product_or_None, flipkart_product_or_None, similarity_score)
        """
        query_keywords = cls.extract_model_keywords(target_query)
        query_storage = cls.normalize_storage(target_query)

        # Filter to only exact variant matches
        amz_filtered = cls.filter_candidates(amazon_list, query_keywords, query_storage)
        fpk_filtered = cls.filter_candidates(flipkart_list, query_keywords, query_storage)

        # Build NOT_FOUND sentinels for missing platforms
        def not_found(platform: str, query: str) -> ProductData:
            import urllib.parse
            base = "https://www.amazon.in/s?k=" if platform == "amazon" else "https://www.flipkart.com/search?q="
            return ProductData(
                platform=platform,
                title=f"{query} — Not found on {'Amazon' if platform == 'amazon' else 'Flipkart'}",
                price=None,
                mrp=None,
                discount_percent=None,
                stock_status=StockStatus.NOT_FOUND,
                stock_message=f"This exact variant was not found on {'Amazon India' if platform == 'amazon' else 'Flipkart'}.",
                rating=None,
                reviews_count=None,
                product_url=base + urllib.parse.quote_plus(query),
                image_url=None,
            )

        # If NEITHER platform has anything → return both as NOT_FOUND
        if not amz_filtered and not fpk_filtered:
            return not_found("amazon", target_query), not_found("flipkart", target_query), 0.0

        # If only one platform has results → other gets NOT_FOUND (no substitution!)
        if not amz_filtered:
            return not_found("amazon", target_query), fpk_filtered[0], 0.0
        if not fpk_filtered:
            return amz_filtered[0], not_found("flipkart", target_query), 0.0

        # Both have candidates — pick highest fuzzy match pair
        best_score = -1.0
        best_pair = (amz_filtered[0], fpk_filtered[0])

        for amz in amz_filtered:
            amz_clean = cls._clean_for_fuzzy(amz.title)
            for fpk in fpk_filtered:
                fpk_clean = cls._clean_for_fuzzy(fpk.title)
                score = fuzz.token_set_ratio(amz_clean, fpk_clean)
                if score > best_score:
                    best_score = score
                    best_pair = (amz, fpk)

        final_score = round(min(max(best_score, 0.0), 100.0), 1)
        return best_pair[0], best_pair[1], final_score

    @staticmethod
    def _clean_for_fuzzy(title: str) -> str:
        """Strip noise for cleaner fuzzy comparison."""
        cleaned = re.sub(r"[\(\)\[\],|]", " ", title)
        cleaned = re.sub(
            r"\b(5G|4G|smartphone|phone|mobile|official|edition|unlocked|assured|seller|fulfilled|imported)\b",
            "", cleaned, flags=re.IGNORECASE
        )
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned
