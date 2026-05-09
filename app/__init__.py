"""Ring Status - Nordschleife track status monitor."""

__version__ = "0.1.0"
__author__ = "Alejandro"

from app.app import get_track_state, check_track

__all__ = ["get_track_state", "check_track"]
