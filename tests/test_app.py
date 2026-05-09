"""Tests para el módulo app."""

import pytest
from app.app import is_weekend, format_snapshot_url
from datetime import datetime


class TestIsWeekend:
    """Tests para la función is_weekend."""

    def test_monday_is_not_weekend(self):
        """Lunes no es fin de semana."""
        # 2026-05-11 es un lunes
        dt = datetime(2026, 5, 11)
        assert not is_weekend(dt)

    def test_saturday_is_weekend(self):
        """Sábado es fin de semana."""
        # 2026-05-09 es un sábado
        dt = datetime(2026, 5, 9)
        assert is_weekend(dt)

    def test_sunday_is_weekend(self):
        """Domingo es fin de semana."""
        # 2026-05-10 es un domingo
        dt = datetime(2026, 5, 10)
        assert is_weekend(dt)


class TestFormatSnapshotUrl:
    """Tests para la función format_snapshot_url."""

    def test_url_formatting(self):
        """Verifica que la URL se formatea correctamente."""
        url = format_snapshot_url(2026, 5, 9, 14, 30, 45)
        assert "2026" in url
        assert "05" in url or "5" in url
        assert "09" in url or "9" in url
        assert "14" in url
        assert "30" in url
        assert "45" in url
