"""Prismatik button entities."""

from typing import Callable, List

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PrismatikDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Callable[[List[ButtonEntity], bool], None],
) -> None:
    """Set up the Prismatik button entities."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    config = data["config"]

    async_add_entities(
        [
            PrismatikLockButton(coordinator, config[CONF_NAME]),
            PrismatikUnlockButton(coordinator, config[CONF_NAME]),
        ],
        True,
    )


class PrismatikButton(CoordinatorEntity, ButtonEntity):
    """Base class for Prismatik button entities."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator)
        self._client = coordinator.client

        host = self._client.host.replace(".", "_")
        light_unique_id = f"{host}_{self._client.port}"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, light_unique_id)},
        }

    @property
    def available(self) -> bool:
        """Return availability."""
        return self.coordinator.last_update_success and self._client.is_connected


class PrismatikLockButton(PrismatikButton):
    """Button to lock Prismatik API."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the lock button."""
        super().__init__(coordinator, name)
        self._attr_name = f"{name} Lock API"

        host = self._client.host.replace(".", "_")
        self._attr_unique_id = f"{host}_{self._client.port}_lock"
        self._attr_icon = "mdi:lock-outline"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._client.lock()
        await self.coordinator.async_request_refresh()


class PrismatikUnlockButton(PrismatikButton):
    """Button to unlock Prismatik API."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the unlock button."""
        super().__init__(coordinator, name)
        self._attr_name = f"{name} Unlock API"

        host = self._client.host.replace(".", "_")
        self._attr_unique_id = f"{host}_{self._client.port}_unlock"
        self._attr_icon = "mdi:lock-open-variant-outline"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._client.unlock()
        await self.coordinator.async_request_refresh()
