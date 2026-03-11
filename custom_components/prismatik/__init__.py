"""
Prismatik integration.
https://github.com/psieg/Lightpack
"""

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_API_KEY,
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    Platform,
)
from .const import DOMAIN
from .coordinator import PrismatikDataUpdateCoordinator
from .prismatik import PrismatikClient

PLATFORMS = [
    Platform.LIGHT,
    Platform.NUMBER,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SWITCH,
]


async def async_setup(hass, config):
    """Set up the Prismatik integration."""
    conf = config.get(DOMAIN)
    if conf is not None:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
            )
        )

    return True


async def async_setup_entry(hass, entry):
    """Set up Prismatik platform."""
    config = dict(entry.data)
    if entry.options:
        config.update(entry.options)
        hass.config_entries.async_update_entry(entry, data=config, options={})

    client = PrismatikClient(
        config[CONF_HOST], config[CONF_PORT], config.get(CONF_API_KEY)
    )

    coordinator = PrismatikDataUpdateCoordinator(hass, client, config[CONF_NAME])
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "config": config,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
