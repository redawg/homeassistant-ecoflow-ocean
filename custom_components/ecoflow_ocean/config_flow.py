"""Config flow for EcoFlow Ocean (Developer API)."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .api import API_BASE_EU, API_BASE_US, IoTApiClient, api_base_for_region
from .api.const import (
    CONF_ACCESS_KEY,
    CONF_DEVICE_SN,
    CONF_REGION,
    CONF_SECRET_KEY,
    DEFAULT_SCAN_INTERVAL,
    REGION_EU,
    REGION_US,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def _device_label(device: dict[str, Any]) -> str:
    name = device.get("deviceName") or device.get("productName") or "EcoFlow device"
    sn = device.get("sn", "")
    online = "online" if device.get("online") else "offline"
    return f"{name} ({sn}) — {online}"


class EcoFlowOceanConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle EcoFlow Ocean setup via Developer API keys."""

    VERSION = 1

    def __init__(self) -> None:
        self._access_key = ""
        self._secret_key = ""
        self._region = REGION_US
        self._devices: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Collect API credentials and region."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._access_key = user_input[CONF_ACCESS_KEY].strip()
            self._secret_key = user_input[CONF_SECRET_KEY].strip()
            self._region = user_input[CONF_REGION]

            session = async_get_clientsession(self.hass)
            api = IoTApiClient(
                session,
                self._access_key,
                self._secret_key,
                api_base_for_region(self._region),
            )
            try:
                creds = await api.get_mqtt_credentials()
                if creds is None:
                    errors["base"] = "invalid_auth"
                else:
                    devices = await api.get_device_list()
                    if not devices:
                        errors["base"] = "no_devices"
                    else:
                        self._devices = devices
                        return await self.async_step_device()
            except (aiohttp.ClientError, TimeoutError, OSError):
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error validating EcoFlow API credentials")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ACCESS_KEY): str,
                    vol.Required(CONF_SECRET_KEY): str,
                    vol.Required(CONF_REGION, default=REGION_US): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(value=REGION_US, label="United States"),
                                SelectOptionDict(value=REGION_EU, label="Europe"),
                            ],
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                }
            ),
            errors=errors,
            description_placeholders={
                "docs_url": "https://developer.ecoflow.com/us/document/introduction",
                "api_us": API_BASE_US,
                "api_eu": API_BASE_EU,
            },
        )

    async def async_step_device(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Select the PowerOcean device serial number."""
        errors: dict[str, str] = {}

        options = {
            device["sn"]: _device_label(device)
            for device in self._devices
            if device.get("sn")
        }

        if user_input is not None:
            sn = user_input[CONF_DEVICE_SN]
            await self.async_set_unique_id(sn)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"EcoFlow Ocean ({sn})",
                data={
                    CONF_ACCESS_KEY: self._access_key,
                    CONF_SECRET_KEY: self._secret_key,
                    CONF_REGION: self._region,
                    CONF_DEVICE_SN: sn,
                },
                options={},
            )

        if not options:
            return self.async_abort(reason="no_devices")

        return self.async_show_form(
            step_id="device",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_SN): SelectSelector(
                        SelectSelectorConfig(options=options, mode=SelectSelectorMode.DROPDOWN)
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> EcoFlowOceanOptionsFlow:
        return EcoFlowOceanOptionsFlow()


class EcoFlowOceanOptionsFlow(OptionsFlow):
    """Options flow for poll interval."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        interval = self.config_entry.options.get(
            "scan_interval", DEFAULT_SCAN_INTERVAL
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional("scan_interval", default=interval): vol.All(
                        int, vol.Range(min=10, max=120)
                    ),
                }
            ),
        )
