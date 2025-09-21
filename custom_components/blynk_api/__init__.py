"""The Blynk API integration."""
import logging
from aiohttp import ClientSession

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS
from .api import BlynkApiClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Blynk API from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create an API client
    session = async_get_clientsession(hass)
    api_client = BlynkApiClient(
        token=entry.data["token"],
        server=entry.data["server"],
        session=session
    )

    # Store the API client for platforms to use
    hass.data[DOMAIN][entry.entry_id] = api_client

    # Add an update listener to reload the integration when options change
    entry.async_on_unload(entry.add_update_listener(update_listener))

    # Forward the setup to the platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, PLATFORMS)

    # Clean up the hass.data entry
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    _LOGGER.debug("Reloading integration due to options update")
    await hass.config_entries.async_reload(entry.entry_id)

