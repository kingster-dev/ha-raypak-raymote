"""Platform for sensor integration."""
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_SENSORS, CONF_PIN, CONF_NAME
from .api import BlynkApiClient

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the blynk sensors based on a config entry."""
    api_client: BlynkApiClient = hass.data[DOMAIN][entry.entry_id]
    
    # Get sensors from options flow
    configured_sensors = entry.options.get(CONF_SENSORS, [])
    
    sensors = [
        BlynkSensor(api_client, sensor_conf[CONF_PIN], sensor_conf[CONF_NAME])
        for sensor_conf in configured_sensors
    ]
    async_add_entities(sensors, update_before_add=True)


class BlynkSensor(SensorEntity):
    """Representation of a Blynk Sensor."""

    def __init__(self, api_client: BlynkApiClient, pin: str, name: str):
        """Initialize the sensor."""
        self._api = api_client
        self._pin = pin
        self._attr_name = name
        # Use the config entry's unique ID in the sensor's unique ID
        self._attr_unique_id = f"{api_client._token[:6]}_sensor_{pin}"
        self._attr_native_value = None
        self._attr_device_info = {
            "identifiers": {(DOMAIN, api_client._token)},
            "name": "Blynk Device",
            "manufacturer": "Blynk",
        }

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        value_array = await self._api.get_pin_value(self._pin)
        if value_array and len(value_array) > 0:
            self._attr_native_value = value_array[0]
        else:
            self._attr_native_value = None

