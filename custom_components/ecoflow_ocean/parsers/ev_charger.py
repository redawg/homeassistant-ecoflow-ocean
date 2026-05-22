"""Parse OCEAN EV Charger quota responses."""

from __future__ import annotations

from typing import Any

from . import safe_float
from .generic import parse_generic_quota
from .powerocean import parse_powerocean_quota


def parse_ev_charger_quota(quota_data: dict[str, Any]) -> dict[str, Any]:
    """Merge PowerOcean-style EMS data with EV-specific fields when present."""
    result = parse_powerocean_quota(quota_data)

    mappings = (
        ("evPwr", "ev_charge_power"),
        ("evChgPwr", "ev_charge_power"),
        ("chargerPower", "ev_charge_power"),
        ("evPower", "ev_charge_power"),
        ("evVol", "ev_voltage"),
        ("evAmp", "ev_current"),
        ("evChgVol", "ev_voltage"),
        ("evChgAmp", "ev_current"),
        ("evSoc", "ev_vehicle_soc"),
        ("gunTemp", "ev_gun_temperature"),
        ("evTemp", "ev_temperature"),
        ("evChgEnergy", "ev_session_energy_wh"),
        ("evChgTotalEnergy", "ev_total_energy_wh"),
    )
    for http_key, sensor_key in mappings:
        if http_key in quota_data:
            value = safe_float(quota_data[http_key])
            if value is not None:
                result[sensor_key] = value

    for http_key, sensor_key in (
        ("evWorkMode", "ev_work_mode"),
        ("evChgSta", "ev_charge_state"),
        ("gunSta", "ev_gun_state"),
        ("evConnSta", "ev_connection_state"),
    ):
        if http_key in quota_data:
            result[sensor_key] = str(quota_data[http_key])

    if "evChgEnergy" in quota_data:
        wh = safe_float(quota_data["evChgEnergy"])
        if wh is not None:
            result["ev_session_energy_kwh"] = round(wh / 1000.0, 3)

    generic = parse_generic_quota(quota_data, prefix="ev")
    for key, value in generic.items():
        result.setdefault(key, value)

    return result
