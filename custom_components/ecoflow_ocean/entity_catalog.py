"""Sensor entity catalog per EcoFlow device type."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)

from .device_types import (
    DEVICE_TYPE_EV_CHARGER,
    DEVICE_TYPE_OCEAN_PRO,
    DEVICE_TYPE_PANEL,
    DEVICE_TYPE_POWER_INSIGHT,
    DEVICE_TYPE_POWEROCEAN,
    DEVICE_TYPE_UNKNOWN,
)
from .descriptions import EcoFlowOceanSensorDescription

# --- Inverter / battery / OCEAN Pro (shared quota shape) ---

_INVERTER_BATTERY_SENSORS: tuple[EcoFlowOceanSensorDescription, ...] = (
    EcoFlowOceanSensorDescription(
        key="battery_soc",
        translation_key="battery_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_power",
        translation_key="battery_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_charge_power",
        translation_key="battery_charge_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_discharge_power",
        translation_key="battery_discharge_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="solar_power",
        translation_key="solar_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
    ),
    EcoFlowOceanSensorDescription(
        key="home_power",
        translation_key="home_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-lightning-bolt",
    ),
    EcoFlowOceanSensorDescription(
        key="grid_power",
        translation_key="grid_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower",
    ),
    EcoFlowOceanSensorDescription(
        key="grid_import_power",
        translation_key="grid_import_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="grid_export_power",
        translation_key="grid_export_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="grid_frequency",
        translation_key="grid_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_voltage",
        translation_key="battery_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_current",
        translation_key="battery_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_soh",
        translation_key="battery_soh",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-heart",
    ),
    EcoFlowOceanSensorDescription(
        key="battery_max_cell_temp",
        translation_key="battery_max_cell_temp",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="solar_energy_total",
        translation_key="solar_energy_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EcoFlowOceanSensorDescription(
        key="home_energy_total",
        translation_key="home_energy_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EcoFlowOceanSensorDescription(
        key="grid_import_energy_total",
        translation_key="grid_import_energy_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EcoFlowOceanSensorDescription(
        key="grid_export_energy_total",
        translation_key="grid_export_energy_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_charge_energy_total",
        translation_key="battery_charge_energy_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EcoFlowOceanSensorDescription(
        key="battery_discharge_energy_total",
        translation_key="battery_discharge_energy_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
)

_EV_SENSORS: tuple[EcoFlowOceanSensorDescription, ...] = (
    EcoFlowOceanSensorDescription(
        key="ev_charge_power",
        translation_key="ev_charge_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ev-station",
    ),
    EcoFlowOceanSensorDescription(
        key="ev_voltage",
        translation_key="ev_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ev-plug-type2",
    ),
    EcoFlowOceanSensorDescription(
        key="ev_current",
        translation_key="ev_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EcoFlowOceanSensorDescription(
        key="ev_session_energy_kwh",
        translation_key="ev_session_energy_kwh",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EcoFlowOceanSensorDescription(
        key="ev_charge_state",
        translation_key="ev_charge_state",
        icon="mdi:car-electric",
    ),
    EcoFlowOceanSensorDescription(
        key="ev_work_mode",
        translation_key="ev_work_mode",
        icon="mdi:car-cog",
    ),
)

_PANEL_SENSORS: tuple[EcoFlowOceanSensorDescription, ...] = (
    EcoFlowOceanSensorDescription(
        key="panel_power",
        translation_key="panel_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:view-dashboard",
    ),
    EcoFlowOceanSensorDescription(
        key="panel_load_power",
        translation_key="panel_load_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-lightning-bolt",
    ),
    EcoFlowOceanSensorDescription(
        key="circuit_load_power",
        translation_key="circuit_load_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:electric-switch",
    ),
    EcoFlowOceanSensorDescription(
        key="panel_state",
        translation_key="panel_state",
        icon="mdi:electric-switch-closed",
    ),
)

_INSIGHT_SENSORS: tuple[EcoFlowOceanSensorDescription, ...] = _INVERTER_BATTERY_SENSORS

_SENSOR_MAP: dict[str, tuple[EcoFlowOceanSensorDescription, ...]] = {
    DEVICE_TYPE_POWEROCEAN: _INVERTER_BATTERY_SENSORS,
    DEVICE_TYPE_OCEAN_PRO: _INVERTER_BATTERY_SENSORS,
    DEVICE_TYPE_INVERTER: _INVERTER_BATTERY_SENSORS,
    DEVICE_TYPE_PANEL: _INVERTER_BATTERY_SENSORS + _PANEL_SENSORS,
    DEVICE_TYPE_EV_CHARGER: _INVERTER_BATTERY_SENSORS + _EV_SENSORS,
    DEVICE_TYPE_POWER_INSIGHT: _INSIGHT_SENSORS,
    DEVICE_TYPE_UNKNOWN: _INVERTER_BATTERY_SENSORS,
}


def get_sensor_descriptions(device_type: str) -> tuple[EcoFlowOceanSensorDescription, ...]:
    """Return sensor entities for a classified device type."""
    return _SENSOR_MAP.get(device_type, _INVERTER_BATTERY_SENSORS)
