from app.config.settings import settings

def format_snapshot_url(year, month, day, hour, minute, second) -> str:
    """Format the snapshot URL with the given parameters."""
    return settings.IMG_BASE_URL.format(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second
    )