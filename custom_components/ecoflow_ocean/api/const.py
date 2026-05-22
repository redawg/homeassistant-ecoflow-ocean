"""EcoFlow IoT Developer API constants."""

# Regional API bases (see https://developer.ecoflow.com)
API_BASE_US = "https://api-a.ecoflow.com"
API_BASE_EU = "https://api-e.ecoflow.com"

IOT_CERT_PATH = "/iot-open/sign/certification"
IOT_DEVICE_LIST_PATH = "/iot-open/sign/device/list"
IOT_QUOTA_ALL_PATH = "/iot-open/sign/device/quota/all"

IOT_MIN_FETCH_INTERVAL_S = 60.0
QUOTA_HTTP_MIN_INTERVAL_S = 10.0
HTTP_RETRIES = 3
HTTP_RETRY_BACKOFF_S = 2.0

CONF_ACCESS_KEY = "access_key"
CONF_SECRET_KEY = "secret_key"
CONF_DEVICE_SN = "device_sn"
CONF_DEVICE_TYPE = "device_type"
CONF_PRODUCT_NAME = "product_name"
CONF_REGION = "region"

REGION_US = "us"
REGION_EU = "eu"

DEFAULT_SCAN_INTERVAL = 15


def api_base_for_region(region: str) -> str:
    """Return regional API host."""
    return API_BASE_EU if region == REGION_EU else API_BASE_US
