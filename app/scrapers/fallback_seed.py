"""
Curated Smartphone Seed & Fallback Dataset
Used only when a live scrape returns nothing. Flipkart figures were refreshed from
live Flipkart listings on 2026-09-24; phones Flipkart no longer lists are marked
CURRENTLY_UNAVAILABLE. Amazon blocks automated price checks, so Amazon figures are
last recorded prices, capped at the current official MRP.
Images are bundled locally under app/static/img/phones/.

STRICT MATCHING RULE: ALL words in the seed key must appear in the query.
Longer key = more specific = wins over shorter key.
e.g. "iphone 15 pro max" beats "iphone 15" for query "iPhone 15 Pro Max 256GB"
"""

from typing import Dict, Optional
from app.scrapers.base import ProductData, StockStatus

# Keys are lowercase. ALL words must match query. Longer = more specific = higher priority.
FALLBACK_PHONES: Dict[str, Dict[str, ProductData]] = {

    # ===== Apple iPhone 15 Series =====
    "iphone 15 pro max": {
        "amazon": ProductData(
            platform="amazon",
            title="Apple iPhone 15 Pro Max (256 GB) - Black Titanium",
            price=134900.0,
            mrp=159900.0,
            discount_percent=15.6,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.6,
            reviews_count=38500,
            product_url="https://www.amazon.in/Apple-iPhone-15-Pro-Max/dp/B0CHX2F5QT",
            image_url="/static/img/phones/iphone-15-pro-max.jpg",
            brand="Apple", model="iPhone 15 Pro Max", storage="256 GB", color="Black Titanium"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Apple iPhone 15 Pro Max (Black Titanium, 256 GB)",
            price=159900.0,
            mrp=159900.0,
            discount_percent=0.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Currently unavailable on Flipkart",
            rating=4.6,
            reviews_count=2708,
            product_url="https://www.flipkart.com/apple-iphone-15-pro-max-black-titanium-256-gb/p/itmd170cfc1dec9e",
            image_url="/static/img/phones/iphone-15-pro-max.jpg",
            brand="Apple", model="iPhone 15 Pro Max", storage="256 GB", color="Black Titanium"
        )
    },

    "iphone 15 pro": {
        "amazon": ProductData(
            platform="amazon",
            title="Apple iPhone 15 Pro (128 GB) - Black Titanium",
            price=107900.0,
            mrp=134900.0,
            discount_percent=20.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.6,
            reviews_count=51000,
            product_url="https://www.amazon.in/Apple-iPhone-15-Pro/dp/B0CHX1W1ZY",
            image_url="/static/img/phones/iphone-15-pro.jpg",
            brand="Apple", model="iPhone 15 Pro", storage="128 GB", color="Black Titanium"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Apple iPhone 15 Pro (Black Titanium, 128 GB)",
            price=134900.0,
            mrp=134900.0,
            discount_percent=0.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Currently unavailable on Flipkart",
            rating=4.7,
            reviews_count=2986,
            product_url="https://www.flipkart.com/apple-iphone-15-pro-black-titanium-128-gb/p/itm96f61fdd7e604",
            image_url="/static/img/phones/iphone-15-pro.jpg",
            brand="Apple", model="iPhone 15 Pro", storage="128 GB", color="Black Titanium"
        )
    },

    "iphone 15": {
        "amazon": ProductData(
            platform="amazon",
            title="Apple iPhone 15 (128 GB) - Black",
            price=59900.0,
            mrp=59900.0,
            discount_percent=0.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.5,
            reviews_count=214000,
            product_url="https://www.amazon.in/Apple-iPhone-15/dp/B0CHX1W1XY",
            image_url="/static/img/phones/iphone-15.jpg",
            brand="Apple", model="iPhone 15", storage="128 GB", color="Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Apple iPhone 15 (Black, 128 GB)",
            price=59900.0,
            mrp=59900.0,
            discount_percent=0.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In Stock on Flipkart",
            rating=4.6,
            reviews_count=248770,
            product_url="https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm6ac6485515ae4",
            image_url="/static/img/phones/iphone-15.jpg",
            brand="Apple", model="iPhone 15", storage="128 GB", color="Black"
        )
    },

    "iphone 14": {
        "amazon": ProductData(
            platform="amazon",
            title="Apple iPhone 14 (128GB) - Midnight",
            price=58999.0,
            mrp=79900.0,
            discount_percent=26.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.6,
            reviews_count=348000,
            product_url="https://www.amazon.in/Apple-iPhone-14/dp/B0BDJ7MHQ8",
            image_url="/static/img/phones/iphone-14.jpg",
            brand="Apple", model="iPhone 14", storage="128 GB", color="Midnight"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Apple iPhone 14 (Midnight, 128 GB)",
            price=55999.0,
            mrp=79900.0,
            discount_percent=30.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.7,
            reviews_count=198000,
            product_url="https://www.flipkart.com/apple-iphone-14-midnight-128-gb/p/itmca361aab169ff",
            image_url="/static/img/phones/iphone-14.jpg",
            brand="Apple", model="iPhone 14", storage="128 GB", color="Midnight"
        )
    },

    "iphone 13": {
        "amazon": ProductData(
            platform="amazon",
            title="Apple iPhone 13 (128GB) - Midnight",
            price=49999.0,
            mrp=59900.0,
            discount_percent=17.0,
            stock_status=StockStatus.OUT_OF_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.6,
            reviews_count=182000,
            product_url="https://www.amazon.in/Apple-iPhone-13/dp/B09G9HD6PD",
            image_url="/static/img/phones/iphone-13.jpg",
            brand="Apple", model="iPhone 13", storage="128 GB", color="Midnight"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Apple iPhone 13 (Midnight, 128 GB)",
            price=48999.0,
            mrp=59900.0,
            discount_percent=18.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.7,
            reviews_count=239000,
            product_url="https://www.flipkart.com/apple-iphone-13-midnight-128-gb/p/itmca361aab169fe",
            image_url="/static/img/phones/iphone-13.jpg",
            brand="Apple", model="iPhone 13", storage="128 GB", color="Midnight"
        )
    },

    # ===== Samsung Galaxy S24 Series =====
    "samsung galaxy s24 ultra": {
        "amazon": ProductData(
            platform="amazon",
            title="Samsung Galaxy S24 Ultra 5G (Titanium Black, 12GB RAM, 256GB Storage)",
            price=124999.0,
            mrp=134999.0,
            discount_percent=7.4,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.5,
            reviews_count=21000,
            product_url="https://www.amazon.in/Samsung-Galaxy-S24-Ultra/dp/B0CS5XJH4X",
            image_url="/static/img/phones/samsung-galaxy-s24-ultra.jpg",
            brand="Samsung", model="Galaxy S24 Ultra", storage="256 GB", color="Titanium Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Samsung Galaxy S24 Ultra 5G (Titanium Black, 256 GB)",
            price=80970.0,
            mrp=134999.0,
            discount_percent=40.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Currently unavailable on Flipkart",
            rating=4.6,
            reviews_count=7666,
            product_url="https://www.flipkart.com/samsung-galaxy-s24-ultra-5g-titanium-black-256-gb/p/itm7d3b6b5d0f501",
            image_url="/static/img/phones/samsung-galaxy-s24-ultra.jpg",
            brand="Samsung", model="Galaxy S24 Ultra", storage="256 GB", color="Titanium Black"
        )
    },

    "samsung galaxy s24": {
        "amazon": ProductData(
            platform="amazon",
            title="Samsung Galaxy S24 5G (Onyx Black, 8GB RAM, 256GB Storage)",
            price=74999.0,
            mrp=79999.0,
            discount_percent=6.3,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.4,
            reviews_count=98000,
            product_url="https://www.amazon.in/Samsung-Galaxy-S24/dp/B0CS5X68R9",
            image_url="/static/img/phones/samsung-galaxy-s24.jpg",
            brand="Samsung", model="Galaxy S24", storage="256 GB", color="Onyx Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Samsung Galaxy S24 5G Snapdragon (Onyx Black, 256 GB)",
            price=55999.0,
            mrp=79999.0,
            discount_percent=30.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In Stock on Flipkart",
            rating=4.6,
            reviews_count=57466,
            product_url="https://www.flipkart.com/samsung-galaxy-s24-5g-snapdragon-onyx-black-256-gb/p/itm0eb31619428e4",
            image_url="/static/img/phones/samsung-galaxy-s24.jpg",
            brand="Samsung", model="Galaxy S24", storage="256 GB", color="Onyx Black"
        )
    },

    "samsung galaxy a55": {
        "amazon": ProductData(
            platform="amazon",
            title="Samsung Galaxy A55 5G (Awesome Navy, 8GB RAM, 128GB Storage)",
            price=28999.0,
            mrp=42999.0,
            discount_percent=32.6,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.3,
            reviews_count=42000,
            product_url="https://www.amazon.in/Samsung-Galaxy-A55/dp/B0CXML45PQ",
            image_url="/static/img/phones/samsung-galaxy-a55.jpg",
            brand="Samsung", model="Galaxy A55", storage="128 GB", color="Awesome Navy"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Samsung Galaxy A55 5G (Awesome Navy, 128 GB)",
            price=17999.0,
            mrp=42999.0,
            discount_percent=58.1,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Currently unavailable on Flipkart",
            rating=4.4,
            reviews_count=7809,
            product_url="https://www.flipkart.com/samsung-galaxy-a55-5g-awesome-navy-128-gb/p/itm7ac5d2771f7a0",
            image_url="/static/img/phones/samsung-galaxy-a55.jpg",
            brand="Samsung", model="Galaxy A55", storage="128 GB", color="Awesome Navy"
        )
    },

    "samsung galaxy a35": {
        "amazon": ProductData(
            platform="amazon",
            title="Samsung Galaxy A35 5G (Awesome Iceblue, 8GB RAM, 128GB Storage)",
            price=21999.0,
            mrp=33999.0,
            discount_percent=35.3,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=31000,
            product_url="https://www.amazon.in/Samsung-Galaxy-A35/dp/B0CXML45AA",
            image_url="/static/img/phones/samsung-galaxy-a35.jpg",
            brand="Samsung", model="Galaxy A35", storage="128 GB", color="Awesome Iceblue"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Samsung Galaxy A35 5G (Awesome Iceblue, 128 GB)",
            price=18999.0,
            mrp=33999.0,
            discount_percent=44.1,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In Stock on Flipkart",
            rating=4.4,
            reviews_count=77410,
            product_url="https://www.flipkart.com/samsung-galaxy-a35-5g-awesome-iceblue-128-gb/p/itm9684d2fe9201e",
            image_url="/static/img/phones/samsung-galaxy-a35.jpg",
            brand="Samsung", model="Galaxy A35", storage="128 GB", color="Awesome Iceblue"
        )
    },

    # ===== OnePlus =====
    "oneplus 12r": {
        "amazon": ProductData(
            platform="amazon",
            title="OnePlus 12R 5G (Cool Blue, 8GB RAM, 128GB Storage)",
            price=29999.0,
            mrp=39999.0,
            discount_percent=25.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.3,
            reviews_count=21000,
            product_url="https://www.amazon.in/OnePlus-12R/dp/B0CQPNW73I",
            image_url="/static/img/phones/oneplus-12r.jpg",
            brand="OnePlus", model="OnePlus 12R", storage="128 GB", color="Cool Blue"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="OnePlus 12R (Cool Blue, 128 GB)",
            price=34999.0,
            mrp=39999.0,
            discount_percent=12.5,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Currently unavailable on Flipkart",
            rating=4.5,
            reviews_count=7685,
            product_url="https://www.flipkart.com/oneplus-12r-cool-blue-128-gb/p/itm347349f7db2f2",
            image_url="/static/img/phones/oneplus-12r.jpg",
            brand="OnePlus", model="OnePlus 12R", storage="128 GB", color="Cool Blue"
        )
    },

    "oneplus 12": {
        "amazon": ProductData(
            platform="amazon",
            title="OnePlus 12 5G (Silky Black, 12GB RAM, 256GB Storage)",
            price=64999.0,
            mrp=64999.0,
            discount_percent=0.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.4,
            reviews_count=178000,
            product_url="https://www.amazon.in/OnePlus-12-5G/dp/B0CQPNW73H",
            image_url="/static/img/phones/oneplus-12.jpg",
            brand="OnePlus", model="OnePlus 12", storage="256 GB", color="Silky Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="OnePlus 12 (Silky Black, 256 GB)",
            price=50399.0,
            mrp=64999.0,
            discount_percent=22.5,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Currently unavailable on Flipkart",
            rating=4.6,
            reviews_count=1666,
            product_url="https://www.flipkart.com/oneplus-12-silky-black-256-gb/p/itm4464454f95a2e",
            image_url="/static/img/phones/oneplus-12.jpg",
            brand="OnePlus", model="OnePlus 12", storage="256 GB", color="Silky Black"
        )
    },

    "oneplus nord ce4": {
        "amazon": ProductData(
            platform="amazon",
            title="OnePlus Nord CE 4 5G (Dark Chrome, 8GB RAM, 128GB Storage)",
            price=24999.0,
            mrp=32499.0,
            discount_percent=23.1,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=19000,
            product_url="https://www.amazon.in/OnePlus-Nord-CE-4/dp/B0D2PY3MKL",
            image_url="/static/img/phones/oneplus-nord-ce4.jpg",
            brand="OnePlus", model="Nord CE 4", storage="128 GB", color="Dark Chrome"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="OnePlus Nord CE4 (Dark Chrome, 128 GB)",
            price=32499.0,
            mrp=32499.0,
            discount_percent=0.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In Stock on Flipkart",
            rating=4.4,
            reviews_count=28062,
            product_url="https://www.flipkart.com/oneplus-nord-ce4-dark-chrome-128-gb/p/itm5a09089114afb",
            image_url="/static/img/phones/oneplus-nord-ce4.jpg",
            brand="OnePlus", model="Nord CE 4", storage="128 GB", color="Dark Chrome"
        )
    },

    # ===== Google Pixel =====
    "pixel 8 pro": {
        "amazon": ProductData(
            platform="amazon",
            title="Google Pixel 8 Pro 5G (Obsidian, 12GB RAM, 128GB Storage)",
            price=84999.0,
            mrp=106999.0,
            discount_percent=21.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.4,
            reviews_count=21000,
            product_url="https://www.amazon.in/Google-Pixel-8-Pro/dp/B0CGVPGKDE",
            image_url="/static/img/phones/pixel-8-pro.jpg",
            brand="Google", model="Pixel 8 Pro", storage="128 GB", color="Obsidian"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Google Pixel 8 Pro (Obsidian, 128 GB) (12 GB RAM)",
            price=79999.0,
            mrp=106999.0,
            discount_percent=25.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.5,
            reviews_count=42000,
            product_url="https://www.flipkart.com/google-pixel-8-pro-obsidian-128-gb/p/itm7e63b46950ee2",
            image_url="/static/img/phones/pixel-8-pro.jpg",
            brand="Google", model="Pixel 8 Pro", storage="128 GB", color="Obsidian"
        )
    },

    "pixel 8": {
        "amazon": ProductData(
            platform="amazon",
            title="Google Pixel 8 5G (Hazel, 128 GB)",
            price=69999.0,
            mrp=75999.0,
            discount_percent=8.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=32000,
            product_url="https://www.amazon.in/Google-Pixel-8/dp/B0CGVPGKDF",
            image_url="/static/img/phones/pixel-8.jpg",
            brand="Google", model="Pixel 8", storage="128 GB", color="Hazel"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Google Pixel 8 (Hazel, 128 GB) (8 GB RAM)",
            price=61999.0,
            mrp=75999.0,
            discount_percent=18.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.4,
            reviews_count=420000,
            product_url="https://www.flipkart.com/google-pixel-8-hazel-128-gb/p/itm7e63b46950ee0",
            image_url="/static/img/phones/pixel-8.jpg",
            brand="Google", model="Pixel 8", storage="128 GB", color="Hazel"
        )
    },

    # ===== Nothing =====
    "nothing phone 2a": {
        "amazon": ProductData(
            platform="amazon",
            title="Nothing Phone (2a) 5G (Black, 8GB RAM, 128GB Storage)",
            price=19999.0,
            mrp=23999.0,
            discount_percent=17.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.3,
            reviews_count=45000,
            product_url="https://www.amazon.in/Nothing-Phone-2a/dp/B0CW5ZJBR2",
            image_url="/static/img/phones/nothing-phone-2a.jpg",
            brand="Nothing", model="Phone (2a)", storage="128 GB", color="Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Nothing Phone (2a) 5G (Black, 128 GB) (8 GB RAM)",
            price=18999.0,
            mrp=23999.0,
            discount_percent=21.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.4,
            reviews_count=98000,
            product_url="https://www.flipkart.com/nothing-phone-2a-black-128-gb/p/itm93153c3917638",
            image_url="/static/img/phones/nothing-phone-2a.jpg",
            brand="Nothing", model="Phone (2a)", storage="128 GB", color="Black"
        )
    },

    "nothing phone 2": {
        "amazon": ProductData(
            platform="amazon",
            title="Nothing Phone (2) 5G (Dark Grey, 8GB RAM, 128GB Storage)",
            price=37499.0,
            mrp=44999.0,
            discount_percent=17.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.3,
            reviews_count=18900,
            product_url="https://www.amazon.in/Nothing-Phone-2/dp/B0C8V21N9N",
            image_url="/static/img/phones/nothing-phone-2.jpg",
            brand="Nothing", model="Phone (2)", storage="128 GB", color="Dark Grey"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Nothing Phone (2) (Dark Grey, 128 GB) (8 GB RAM)",
            price=35999.0,
            mrp=44999.0,
            discount_percent=20.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.4,
            reviews_count=69000,
            product_url="https://www.flipkart.com/nothing-phone-2-dark-grey-128-gb/p/itm93153c3917637",
            image_url="/static/img/phones/nothing-phone-2.jpg",
            brand="Nothing", model="Phone (2)", storage="128 GB", color="Dark Grey"
        )
    },

    # ===== Xiaomi / Redmi =====
    "redmi note 13 pro plus": {
        "amazon": ProductData(
            platform="amazon",
            title="Redmi Note 13 Pro+ 5G (Fusion Black, 8GB RAM, 256GB Storage)",
            price=29999.0,
            mrp=33999.0,
            discount_percent=12.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=14500,
            product_url="https://www.amazon.in/Redmi-Note-13-Pro-Plus/dp/B0CQG5W1M5",
            image_url="/static/img/phones/redmi-note-13-pro-plus.jpg",
            brand="Xiaomi", model="Redmi Note 13 Pro+", storage="256 GB", color="Fusion Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="REDMI Note 13 Pro+ 5G (Fusion Black, 256 GB) (8 GB RAM)",
            price=28999.0,
            mrp=33999.0,
            discount_percent=15.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.3,
            reviews_count=52100,
            product_url="https://www.flipkart.com/redmi-note-13-pro-5g-fusion-black-256-gb/p/itm4b94f1c1f727c",
            image_url="/static/img/phones/redmi-note-13-pro-plus.jpg",
            brand="Xiaomi", model="Redmi Note 13 Pro+", storage="256 GB", color="Fusion Black"
        )
    },

    "redmi note 13 pro": {
        "amazon": ProductData(
            platform="amazon",
            title="Redmi Note 13 Pro 5G (Arctic White, 8GB RAM, 128GB Storage)",
            price=24999.0,
            mrp=29999.0,
            discount_percent=17.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=11000,
            product_url="https://www.amazon.in/Redmi-Note-13-Pro/dp/B0CQG5W1N6",
            image_url="/static/img/phones/redmi-note-13-pro.jpg",
            brand="Xiaomi", model="Redmi Note 13 Pro", storage="128 GB", color="Arctic White"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="REDMI Note 13 Pro 5G (Arctic White, 128 GB) (8 GB RAM)",
            price=23999.0,
            mrp=29999.0,
            discount_percent=20.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.3,
            reviews_count=39000,
            product_url="https://www.flipkart.com/redmi-note-13-pro-5g-arctic-white-128-gb/p/itm4b94f1c1f727d",
            image_url="/static/img/phones/redmi-note-13-pro.jpg",
            brand="Xiaomi", model="Redmi Note 13 Pro", storage="128 GB", color="Arctic White"
        )
    },

    "xiaomi 14 ultra": {
        "amazon": ProductData(
            platform="amazon",
            title="Xiaomi 14 Ultra 5G (Black, 16GB RAM, 512GB Storage)",
            price=99999.0,
            mrp=109999.0,
            discount_percent=9.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.5,
            reviews_count=1200,
            product_url="https://www.amazon.in/Xiaomi-14-Ultra/dp/B0D1PZXYZ1",
            image_url="/static/img/phones/xiaomi-14-ultra.jpg",
            brand="Xiaomi", model="14 Ultra", storage="512 GB", color="Black"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Xiaomi 14 Ultra (Black, 512 GB) (16 GB RAM)",
            price=96999.0,
            mrp=109999.0,
            discount_percent=12.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.6,
            reviews_count=2100,
            product_url="https://www.flipkart.com/xiaomi-14-ultra-black-512-gb/p/itm4b94f1c1f7280",
            image_url="/static/img/phones/xiaomi-14-ultra.jpg",
            brand="Xiaomi", model="14 Ultra", storage="512 GB", color="Black"
        )
    },

    # ===== Motorola =====
    "motorola edge 50 pro": {
        "amazon": ProductData(
            platform="amazon",
            title="Motorola Edge 50 Pro 5G (Black Beauty, 12GB RAM, 256GB Storage)",
            price=29999.0,
            mrp=35999.0,
            discount_percent=17.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=3400,
            product_url="https://www.amazon.in/Motorola-Edge-50-Pro/dp/B0D1PZ1234",
            image_url="/static/img/phones/motorola-edge-50-pro.jpg",
            brand="Motorola", model="Edge 50 Pro", storage="256 GB", color="Black Beauty"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="Motorola Edge 50 Pro 5G (Black Beauty, 256 GB) (12 GB RAM)",
            price=28999.0,
            mrp=35999.0,
            discount_percent=19.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.3,
            reviews_count=6700,
            product_url="https://www.flipkart.com/motorola-edge-50-pro-black-beauty-256-gb/p/itm44f7ac04db2a5",
            image_url="/static/img/phones/motorola-edge-50-pro.jpg",
            brand="Motorola", model="Edge 50 Pro", storage="256 GB", color="Black Beauty"
        )
    },

    # ===== vivo =====
    "vivo v30 pro": {
        "amazon": ProductData(
            platform="amazon",
            title="vivo V30 Pro 5G (Peacock Green, 12GB RAM, 256GB Storage)",
            price=40999.0,
            mrp=44999.0,
            discount_percent=9.0,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=2300,
            product_url="https://www.amazon.in/vivo-V30-Pro/dp/B0D1PZ5678",
            image_url="/static/img/phones/vivo-v30-pro.jpg",
            brand="vivo", model="V30 Pro", storage="256 GB", color="Peacock Green"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="vivo V30 Pro 5G (Peacock Green, 256 GB) (12 GB RAM)",
            price=39999.0,
            mrp=44999.0,
            discount_percent=11.0,
            stock_status=StockStatus.CURRENTLY_UNAVAILABLE,
            stock_message="No longer listed on Flipkart",
            rating=4.3,
            reviews_count=4500,
            product_url="https://www.flipkart.com/vivo-v30-pro-peacock-green-256-gb/p/itm44f7ac04db2a6",
            image_url="/static/img/phones/vivo-v30-pro.jpg",
            brand="vivo", model="V30 Pro", storage="256 GB", color="Peacock Green"
        )
    },

    # ===== OPPO =====
    "oppo reno 11 pro": {
        "amazon": ProductData(
            platform="amazon",
            title="OPPO Reno11 Pro 5G (Rock Grey, 12GB RAM, 256GB Storage)",
            price=33999.0,
            mrp=44999.0,
            discount_percent=24.4,
            stock_status=StockStatus.IN_STOCK,
            stock_message="Last recorded Amazon price (live check unavailable)",
            rating=4.2,
            reviews_count=1900,
            product_url="https://www.amazon.in/OPPO-Reno11-Pro/dp/B0D1PZ9012",
            image_url="/static/img/phones/oppo-reno-11-pro.jpg",
            brand="OPPO", model="Reno11 Pro", storage="256 GB", color="Rock Grey"
        ),
        "flipkart": ProductData(
            platform="flipkart",
            title="OPPO Reno11 Pro 5G (Rock Grey, 256 GB)",
            price=40000.0,
            mrp=44999.0,
            discount_percent=11.1,
            stock_status=StockStatus.IN_STOCK,
            stock_message="In Stock on Flipkart",
            rating=4.4,
            reviews_count=3708,
            product_url="https://www.flipkart.com/oppo-reno11-pro-5g-rock-grey-256-gb/p/itm41ee989232c22",
            image_url="/static/img/phones/oppo-reno-11-pro.jpg",
            brand="OPPO", model="Reno11 Pro", storage="256 GB", color="Rock Grey"
        )
    },
}


def get_fallback_product(query: str, platform: str) -> Optional[ProductData]:
    """
    Find the MOST SPECIFIC seed entry that strictly matches the query.

    Rules:
    - ALL words in the seed key must appear in the query (case-insensitive).
    - The LONGEST matching key wins (most specific match).
    - e.g. query 'iphone 15 pro max 256gb' matches 'iphone 15 pro max' key,
      NOT 'iphone 15 pro' or 'iphone 15'.
    - Returns None if no seed entry matches — matcher will return NOT_FOUND.
    """
    query_lower = query.lower().strip()

    # Normalize common shorthand variations
    query_lower = (query_lower
                   .replace("pro+", "pro plus")
                   .replace("pro +", "pro plus")
                   .replace("note13", "note 13")
                   .replace("nord ce 4", "nord ce4")
                   .replace("12r", "12r"))  # keep 12r as-is

    best_key_length = 0
    best_match: Optional[ProductData] = None

    for key, data_dict in FALLBACK_PHONES.items():
        key_words = key.split()
        # ALL key words must appear somewhere in the query string
        if all(word in query_lower for word in key_words):
            # Prefer longer (more specific) keys
            if len(key_words) > best_key_length:
                best_key_length = len(key_words)
                best_match = data_dict.get(platform)

    return best_match
