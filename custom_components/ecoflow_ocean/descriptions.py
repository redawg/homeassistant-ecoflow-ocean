"""Shared sensor entity description type."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntityDescription


@dataclass(frozen=True, kw_only=True)
class EcoFlowOceanSensorDescription(SensorEntityDescription):
    """Sensor description for EcoFlow Ocean entities."""
