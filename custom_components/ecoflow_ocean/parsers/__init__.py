"""Quota response parsers."""


def safe_float(value) -> float | None:
    """Convert API values to float when possible."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
