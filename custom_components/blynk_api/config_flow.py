"""Config flow for Blynk API."""
import logging
import voluptuous as vol
from aiohttp import ClientSession

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_SERVER, CONF_TOKEN, DEFAULT_SERVER
from .api import BlynkApiClient

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_TOKEN): str,
    vol.Optional(CONF_SERVER, default=DEFAULT_SERVER): str,
})

class BlynkApiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Blynk API."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Create a temporary client to test the connection
            session = async_get_clientsession(self.hass)
            client = BlynkApiClient(
                token=user_input[CONF_TOKEN],
                server=user_input[CONF_SERVER],
                session=session
            )

            # Test the connection
            is_connected = await client.is_hardware_connected()
            if is_connected:
                # Set a unique ID to prevent duplicate entries
                await self.async_set_unique_id(user_input[CONF_TOKEN])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="Blynk Device",
                    data=user_input
                )
            else:
                errors["base"] = "cannot_connect"

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
