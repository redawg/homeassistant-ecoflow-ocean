"""Quota response parsers."""

from __future__ import annotations

from typing import Any

from ..device_types import (
    DEVICE_TYPE_EV_CHARGER,
    DEVICE_TYPE_INVERTER,
    DEVICE_TYPE_OCEAN_PRO,
    DEVICE_TYPE_PANEL,
    DEVICE_TYPE_POWER_INSIGHT,
    DEVICE_TYPE_POWEROCEAN,
    DEVICE_TYPE_UNKNOWN,
)
from .ev_charger import parse_ev_charger_quota
from .generic import parse_generic_quota
from .panel import parse_panel_quota
from .power_insight import parse_power_insight_quota
from .powerocean import parse_powerocean_quota


def parse_device_quota(device_type: str, quota_data: dict[str, Any]) -> dict[str, Any]:
    """Route quota payload to the correct device parser."""
    if device_type in (
        DEVICE_TYPE_POWEROCEAN,
        DEVICE_TYPE_OCEAN_PRO,
        DEVICE_TYPE_INVERTER,
        DEVICE_TYPE_UNKNOWN,
    ):
        parsed = parse_powerocean_quota(quota_data)
    elif device_type == DEVICE_TYPE_EV_CHARGER:
        parsed = parse_ev_charger_quota(quota_data)
    elif device_type == DEVICE_TYPE_PANEL:
        parsed = parse_panel_quota(quota_data)
    elif device_type == DEVICE_TYPE_POWER_INSIGHT:
        parsed = parse_power_insight_quota(quota_data)
    else:
        parsed = parse_powerocean_quota(quota_data)

    if device_type == DEVICE_TYPE_OCEAN_PRO:
        parsed["system_variant"] = "ocean_pro"

    parsed["device_type"] = device_type
    return parsed
