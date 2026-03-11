"""Prismatik number entities."""

from typing import Callable, List, Optional

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PrismatikDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Callable[[List[NumberEntity], bool], None],
) -> None:
    """Set up the Prismatik number entities."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    config = data["config"]

    async_add_entities(
        [
            PrismatikGammaNumber(coordinator, config[CONF_NAME]),
            PrismatikSmoothnessNumber(coordinator, config[CONF_NAME]),
        ],
        True,
    )


class PrismatikNumber(CoordinatorEntity, NumberEntity):
    """Base class for Prismatik number entities."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the number entity."""
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


class PrismatikGammaNumber(PrismatikNumber):
    """Representation of Prismatik Gamma."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the gamma number."""
        super().__init__(coordinator, name)
        self._attr_name = f"{name} Gamma"

        host = self._client.host.replace(".", "_")
        self._attr_unique_id = f"{host}_{self._client.port}_gamma"

        self._attr_native_min_value = 0.1
        self._attr_native_max_value = 10.0
        self._attr_native_step = 0.1

    @property
    def native_value(self) -> Optional[float]:
        """Return current value."""
        return self.coordinator.data.get("gamma")

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        if await self._client.set_gamma(value):
            await self.coordinator.async_request_refresh()


class PrismatikSmoothnessNumber(PrismatikNumber):
    """Representation of Prismatik Smoothness."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the smoothness number."""
        super().__init__(coordinator, name)
        self._attr_name = f"{name} Smoothness"

        host = self._client.host.replace(".", "_")
        self._attr_unique_id = f"{host}_{self._client.port}_smoothness"

        self._attr_native_min_value = 0
        self._attr_native_max_value = 255
        self._attr_native_step = 1

    @property
    def native_value(self) -> Optional[float]:
        """Return current value."""
        return self.coordinator.data.get("smoothness")

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        if await self._client.set_smooth(int(value)):
            await self.coordinator.async_request_refresh()
