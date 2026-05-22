"""EcoFlow Developer API helpers."""

from .cloud_http import EcoFlowHTTPQuota
from .const import API_BASE_EU, API_BASE_US, REGION_EU, REGION_US
from .iot_api import IoTApiClient


def api_base_for_region(region: str) -> str:
    """Return regional API host."""
    return API_BASE_EU if region == REGION_EU else API_BASE_US


__all__ = [
    "API_BASE_EU",
    "API_BASE_US",
    "EcoFlowHTTPQuota",
    "IoTApiClient",
    "api_base_for_region",
]
