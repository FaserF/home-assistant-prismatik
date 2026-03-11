"""DataUpdateCoordinator for Prismatik integration."""

from datetime import timedelta
import logging
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.util.color as color_util

from .const import DOMAIN
from .prismatik import PrismatikAPI, PrismatikClient

_LOGGER = logging.getLogger(__name__)


class PrismatikDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Prismatik data."""

    def __init__(self, hass: HomeAssistant, client: PrismatikClient, name: str) -> None:
        """Initialize."""
        self.client = client
        self.name = name
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Prismatik."""
        try:
            if not self.client.is_reachable:
                await self.client.disconnect()  # Reset connection if not reachable

            is_on = await self.client.is_on()
            profile = await self.client.get_profile()
            profiles = await self.client.get_profiles()
            brightness = await self.client.get_brightness()
            rgb = await self.client.get_color()
            led_count = await self.client.leds()
            gamma = await self.client.get_gamma()
            smooth = await self.client.get_smooth()
            status_api = await self.client.get_api_status()
            mode = await self.client._get_cmd(PrismatikAPI.CMD_GET_MODE)

            return {
                "is_on": is_on,
                "profile": profile,
                "profiles": profiles,
                "brightness": round(brightness * 2.55)
                if brightness is not None
                else None,
                "hs_color": color_util.color_RGB_to_hs(*rgb) if rgb else None,
                "led_count": led_count,
                "gamma": gamma,
                "smoothness": smooth,
                "api_status": status_api,
                "mode": mode,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
