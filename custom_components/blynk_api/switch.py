"""Platform for switch integration."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .api import BlynkApiClient

_LOGGER = logging.getLogger(__name__)

# This is a sample list of switches. In a more advanced version,
# this would be configured via an options flow in the UI.
Blynk_SWITCHES = {
    "D2": "Digital Pin 2",
    "D3": "Digital Pin 3",
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the blynk switches."""
    api_client: BlynkApiClient = hass.data[DOMAIN][entry.entry_id]
    
    switches = [
        BlynkSwitch(api_client, pin, name)
        for pin, name in Blynk_SWITCHES.items()
    ]
    async_add_entities(switches, update_before_add=True)


class BlynkSwitch(SwitchEntity):
    """Representation of a Blynk Switch."""

    def __init__(self, api_client: BlynkApiClient, pin: str, name: str):
        """Initialize the switch."""
        self._api = api_client
        self._pin = pin
        self._attr_name = f"Blynk {name}"
        self._attr_unique_id = f"blynk_switch_{api_client._token[:6]}_{pin}"
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on."""
        if await self._api.update_pin_value(self._pin, 1):
            self._attr_is_on = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        if await self._api.update_pin_value(self._pin, 0):
            self._attr_is_on = False

    async def async_update(self) -> None:
        """Fetch new state data for the switch."""
        value_array = await self._api.get_pin_value(self._pin)
        if value_array and len(value_array) > 0:
            self._attr_is_on = value_array[0] == "1"
