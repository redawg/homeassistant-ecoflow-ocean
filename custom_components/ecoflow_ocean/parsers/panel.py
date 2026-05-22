"""Parse Smart Electrical Panel quota responses."""

from __future__ import annotations

from typing import Any

from .utils import safe_float
from .generic import parse_generic_quota
from .powerocean import parse_powerocean_quota


def parse_panel_quota(quota_data: dict[str, Any]) -> dict[str, Any]:
    """Parse panel load/circuit data; falls back to shared EMS fields."""
    result = parse_powerocean_quota(quota_data)

    mappings = (
        ("panelPwr", "panel_power"),
        ("panelLoadPwr", "panel_load_power"),
        ("cirLoadPwr", "circuit_load_power"),
        ("mainLoadPwr", "main_load_power"),
        ("backupLoadPwr", "backup_load_power"),
        ("gridRelaySta", "grid_relay_state"),
        ("panelSta", "panel_state"),
    )
    for http_key, sensor_key in mappings:
        if http_key in quota_data:
            value = safe_float(quota_data[http_key])
            if value is not None:
                result[sensor_key] = value
            else:
                result[sensor_key] = quota_data[http_key]

    for key, value in quota_data.items():
        if not isinstance(key, str):
            continue
        key_lower = key.lower()
        if "cir" in key_lower and ("pwr" in key_lower or "power" in key_lower):
            fv = safe_float(value)
            if fv is not None:
                safe_name = key.replace(".", "_").lower()
                result[f"panel_{safe_name}"] = fv

    generic = parse_generic_quota(quota_data, prefix="panel")
    for key, value in generic.items():
        result.setdefault(key, value)

    return result
