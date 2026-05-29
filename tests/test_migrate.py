"""Tests for backward-compatible migration from markdown/CSV."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from db import init_db, set_db_path
from scripts.migrate_to_db import parse_frontmatter


@pytest.fixture(autouse=True)
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    set_db_path(db_path)
    init_db()
    yield db_path
    set_db_path(None)
    Path(db_path).unlink(missing_ok=True)


class TestFrontmatterParser:
    def test_parses_yaml_frontmatter(self):
        text = """---
type: weekly_forecast
week: 2026-W22
generated: 2026-05-25
macro_bias: BEARISH
---

# XAUUSD Weekly Forecast
"""
        fm, body = parse_frontmatter(text)
        assert fm["type"] == "weekly_forecast"
        assert fm["week"] == "2026-W22"
        assert "# XAUUSD Weekly Forecast" in body

    def test_no_frontmatter_returns_empty(self):
        text = "# Just a heading\n\nSome body text."
        fm, body = parse_frontmatter(text)
        assert fm == {}
        assert body == text


class TestMigrateExistingFiles:
    def test_migrate_real_weekly_forecast(self):
        """Parse the real 2026-W22.md if it exists."""
        path = Path("forecasts/weekly/xauusd/2026-W22.md")
        if not path.exists():
            pytest.skip("Real forecast file not found")

        fm, body = parse_frontmatter(path.read_text())
        assert fm.get("type") == "weekly_forecast"
        assert "week" in fm
        assert "macro_bias" in fm
        assert len(body) > 100

    def test_migrate_real_daily_validation(self):
        """Parse the real 2026-05-26.md if it exists."""
        path = Path("forecasts/daily/xauusd/2026-05-26.md")
        if not path.exists():
            pytest.skip("Real validation file not found")

        fm, body = parse_frontmatter(path.read_text())
        assert fm.get("type") == "daily_validation"
        assert "date" in fm
        assert "validation_score" in fm
        assert len(body) > 100
