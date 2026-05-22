"""Data coordinator for EcoFlow Ocean cloud polling."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EcoFlowHTTPQuota, api_base_for_region
from .api.const import CONF_ACCESS_KEY, CONF_DEVICE_SN, CONF_REGION, CONF_SECRET_KEY, REGION_US
from .const import DOMAIN
from .parsers.powerocean import parse_powerocean_quota

_LOGGER = logging.getLogger(__name__)


class EcoFlowOceanCoordinator(DataUpdateCoordinator[dict]):
    """Poll EcoFlow Developer API quota for a PowerOcean device."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry_data: dict,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self._access_key = entry_data[CONF_ACCESS_KEY]
        self._secret_key = entry_data[CONF_SECRET_KEY]
        self._device_sn = entry_data[CONF_DEVICE_SN]
        self._region = entry_data.get(CONF_REGION, REGION_US)
        self._base_url = api_base_for_region(self._region)
        session = async_get_clientsession(hass)
        self._quota = EcoFlowHTTPQuota(
            session,
            self._access_key,
            self._secret_key,
            self._device_sn,
            self._base_url,
        )

    @property
    def device_sn(self) -> str:
        return self._device_sn

    async def _async_update_data(self) -> dict:
        raw = await self._quota.get_quota_all()
        if raw is None:
            code = self._quota.last_error_code or "unknown"
            raise UpdateFailed(f"EcoFlow API quota request failed (code={code})")
        parsed = parse_powerocean_quota(raw)
        parsed["device_sn"] = self._device_sn
        return parsed
