"""Parse PowerInsight hub quota responses."""

from __future__ import annotations

from typing import Any

from .generic import parse_generic_quota
from .powerocean import parse_powerocean_quota


def parse_power_insight_quota(quota_data: dict[str, Any]) -> dict[str, Any]:
    """PowerInsight often mirrors system-level power totals."""
    result = parse_powerocean_quota(quota_data)
    generic = parse_generic_quota(quota_data, prefix="insight")
    for key, value in generic.items():
        result.setdefault(key, value)
    return result
