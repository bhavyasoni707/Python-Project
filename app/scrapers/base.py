"""
Base Scraper Interface and Data Structures
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, List, Dict, Any

class StockStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    CURRENTLY_UNAVAILABLE = "CURRENTLY_UNAVAILABLE"
    NOT_FOUND = "NOT_FOUND"

@dataclass
class ProductData:
    platform: str                    # 'amazon' or 'flipkart'
    title: str                       # Scraped product title
    price: Optional[float]           # Current selling price in INR
    mrp: Optional[float]             # Maximum Retail Price in INR
    discount_percent: Optional[float]# Calculated or scraped discount percentage
    stock_status: StockStatus        # In stock, out of stock, unavailable, etc.
    stock_message: str               # Raw text snippet explaining availability
    rating: Optional[float]          # Star rating out of 5.0
    reviews_count: Optional[int]     # Number of ratings/reviews
    product_url: str                 # Direct link to product page
    image_url: Optional[str]         # Product image thumbnail URL
    brand: Optional[str] = None
    model: Optional[str] = None
    storage: Optional[str] = None
    color: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["stock_status"] = self.stock_status.value
        return data

class BaseScraper(ABC):
    """Abstract base class for platform scrapers."""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name

    @abstractmethod
    def search(self, query: str) -> List[ProductData]:
        """Search platform for query and return list of matched products."""
        pass
