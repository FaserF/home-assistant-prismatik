"""Prismatik binary sensor entities."""

from typing import Callable, List, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PrismatikDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Callable[[List[BinarySensorEntity], bool], None],
) -> None:
    """Set up the Prismatik binary sensor entities."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    config = data["config"]

    async_add_entities(
        [PrismatikAPIStatusBinarySensor(coordinator, config[CONF_NAME])], True
    )


class PrismatikAPIStatusBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of Prismatik API status (busy/idle)."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._client = coordinator.client
        self._attr_name = f"{name} API Busy"

        host = self._client.host.replace(".", "_")
        light_unique_id = f"{host}_{self._client.port}"
        self._attr_unique_id = f"{light_unique_id}_api_status"

        self._attr_icon = "mdi:progress-clock"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, light_unique_id)},
        }

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if API is busy."""
        return self.coordinator.data.get("api_status") == "busy"

    @property
    def available(self) -> bool:
        """Return availability."""
        return self.coordinator.last_update_success and self._client.is_connected
