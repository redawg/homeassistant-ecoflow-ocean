"""Parse PowerOcean GET /quota/all responses into sensor keys."""

from __future__ import annotations

import json
from typing import Any

from . import safe_float


def parse_powerocean_quota(quota_data: dict[str, Any]) -> dict[str, Any]:
    """Map EcoFlow quota fields to integration sensor keys."""
    result: dict[str, Any] = {}

    for http_key, sensor_key in (
        ("mpptPwr", "solar_power"),
        ("sysLoadPwr", "home_power"),
        ("sysGridPwr", "grid_power"),
        ("bpPwr", "battery_power"),
        ("bpSoc", "battery_soc"),
    ):
        if http_key in quota_data:
            value = safe_float(quota_data[http_key])
            if value is not None:
                result[sensor_key] = value

    grid = result.get("grid_power")
    if grid is not None:
        result["grid_import_power"] = grid if grid > 0 else 0.0
        result["grid_export_power"] = abs(grid) if grid < 0 else 0.0

    batt = result.get("battery_power")
    if batt is not None:
        result["battery_charge_power"] = batt if batt > 0 else 0.0
        result["battery_discharge_power"] = abs(batt) if batt < 0 else 0.0

    _extract_battery_pack(quota_data, result)
    _extract_energy_totals(quota_data, result)

    if "pcs_change_report.gridFreq" in quota_data:
        freq = safe_float(quota_data["pcs_change_report.gridFreq"])
        if freq is not None:
            result["grid_frequency"] = freq

    mppt_hb = quota_data.get("mpptHeartBeat")
    if isinstance(mppt_hb, list) and mppt_hb and isinstance(mppt_hb[0], dict):
        pvs = mppt_hb[0].get("mpptPv")
        if isinstance(pvs, list):
            for index, pv in enumerate(pvs[:3], start=1):
                if not isinstance(pv, dict):
                    continue
                for field, suffix in (
                    ("pwr", "power"),
                    ("vol", "voltage"),
                    ("amp", "current"),
                ):
                    if field in pv:
                        val = safe_float(pv[field])
                        if val is not None:
                            result[f"pv_string_{index}_{suffix}"] = val

    return result


def _extract_battery_pack(quota_data: dict[str, Any], result: dict[str, Any]) -> None:
    for key, val in quota_data.items():
        if not key.startswith("bp_addr.") or key == "bp_addr.updateTime":
            continue
        if isinstance(val, str):
            try:
                val = json.loads(val)
            except (json.JSONDecodeError, TypeError):
                continue
        if not isinstance(val, dict):
            continue
        for http_key, sensor_key in (
            ("bpSoh", "battery_soh"),
            ("bpVol", "battery_voltage"),
            ("bpAmp", "battery_current"),
            ("bpMaxCellTemp", "battery_max_cell_temp"),
            ("bpRemainWatth", "battery_remaining_wh"),
        ):
            if http_key in val:
                parsed = safe_float(val[http_key])
                if parsed is not None:
                    result[sensor_key] = parsed
        break


def _extract_energy_totals(quota_data: dict[str, Any], result: dict[str, Any]) -> None:
    energy_map = {
        "energy_stream.solarTotalEnergy": "solar_energy_total",
        "energy_stream.homeTotalEnergy": "home_energy_total",
        "energy_stream.gridInTotalEnergy": "grid_import_energy_total",
        "energy_stream.gridOutTotalEnergy": "grid_export_energy_total",
        "energy_stream.bpChgTotalEnergy": "battery_charge_energy_total",
        "energy_stream.bpDsgTotalEnergy": "battery_discharge_energy_total",
    }
    for http_key, sensor_key in energy_map.items():
        if http_key in quota_data:
            value = safe_float(quota_data[http_key])
            if value is not None:
                result[sensor_key] = round(value / 1000.0, 3)
