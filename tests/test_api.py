"""
Unit Tests for FastAPI REST Endpoints
"""

import pytest
from starlette.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_root_serves_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Smartphone Price Comparison Analyzer" in response.text

def test_popular_phones_endpoint(client):
    response = client.get("/api/popular")
    assert response.status_code == 200
    data = response.json()
    assert "popular" in data
    assert len(data["popular"]) > 0

def test_compare_endpoint(client):
    response = client.get("/api/compare?q=iPhone+15&live=false")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "analysis" in data
    assert "price_diff" in data["analysis"]
    assert "cheaper_platform" in data["analysis"]
    assert "pipeline_telemetry" in data

def test_analytics_overview_endpoint(client):
    response = client.get("/api/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_comparisons" in data
    assert "cheaper_counts" in data

def test_export_csv_endpoint(client):
    # Ensure at least one search was performed
    client.get("/api/compare?q=iPhone+15&live=false")
    response = client.get("/api/export?format=csv")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "query" in response.text
