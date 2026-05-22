"""Sensor platform for EcoFlow Ocean."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api.const import CONF_DEVICE_SN, CONF_DEVICE_TYPE, CONF_PRODUCT_NAME
from .const import DOMAIN
from .coordinator import EcoFlowOceanCoordinator
from .descriptions import EcoFlowOceanSensorDescription
from .device_types import device_model_name, device_type_label
from .entity_catalog import get_sensor_descriptions


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: EcoFlowOceanCoordinator = hass.data[DOMAIN][entry.entry_id]
    device_type = entry.data.get(CONF_DEVICE_TYPE, coordinator.device_type)
    descriptions = get_sensor_descriptions(device_type)
    async_add_entities(
        EcoFlowOceanSensor(coordinator, description, entry) for description in descriptions
    )


class EcoFlowOceanSensor(CoordinatorEntity[EcoFlowOceanCoordinator], SensorEntity):
    """EcoFlow Ocean sensor fed by Developer API quota polling."""

    entity_description: EcoFlowOceanSensorDescription

    def __init__(
        self,
        coordinator: EcoFlowOceanCoordinator,
        description: EcoFlowOceanSensorDescription,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_has_entity_name = True

        device_type = entry.data.get(CONF_DEVICE_TYPE, coordinator.device_type)
        product_name = entry.data.get(CONF_PRODUCT_NAME, "")
        model = device_model_name(device_type, product_name)
        type_label = device_type_label(device_type)

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"{type_label}",
            manufacturer="EcoFlow",
            model=model,
            serial_number=entry.data.get(CONF_DEVICE_SN, coordinator.device_sn),
            labels={"ecoflow_ocean", f"ecoflow_{device_type}"},
        )

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key)
