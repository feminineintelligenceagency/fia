"""
Pytest test suite for FIA backend API endpoints.

Tests are grouped into:
- Data endpoints (no OpenAI needed — fast, no API cost)
- Search endpoints (needs ChromaDB initialized)
- AI endpoints (needs OpenAI — marked @pytest.mark.slow)
- Regression tests for existing endpoints
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Data endpoint tests (no OpenAI calls)
# ---------------------------------------------------------------------------

class TestTypologies:
    def test_get_typologies(self):
        response = client.get("/typologies")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Each typology should have a name and summary key
        first = data[0]
        assert "name" in first
        assert "summary" in first

    def test_get_typology_by_name(self):
        response = client.get("/typologies/Mr. Always Right")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Mr. Always Right"
        assert data.get("summary") is not None

    def test_get_typology_not_found(self):
        response = client.get("/typologies/Nonexistent Pattern")
        assert response.status_code == 404


class TestAbuseFlavors:
    def test_get_abuse_flavors(self):
        response = client.get("/abuse-flavors")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        assert "Flavor" in first
        assert "Player typologies" in first


class TestTraumaTypes:
    def test_get_trauma_types(self):
        response = client.get("/trauma-types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "Name" in data[0]


class TestVulnerabilityTypes:
    def test_get_vulnerability_types(self):
        response = client.get("/vulnerability-types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        assert "name" in first
        assert "vulnerability_traits" in first


# ---------------------------------------------------------------------------
# Search endpoint tests (needs ChromaDB initialized)
# ---------------------------------------------------------------------------

class TestSearch:
    def test_search_returns_results(self):
        response = client.post("/search?query=guilt+tripping&k=5")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "guilt tripping"
        assert isinstance(data["results"], list)
        assert data["count"] >= 0
        if data["count"] > 0:
            result = data["results"][0]
            assert "content" in result
            assert "metadata" in result
            assert "relevance_score" in result

    def test_search_with_category_filter(self):
        response = client.post("/search?query=manipulation&k=10&category=player_typology")
        assert response.status_code == 200
        data = response.json()
        # All returned results should match the category (if any returned)
        for result in data["results"]:
            assert result["metadata"].get("category") == "player_typology"

    def test_search_empty_query(self):
        response = client.post("/search?query=")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# AI endpoint tests (needs OpenAI — slow)
# ---------------------------------------------------------------------------

@pytest.mark.slow
class TestExplainPattern:
    def test_explain_pattern(self):
        response = client.post(
            "/explain-pattern",
            json={"pattern_name": "Mr. Always Right"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["pattern_name"] == "Mr. Always Right"
        assert len(data["explanation"]) > 0
        assert isinstance(data["key_red_flags"], list)
        assert isinstance(data["safety_tips"], list)

    def test_explain_pattern_not_found(self):
        response = client.post(
            "/explain-pattern",
            json={"pattern_name": "Nonexistent Pattern"},
        )
        assert response.status_code == 404


@pytest.mark.slow
class TestComparePatterns:
    def test_compare_patterns(self):
        response = client.post(
            "/compare-patterns",
            json={"pattern_a": "Mr. Always Right", "pattern_b": "The Subtle Saboteur"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["pattern_a"] == "Mr. Always Right"
        assert data["pattern_b"] == "The Subtle Saboteur"
        assert isinstance(data["similarities"], list)
        assert isinstance(data["differences"], list)
        assert len(data["combined_danger"]) > 0


@pytest.mark.slow
class TestSafetyPlan:
    def test_safety_plan(self):
        response = client.post(
            "/safety-plan",
            json={
                "story": "My partner controls everything I do and isolates me from friends.",
                "patterns_detected": ["Mr. Always Right"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["immediate_steps"], list)
        assert isinstance(data["long_term_strategies"], list)
        assert isinstance(data["resources"], list)
        assert len(data["affirmation"]) > 0


# ---------------------------------------------------------------------------
# Existing endpoint regression tests
# ---------------------------------------------------------------------------

class TestExistingEndpoints:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200

    @pytest.mark.slow
    def test_analyze(self):
        response = client.post(
            "/analyze",
            json={"content": "My partner always needs to be right and belittles me."},
        )
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert "findings" in data
        assert "patterns_detected" in data
