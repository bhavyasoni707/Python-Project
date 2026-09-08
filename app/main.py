"""
FastAPI Backend Application Entrypoint
Provides REST endpoints, comparison pipeline execution,
analytics aggregations, and data export.
"""

import io
import pandas as pd
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import STATIC_DIR, TEMPLATES_DIR, POPULAR_PHONES
from app.database.db import (
    init_db,
    get_price_history,
    get_recent_comparisons,
    get_analytics_summary,
    get_all_products
)
from app.pipeline.pipeline import ComparisonPipeline

pipeline = ComparisonPipeline()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database on startup
    init_db()
    # Pre-seed top popular smartphones so dashboard charts and analytics have rich data immediately
    try:
        for item in POPULAR_PHONES[:4]:
            pipeline.run(item["query"])
    except Exception:
        pass
    yield

app = FastAPI(
    title="Amazon vs Flipkart Smartphone Price Comparison Analyzer",
    description="Full-stack web scraping and data analytics platform for smartphone price and stock comparison.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve the interactive dashboard HTML."""
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Template index.html not found.")
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))

@app.get("/api/compare")
async def compare_smartphone(
    q: str = Query(..., description="Smartphone name or query string (e.g., 'iPhone 15')"),
    live: bool = Query(False, description="Attempt live network scraping first")
):
    """Run the complete comparative pipeline for a smartphone query."""
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters.")
    
    result = pipeline.run(query=q, force_live=live)
    return result

@app.get("/api/history/{product_name}")
async def get_product_history(product_name: str):
    """Fetch historical price timeline for a product."""
    data = get_price_history(product_name)
    return data

@app.get("/api/popular")
async def get_popular_phones():
    """Return curated popular smartphones for quick search pills."""
    return {"popular": POPULAR_PHONES}

@app.get("/api/recent")
async def get_recent():
    """Return recent comparison runs."""
    records = get_recent_comparisons(limit=12)
    return {"recent": records}

@app.get("/api/analytics/overview")
async def get_analytics():
    """Return aggregate analytics for dashboard KPIs."""
    summary = get_analytics_summary()
    return summary

@app.get("/api/export")
async def export_data(format: str = Query("csv", pattern="^(csv|json)$")):
    """Export all comparison records as CSV or JSON."""
    records = get_recent_comparisons(limit=100)
    if not records:
        raise HTTPException(status_code=404, detail="No comparison data found to export.")
    
    df = pd.DataFrame(records)
    
    if format == "csv":
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return Response(
            content=csv_buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=smartphone_price_comparisons.csv"}
        )
    else:
        json_str = df.to_json(orient="records", indent=2)
        return Response(
            content=json_str,
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=smartphone_price_comparisons.json"}
        )
