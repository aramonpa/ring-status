"""Tests for the app module."""

import pytest
from app.api.app import is_weekend, format_snapshot_url
from datetime import datetime


class TestIsWeekend:
    """Tests for the is_weekend function."""

    def test_monday_is_not_weekend(self):
        """Monday is not a weekend."""
        # 2026-05-11 is a Monday
        dt = datetime(2026, 5, 11)
        assert not is_weekend(dt)

    def test_saturday_is_weekend(self):
        """Saturday is a weekend."""
        # 2026-05-09 is a Saturday
        dt = datetime(2026, 5, 9)
        assert is_weekend(dt)

    def test_sunday_is_weekend(self):
        """Sunday is a weekend."""
        # 2026-05-10 is a Sunday
        dt = datetime(2026, 5, 10)
        assert is_weekend(dt)


class TestFormatSnapshotUrl:
    """Tests for the format_snapshot_url function."""

    def test_url_formatting(self):
        """Verify that the URL is formatted correctly."""
        url = format_snapshot_url(2026, 5, 9, 14, 30, 45)
        assert "2026" in url
        assert "05" in url or "5" in url
        assert "09" in url or "9" in url
        assert "14" in url
        assert "30" in url
        assert "45" in url
