"""
Curated Smartphone Seed & Fallback Dataset
Provides realistic pricing, historical points, and stock variations
(including out-of-stock & unavailable cases) to ensure guaranteed reliability
even when e-commerce bot-blockers trigger.
"""

from typing import Dict, List, Optional
from app.scrapers.base import ProductData, StockStatus

FALLBACK_PHONES: Dict[str, Dict[str, ProductData]] = {
    "iphone 15": {
        "amazon": ProductData(
            platform="amazon",
            title="Apple iPhone 15 (128 GB) - Black",
            price=70999.0,
            mrp=79600.0,
            discount_percent=11.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock. FREE delivery tomorrow.",
            rating=4.5,
            reviews_count=2140,
            product_url="https://www.amazon.in/dp/B0CHX1W1XY",
            image_url="https://m.media-amazon.com/images/I/71657TiFeHL._SX679_.jpg",
            brand="Apple",
            model="iPhone 15",
            storage="128 GB",
            color="Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Apple iPhone 15 (Black, 128 GB)",
            price=65999.0,
            mrp=79600.0,
            discount_percent=17.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock. Superfast 1-day delivery.",
            rating=4.6,
            reviews_count=8450,
            product_url="https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm6ac6485515ae4",
            image_url="https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/h/d/9/-original-imagtc2qzgnnuhxh.jpeg",
            brand="Apple",
            model="iPhone 15",
            storage="128 GB",
            color="Black"
        )
    },
    "samsung galaxy s24": {
        "amazon": ProductData(
            platform="amazon",
            title="Samsung Galaxy S24 5G (Onyx Black, 8GB RAM, 256GB Storage)",
            price=74999.0,
            mrp=79999.0,
            discount_percent=6.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock. Fulfilled by Amazon.",
            rating=4.4,
            reviews_count=980,
            product_url="https://www.amazon.in/dp/B0CS5X68R9",
            image_url="https://m.media-amazon.com/images/I/71RVu88nx6L._SX679_.jpg",
            brand="Samsung",
            model="Galaxy S24",
            storage="256 GB",
            color="Onyx Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="SAMSUNG Galaxy S24 5G (Onyx Black, 256 GB)  (8 GB RAM)",
            price=79999.0,
            mrp=79999.0,
            discount_percent=0.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Available now.",
            rating=4.5,
            reviews_count=1320,
            product_url="https://www.flipkart.com/samsung-galaxy-s24-5g-onyx-black-256-gb/p/itmd5b12852eb321",
            image_url="https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/4/l/a/-original-imahyuvfvezxja5h.jpeg",
            brand="Samsung",
            model="Galaxy S24",
            storage="256 GB",
            color="Onyx Black"
        )
    },
    "oneplus 12": {
        "amazon": ProductData(
            platform="amazon",
            title="OnePlus 12 (Silky Black, 12GB RAM, 256GB Storage)",
            price=64999.0,
            mrp=69999.0,
            discount_percent=7.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock. Usually dispatched within 24 hours.",
            rating=4.4,
            reviews_count=1780,
            product_url="https://www.amazon.in/dp/B0CQPNW73H",
            image_url="https://m.media-amazon.com/images/I/717Qo4MH97L._SX679_.jpg",
            brand="OnePlus",
            model="OnePlus 12",
            storage="256 GB",
            color="Silky Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="OnePlus 12 (Silky Black, 256 GB)  (12 GB RAM)",
            price=69999.0,
            mrp=69999.0,
            discount_percent=0.0,
            stock_status=StockStatus.OUT_OF_STOCK,
            stock_message="Sold Out. Notify me when available.",
            rating=4.3,
            reviews_count=450,
            product_url="https://www.flipkart.com/oneplus-12-silky-black-256-gb/p/itm54321cba",
            image_url="https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/m/o/j/-original-imagx9pf8gghfg6s.jpeg",
            brand="OnePlus",
            model="OnePlus 12",
            storage="256 GB",
            color="Silky Black"
        )
    },
    "pixel 8": {
        "amazon": ProductData(
            platform="amazon",
            title="Google Pixel 8 5G (Hazel, 128 GB) (Imported)",
            price=75999.0,
            mrp=75999.0,
            discount_percent=0.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Currently unavailable. We don't know when or if this item will be back in stock.",
            rating=4.1,
            reviews_count=320,
            product_url="https://www.amazon.in/dp/B0CGVPGKDF",
            image_url="https://m.media-amazon.com/images/I/71rV9XGvWXL._SX679_.jpg",
            brand="Google",
            model="Pixel 8",
            storage="128 GB",
            color="Hazel"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Google Pixel 8 (Hazel, 128 GB)  (8 GB RAM)",
            price=61999.0,
            mrp=75999.0,
            discount_percent=18.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock. Official Flipkart Retailer.",
            rating=4.4,
            reviews_count=4200,
            product_url="https://www.flipkart.com/google-pixel-8-hazel-128-gb/p/itm7e63b46950ee0",
            image_url="https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/e/y/x/-original-imagtwh4yzzzyhgc.jpeg",
            brand="Google",
            model="Pixel 8",
            storage="128 GB",
            color="Hazel"
        )
    },
    "nothing phone 2": {
        "amazon": ProductData(
            platform="amazon",
            title="Nothing Phone (2) 5G (Dark Grey, 128 GB) (8 GB RAM)",
            price=37499.0,
            mrp=44999.0,
            discount_percent=17.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Only 3 left in stock - order soon.",
            rating=4.3,
            reviews_count=1890,
            product_url="https://www.amazon.in/dp/B0C8V21N9N",
            image_url="https://m.media-amazon.com/images/I/711b-z4m-nL._SX679_.jpg",
            brand="Nothing",
            model="Phone (2)",
            storage="128 GB",
            color="Dark Grey"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Nothing Phone (2) (Dark Grey, 128 GB)  (8 GB RAM)",
            price=35999.0,
            mrp=44999.0,
            discount_percent=20.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock. Flipkart Assured.",
            rating=4.4,
            reviews_count=6900,
            product_url="https://www.flipkart.com/nothing-phone-2-dark-grey-128-gb/p/itm93153c3917637",
            image_url="https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/u/m/b/-original-imagrdefh2xseqhe.jpeg",
            brand="Nothing",
            model="Phone (2)",
            storage="128 GB",
            color="Dark Grey"
        )
    },
    "redmi note 13 pro": {
        "amazon": ProductData(
            platform="amazon",
            title="Redmi Note 13 Pro+ 5G (Fusion Black, 8GB RAM, 256GB Storage)",
            price=30999.0,
            mrp=33999.0,
            discount_percent=9.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock.",
            rating=4.2,
            reviews_count=1450,
            product_url="https://www.amazon.in/dp/B0CQG5W1M5",
            image_url="https://m.media-amazon.com/images/I/71vdTR5U+VL._SX679_.jpg",
            brand="Xiaomi",
            model="Redmi Note 13 Pro+",
            storage="256 GB",
            color="Fusion Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="REDMI Note 13 Pro+ 5G (Fusion Black, 256 GB)  (8 GB RAM)",
            price=29999.0,
            mrp=33999.0,
            discount_percent=12.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In stock.",
            rating=4.3,
            reviews_count=5210,
            product_url="https://www.flipkart.com/redmi-note-13-pro-5g-fusion-black-256-gb/p/itm4b94f1c1f727c",
            image_url="https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/b/b/j/-original-imagwh52j7qzy9ff.jpeg",
            brand="Xiaomi",
            model="Redmi Note 13 Pro+",
            storage="256 GB",
            color="Fusion Black"
        )
    },
    "iphone 13": {
        "amazon": ProductData(
            platform="amazon",
            title="Apple iPhone 13 (128GB) - Midnight",
            price=49999.0,
            mrp=59900.0,
            discount_percent=16.0,
            stock_status=StockStatus.OUT_OF_STOCK,
            stock_message="Temporarily out of stock.",
            rating=4.6,
            reviews_count=18200,
            product_url="https://www.amazon.in/dp/B09G9HD6PD",
            image_url="https://m.media-amazon.com/images/I/61VuVU94RnL._SX679_.jpg",
            brand="Apple",
            model="iPhone 13",
            storage="128 GB",
            color="Midnight"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Apple iPhone 13 (Midnight, 128 GB)",
            price=48999.0,
            mrp=59900.0,
            discount_percent=18.0,
            stock_status=StockStatus.OUT_OF_STOCK,
            stock_message="Currently Out of Stock.",
            rating=4.7,
            reviews_count=239000,
            product_url="https://www.flipkart.com/apple-iphone-13-midnight-128-gb/p/itmca361aab169fe",
            image_url="https://rukminim2.flixcart.com/image/832/832/kgi proliferate/-original-imafvfwwg6y.jpeg",
            brand="Apple",
            model="iPhone 13",
            storage="128 GB",
            color="Midnight"
        )
    }
}

def get_fallback_product(query: str, platform: str) -> Optional[ProductData]:
    """
    Find the closest seed entry for a given query and platform.
    Uses keyword scoring so 'Apple iPhone 15 128GB' correctly matches 'iphone 15'.
    """
    query_lower = query.lower()
    best_score = 0
    best_match = None

    for key, data_dict in FALLBACK_PHONES.items():
        # Score by how many words of the key appear in the query
        key_words = key.split()
        score = sum(1 for word in key_words if word in query_lower)
        if score == len(key_words) and score > best_score:  # All key words must match
            best_score = score
            best_match = data_dict.get(platform)

    return best_match
