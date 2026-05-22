"""EcoFlow USA full-system device classification."""

from __future__ import annotations

from typing import Any

DEVICE_TYPE_OCEAN_PRO = "ocean_pro"
DEVICE_TYPE_POWEROCEAN = "powerocean"
DEVICE_TYPE_INVERTER = "inverter"
DEVICE_TYPE_PANEL = "smart_panel"
DEVICE_TYPE_EV_CHARGER = "ev_charger"
DEVICE_TYPE_POWER_INSIGHT = "power_insight"
DEVICE_TYPE_UNKNOWN = "unknown"

HACS_DISPLAY_NAME = (
    "Ecoflow Ocean USA - full system (Panel,Inverter, Batteries, EV charger, Power insight)"
)

SUPPORTED_DEVICE_TYPES = frozenset(
    {
        DEVICE_TYPE_OCEAN_PRO,
        DEVICE_TYPE_POWEROCEAN,
        DEVICE_TYPE_INVERTER,
        DEVICE_TYPE_PANEL,
        DEVICE_TYPE_EV_CHARGER,
        DEVICE_TYPE_POWER_INSIGHT,
        DEVICE_TYPE_UNKNOWN,
    }
)

_DEVICE_LABELS: dict[str, str] = {
    DEVICE_TYPE_OCEAN_PRO: "OCEAN Pro (Inverter + Batteries)",
    DEVICE_TYPE_POWEROCEAN: "PowerOcean / OCEAN (Inverter + Batteries)",
    DEVICE_TYPE_INVERTER: "Hybrid Inverter",
    DEVICE_TYPE_PANEL: "Smart Electrical Panel",
    DEVICE_TYPE_EV_CHARGER: "OCEAN EV Charger",
    DEVICE_TYPE_POWER_INSIGHT: "PowerInsight",
    DEVICE_TYPE_UNKNOWN: "EcoFlow Device",
}

_MODEL_NAMES: dict[str, str] = {
    DEVICE_TYPE_OCEAN_PRO: "EcoFlow OCEAN Pro",
    DEVICE_TYPE_POWEROCEAN: "EcoFlow PowerOcean",
    DEVICE_TYPE_INVERTER: "EcoFlow OCEAN Inverter",
    DEVICE_TYPE_PANEL: "EcoFlow Smart Electrical Panel",
    DEVICE_TYPE_EV_CHARGER: "EcoFlow OCEAN EV Charger",
    DEVICE_TYPE_POWER_INSIGHT: "EcoFlow PowerInsight",
    DEVICE_TYPE_UNKNOWN: "EcoFlow Device",
}

_OCEAN_KEYWORDS = (
    "powerocean",
    "power ocean",
    "ocean pro",
    "ocean plus",
    "ocean fit",
    "ocean dc",
)
_OCEAN_PRO_KEYWORDS = ("ocean pro", "powerocean pro", "oceanpro")
_PANEL_KEYWORDS = (
    "smart panel",
    "smart home panel",
    "electrical panel",
    "ocean panel",
    "shp2",
    "panel 40",
    "panel 30",
    "smart electrical",
)
_EV_KEYWORDS = (
    "ev charger",
    "ev-charger",
    "powerpulse",
    "ocean ev",
    "charger 11",
    "11.5kw",
)
_INSIGHT_KEYWORDS = ("powerinsight", "power insight", "power-insight")
_INVERTER_KEYWORDS = ("inverter", "hybrid inv", "pcs")

_SN_PREFIX_MAP: dict[str, str] = {
    "HJ31": DEVICE_TYPE_POWEROCEAN,
    "HJ32": DEVICE_TYPE_POWEROCEAN,
    "HJ33": DEVICE_TYPE_OCEAN_PRO,
    "PO11": DEVICE_TYPE_POWEROCEAN,
    "PO31": DEVICE_TYPE_POWEROCEAN,
    "POPL": DEVICE_TYPE_OCEAN_PRO,
    "POFI": DEVICE_TYPE_POWEROCEAN,
    "POPR": DEVICE_TYPE_OCEAN_PRO,
    "SP40": DEVICE_TYPE_PANEL,
    "SP30": DEVICE_TYPE_PANEL,
    "SHP2": DEVICE_TYPE_PANEL,
    "EV11": DEVICE_TYPE_EV_CHARGER,
    "EVC1": DEVICE_TYPE_EV_CHARGER,
    "PPI1": DEVICE_TYPE_POWER_INSIGHT,
    "PIN1": DEVICE_TYPE_POWER_INSIGHT,
}


def classify_device(device: dict[str, Any]) -> str:
    """Classify an API device list entry."""
    product = (
        device.get("productName")
        or device.get("deviceName")
        or device.get("name")
        or ""
    )
    sn = str(device.get("sn") or "")
    return get_device_type(product, sn)


def get_device_type(product_name: str, sn: str = "") -> str:
    """Return device type from product name and optional serial prefix."""
    name = product_name.lower()

    for keyword in _INSIGHT_KEYWORDS:
        if keyword in name:
            return DEVICE_TYPE_POWER_INSIGHT
    for keyword in _EV_KEYWORDS:
        if keyword in name:
            return DEVICE_TYPE_EV_CHARGER
    for keyword in _PANEL_KEYWORDS:
        if keyword in name:
            return DEVICE_TYPE_PANEL
    for keyword in _OCEAN_PRO_KEYWORDS:
        if keyword in name:
            return DEVICE_TYPE_OCEAN_PRO
    for keyword in _OCEAN_KEYWORDS:
        if keyword in name:
            return DEVICE_TYPE_POWEROCEAN
    for keyword in _INVERTER_KEYWORDS:
        if keyword in name:
            return DEVICE_TYPE_INVERTER

    if sn:
        prefix = sn[:4].upper()
        if prefix in _SN_PREFIX_MAP:
            return _SN_PREFIX_MAP[prefix]

    return DEVICE_TYPE_UNKNOWN


def device_type_label(device_type: str) -> str:
    return _DEVICE_LABELS.get(device_type, _DEVICE_LABELS[DEVICE_TYPE_UNKNOWN])


def device_model_name(device_type: str, product_name: str = "") -> str:
    if product_name and device_type == DEVICE_TYPE_UNKNOWN:
        return product_name
    return _MODEL_NAMES.get(device_type, _MODEL_NAMES[DEVICE_TYPE_UNKNOWN])


def is_supported_device_type(device_type: str) -> bool:
    return device_type in SUPPORTED_DEVICE_TYPES


def config_flow_device_label(device: dict[str, Any]) -> str:
    """Human-readable label for device selection."""
    product = device.get("productName") or device.get("deviceName") or "EcoFlow"
    sn = device.get("sn", "")
    device_type = classify_device(device)
    type_label = device_type_label(device_type)
    online = "online" if device.get("online") else "offline"
    sn_short = f"{sn[:10]}…" if len(sn) > 10 else sn
    return f"{product} — {type_label} ({sn_short}) [{online}]"
