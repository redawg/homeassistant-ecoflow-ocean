"""Config flow for EcoFlow Ocean (Developer API)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .api.const import (
    API_BASE_EU,
    API_BASE_US,
    CONF_ACCESS_KEY,
    CONF_DEVICE_SN,
    CONF_DEVICE_TYPE,
    CONF_PRODUCT_NAME,
    CONF_REGION,
    CONF_SECRET_KEY,
    DEFAULT_SCAN_INTERVAL,
    REGION_EU,
    REGION_US,
    api_base_for_region,
)
from .const import DOMAIN

if TYPE_CHECKING:
    import aiohttp

_LOGGER = logging.getLogger(__name__)

# Display name only — keep out of device_types import at module load
_INTEGRATION_TITLE = (
    "Ecoflow Ocean USA - full system (Panel,Inverter, Batteries, EV charger, Power insight)"
)


class EcoFlowOceanConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle EcoFlow Ocean USA full-system setup via Developer API keys."""

    VERSION = 2

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

            # Lazy imports — avoid loading aiohttp/iot_api when HA imports config_flow
            from .api.iot_api import IoTApiClient

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
            except (TimeoutError, OSError):
                errors["base"] = "cannot_connect"
            except Exception as err:  # noqa: BLE001
                import aiohttp

                if isinstance(err, aiohttp.ClientError):
                    errors["base"] = "cannot_connect"
                else:
                    _LOGGER.exception(
                        "Unexpected error validating EcoFlow API credentials"
                    )
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
                "integration_name": _INTEGRATION_TITLE,
            },
        )

    async def async_step_device(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Select a device from the developer application."""
        from .device_types import (
            classify_device,
            config_flow_device_label,
            device_type_label,
        )

        errors: dict[str, str] = {}

        device_by_sn = {
            device["sn"]: device for device in self._devices if device.get("sn")
        }
        device_options = [
            SelectOptionDict(value=sn, label=config_flow_device_label(device))
            for sn, device in device_by_sn.items()
        ]

        if user_input is not None:
            sn = user_input[CONF_DEVICE_SN]
            device = device_by_sn.get(sn)
            if not device:
                errors["base"] = "unknown"
            else:
                device_type = classify_device(device)
                product_name = (
                    device.get("productName")
                    or device.get("deviceName")
                    or ""
                )
                await self.async_set_unique_id(sn)
                self._abort_if_unique_id_configured()

                type_label = device_type_label(device_type)
                return self.async_create_entry(
                    title=f"{type_label} ({sn[-6:]})",
                    data={
                        CONF_ACCESS_KEY: self._access_key,
                        CONF_SECRET_KEY: self._secret_key,
                        CONF_REGION: self._region,
                        CONF_DEVICE_SN: sn,
                        CONF_DEVICE_TYPE: device_type,
                        CONF_PRODUCT_NAME: product_name,
                    },
                    options={},
                )

        if not device_options:
            return self.async_abort(reason="no_devices")

        return self.async_show_form(
            step_id="device",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_SN): SelectSelector(
                        SelectSelectorConfig(
                            options=device_options,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                }
            ),
            errors=errors,
            description_placeholders={
                "supported": (
                    "OCEAN Pro, Inverter/Batteries, Smart Panel, EV Charger, PowerInsight"
                ),
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> EcoFlowOceanOptionsFlow:
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


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate v1 entries to store device type metadata."""
    if config_entry.version == 1:
        data = dict(config_entry.data)
        data.setdefault(CONF_DEVICE_TYPE, "powerocean")
        data.setdefault(CONF_PRODUCT_NAME, "")
        hass.config_entries.async_update_entry(
            config_entry,
            data=data,
            version=2,
        )
    return True
