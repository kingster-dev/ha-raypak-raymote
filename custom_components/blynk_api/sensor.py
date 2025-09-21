"""Platform for sensor integration."""
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .api import BlynkApiClient

_LOGGER = logging.getLogger(__name__)

# This is a sample list of sensors. In a more advanced version,
# this would be configured via an options flow in the UI.
Blynk_SENSORS = {
    "V0": "Virtual Pin 0",
    "V1": "Virtual Pin 1",
    "V5": "Temperature",
}

SCAN_INTERVAL = timedelta(seconds=30)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the blynk sensors."""
    api_client: BlynkApiClient = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        BlynkSensor(api_client, pin, name)
        for pin, name in Blynk_SENSORS.items()
    ]
    async_add_entities(sensors, update_before_add=True)


class BlynkSensor(SensorEntity):
    """Representation of a Blynk Sensor."""

    def __init__(self, api_client: BlynkApiClient, pin: str, name: str):
        """Initialize the sensor."""
        self._api = api_client
        self._pin = pin
        self._attr_name = f"Blynk {name}"
        self._attr_unique_id = f"blynk_sensor_{api_client._token[:6]}_{pin}"
        self._attr_native_value = None

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        value_array = await self._api.get_pin_value(self._pin)
        if value_array and len(value_array) > 0:
            self._attr_native_value = value_array[0]
        else:
            self._attr_native_value = None
