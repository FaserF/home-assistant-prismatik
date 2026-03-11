"""Prismatik light entity."""

from typing import Any, Callable, Dict, List, Optional

import homeassistant.util.color as color_util
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_NAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DEFAULT_ICON_OFF,
    DEFAULT_ICON_ON,
    DOMAIN,
)
from .coordinator import PrismatikDataUpdateCoordinator


async def async_setup_platform(
    hass: HomeAssistant,
    config: Dict[str, Any],
    async_add_entities: Callable[[List[LightEntity], bool], None],
    discovery_info: Optional[Any] = None,
) -> None:
    """Set up the Prismatik Light platform from legacy YAML (deprecated)."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        "deprecated_yaml",
        is_fixable=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="deprecated_yaml",
    )

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=config
        )
    )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Callable[[List[LightEntity], bool], None],
) -> None:
    """Set up the Prismatik Light from a config entry."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    config = data["config"]

    async_add_entities([PrismatikLight(coordinator, config[CONF_NAME], config)], True)


class PrismatikLight(CoordinatorEntity, LightEntity):
    """Representation of a Prismatik light."""

    def __init__(
        self,
        coordinator: PrismatikDataUpdateCoordinator,
        name: str,
        config: Dict[str, Any],
    ) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._name = name
        self._client = coordinator.client
        self._profile = config.get("profile_name")

        host = self._client.host.replace(".", "_")
        self._attr_unique_id = f"{host}_{self._client.port}"
        self._attr_name = name
        self._attr_color_mode = ColorMode.HS
        self._attr_supported_color_modes = {ColorMode.HS}
        self._attr_supported_features = LightEntityFeature.EFFECT

        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": name,
            "manufacturer": "Prismatik",
            "model": "Ambient Light",
            "configuration_url": f"http://{self._client.host}:{self._client.port}",
        }

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self.coordinator.data.get("is_on", False)

    @property
    def brightness(self) -> Optional[int]:
        """Return the brightness of this light."""
        return self.coordinator.data.get("brightness")

    @property
    def hs_color(self) -> Optional[tuple]:
        """Return the hs color value."""
        return self.coordinator.data.get("hs_color")

    @property
    def effect_list(self) -> Optional[List[str]]:
        """Return the list of supported effects."""
        return self.coordinator.data.get("profiles")

    @property
    def effect(self) -> Optional[str]:
        """Return the current effect."""
        return self.coordinator.data.get("profile")

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self._client.is_connected

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return DEFAULT_ICON_ON if self.available else DEFAULT_ICON_OFF

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra state attributes."""
        return {
            "led_count": self.coordinator.data.get("led_count"),
            "gamma": self.coordinator.data.get("gamma"),
            "smoothness": self.coordinator.data.get("smoothness"),
            "api_status": self.coordinator.data.get("api_status"),
            "mode": self.coordinator.data.get("mode"),
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        await self._client.turn_on()
        if ATTR_EFFECT in kwargs:
            await self._client.set_profile(kwargs[ATTR_EFFECT])
        elif ATTR_BRIGHTNESS in kwargs:
            await self._client.set_brightness(
                round(kwargs[ATTR_BRIGHTNESS] / 2.55), self._profile
            )
        elif ATTR_HS_COLOR in kwargs:
            rgb = color_util.color_hs_to_RGB(*kwargs[ATTR_HS_COLOR])
            await self._client.set_color(rgb, self._profile)
        await self._client.unlock()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self._client.turn_off()
        await self.coordinator.async_request_refresh()
