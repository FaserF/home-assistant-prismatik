"""Prismatik switch entities."""

from typing import Any, Callable, List, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .prismatik import PrismatikAPI
from .coordinator import PrismatikDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Callable[[List[SwitchEntity], bool], None],
) -> None:
    """Set up the Prismatik switch entities."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    config = data["config"]

    async_add_entities([PrismatikMoodlightSwitch(coordinator, config[CONF_NAME])], True)


class PrismatikMoodlightSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of Prismatik Moodlight mode."""

    def __init__(self, coordinator: PrismatikDataUpdateCoordinator, name: str) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._client = coordinator.client
        self._attr_name = f"{name} Moodlight Mode"

        host = self._client.host.replace(".", "_")
        light_unique_id = f"{host}_{self._client.port}"
        self._attr_unique_id = f"{light_unique_id}_moodlight"

        self._attr_icon = "mdi:lightbulb-multiple"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, light_unique_id)},
        }

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if moodlight mode is on."""
        return self.coordinator.data.get("mode") == PrismatikAPI.MOD_MOODLIGHT

    @property
    def available(self) -> bool:
        """Return availability."""
        return self.coordinator.last_update_success and self._client.is_connected

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on moodlight mode."""
        if await self._client._set_cmd(
            PrismatikAPI.CMD_SET_MODE, PrismatikAPI.MOD_MOODLIGHT
        ):
            await self._client.unlock()
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off moodlight mode."""
        data = self.hass.data[DOMAIN]
        # Find config to get profile name
        profile = None
        for entry_id, entry_data in data.items():
            if entry_data["client"] == self._client:
                profile = entry_data["config"].get("profile_name")
                break

        if profile:
            await self._client.set_profile(profile)

        await self._client.unlock()

        await self.coordinator.async_request_refresh()
