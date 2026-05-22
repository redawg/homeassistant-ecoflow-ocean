"""Shared parser helpers (no imports from sibling parser modules)."""


def safe_float(value) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
