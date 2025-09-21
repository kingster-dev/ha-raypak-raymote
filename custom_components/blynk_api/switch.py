"""Platform for switch integration."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_SWITCHES, CONF_PIN, CONF_NAME
from .api import BlynkApiClient

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the blynk switches based on a config entry."""
    api_client: BlynkApiClient = hass.data[DOMAIN][entry.entry_id]
    
    # Get switches from options flow
    configured_switches = entry.options.get(CONF_SWITCHES, [])
    
    switches = [
        BlynkSwitch(api_client, switch_conf[CONF_PIN], switch_conf[CONF_NAME])
        for switch_conf in configured_switches
    ]
    async_add_entities(switches, update_before_add=True)


class BlynkSwitch(SwitchEntity):
    """Representation of a Blynk Switch."""

    def __init__(self, api_client: BlynkApiClient, pin: str, name: str):
        """Initialize the switch."""
        self._api = api_client
        self._pin = pin
        self._attr_name = name
        self._attr_unique_id = f"{api_client._token[:6]}_switch_{pin}"
        self._attr_is_on = False
        self._attr_device_info = {
            "identifiers": {(DOMAIN, api_client._token)},
            "name": "Blynk Device",
            "manufacturer": "Blynk",
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on."""
        if await self._api.update_pin_value(self._pin, 1):
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        if await self._api.update_pin_value(self._pin, 0):
            self._attr_is_on = False
            self.async_write_ha_state()

    async def async_update(self) -> None:
        """Fetch new state data for the switch."""
        value_array = await self._api.get_pin_value(self._pin)
        if value_array and len(value_array) > 0:
            self._attr_is_on = value_array[0] == "1"

