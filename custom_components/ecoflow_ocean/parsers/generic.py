"""Generic quota field extraction for EcoFlow peripherals."""

from __future__ import annotations

import re
from typing import Any

from .utils import safe_float

_POWER_KEY_HINTS = ("pwr", "power", "watts", "watt")
_ENERGY_KEY_HINTS = ("energy", "watth", "kwh")
_SOC_KEY_HINTS = ("soc", "soh")
_STATE_KEY_HINTS = ("sta", "state", "status", "mode")


def _sanitize_key(key: str) -> str:
    key = key.replace("ems_change_report.", "").replace("pcs_change_report.", "")
    key = re.sub(r"[^a-zA-Z0-9]+", "_", key).strip("_").lower()
    return key[:48] if key else "field"


def parse_generic_quota(quota_data: dict[str, Any], *, prefix: str = "") -> dict[str, Any]:
    """Extract numeric and enum-like values from flat quota keys."""
    result: dict[str, Any] = {}
    for raw_key, value in quota_data.items():
        if not isinstance(raw_key, str) or raw_key.startswith("bp_addr."):
            continue
        key_lower = raw_key.lower()
        sanitized = _sanitize_key(raw_key)
        if prefix:
            sanitized = f"{prefix}_{sanitized}" if not sanitized.startswith(prefix) else sanitized

        if isinstance(value, (int, float)):
            result[sanitized] = float(value)
            continue
        if isinstance(value, str):
            fv = safe_float(value)
            if fv is not None:
                result[sanitized] = fv
            elif len(value) < 64:
                result[sanitized] = value
            continue
        if any(h in key_lower for h in _POWER_KEY_HINTS):
            fv = safe_float(value)
            if fv is not None:
                result[sanitized] = fv
    return result
