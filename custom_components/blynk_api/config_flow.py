"""Config flow for Blynk API."""
import logging
import voluptuous as vol
from typing import Any, Dict

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.schema_attribute_validator import cv_string

from .const import (
    DOMAIN,
    CONF_SERVER,
    CONF_TOKEN,
    DEFAULT_SERVER,
    CONF_SENSORS,
    CONF_SWITCHES,
    CONF_PIN,
    CONF_NAME,
)
from .api import BlynkApiClient

_LOGGER = logging.getLogger(__name__)

class BlynkApiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Blynk API."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "BlynkApiOptionsFlowHandler":
        """Get the options flow for this handler."""
        return BlynkApiOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            session = async_get_clientsession(self.hass)
            client = BlynkApiClient(
                token=user_input[CONF_TOKEN],
                server=user_input[CONF_SERVER],
                session=session
            )

            is_connected = await client.is_hardware_connected()
            if is_connected:
                await self.async_set_unique_id(user_input[CONF_TOKEN])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Blynk Device",
                    data=user_input
                )
            else:
                errors["base"] = "cannot_connect"

        DATA_SCHEMA = vol.Schema({
            vol.Required(CONF_TOKEN): str,
            vol.Optional(CONF_SERVER, default=DEFAULT_SERVER): str,
        })
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class BlynkApiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Blynk API."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        # We use a temporary dict to hold the options while editing
        self.options = dict(config_entry.options)
        self._sensors = self.options.get(CONF_SENSORS, [])
        self._switches = self.options.get(CONF_SWITCHES, [])

    async def async_step_init(self, user_input: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Manage the options."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["sensors", "switches"],
        )

    async def async_step_sensors(self, user_input: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Manage the sensors."""
        if user_input is not None:
            # Add new sensor
            if user_input.get(CONF_PIN) and user_input.get(CONF_NAME):
                self._sensors.append(
                    {CONF_PIN: user_input[CONF_PIN], CONF_NAME: user_input[CONF_NAME]}
                )
            
            # Remove selected sensors
            if user_input.get("remove_sensors"):
                self._sensors = [
                    s for s in self._sensors if s[CONF_PIN] not in user_input["remove_sensors"]
                ]

            self.options[CONF_SENSORS] = self._sensors
            return self.async_create_entry(title="", data=self.options)
        
        # Schema for removing existing sensors
        remove_schema = {
            vol.Optional("remove_sensors"): cv.multi_select(
                {s[CONF_PIN]: f"{s[CONF_NAME]} ({s[CONF_PIN]})" for s in self._sensors}
            )
        }
        
        # Schema for adding a new sensor
        add_schema = {
            vol.Optional(CONF_PIN): cv_string,
            vol.Optional(CONF_NAME): cv_string
        }

        return self.async_show_form(
            step_id="sensors",
            data_schema=vol.Schema({**remove_schema, **add_schema}),
            description_placeholders={"pins": ", ".join([s[CONF_PIN] for s in self._sensors]) or "none"},
        )

    async def async_step_switches(self, user_input: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Manage the switches."""
        if user_input is not None:
            # Add new switch
            if user_input.get(CONF_PIN) and user_input.get(CONF_NAME):
                self._switches.append(
                    {CONF_PIN: user_input[CONF_PIN], CONF_NAME: user_input[CONF_NAME]}
                )
            
            # Remove selected switches
            if user_input.get("remove_switches"):
                self._switches = [
                    s for s in self._switches if s[CONF_PIN] not in user_input["remove_switches"]
                ]

            self.options[CONF_SWITCHES] = self._switches
            return self.async_create_entry(title="", data=self.options)
        
        # Schema for removing existing switches
        remove_schema = {
            vol.Optional("remove_switches"): cv.multi_select(
                {s[CONF_PIN]: f"{s[CONF_NAME]} ({s[CONF_PIN]})" for s in self._switches}
            )
        }
        
        # Schema for adding a new switch
        add_schema = {
            vol.Optional(CONF_PIN): cv_string,
            vol.Optional(CONF_NAME): cv_string
        }

        return self.async_show_form(
            step_id="switches",
            data_schema=vol.Schema({**remove_schema, **add_schema}),
            description_placeholders={"pins": ", ".join([s[CONF_PIN] for s in self._switches]) or "none"},
        )

