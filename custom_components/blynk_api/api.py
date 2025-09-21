"""A simple API client for Blynk."""
import logging
from aiohttp import ClientSession, ClientError

_LOGGER = logging.getLogger(__name__)

class BlynkApiClient:
    """Manages communication with the Blynk API."""

    def __init__(self, token: str, server: str, session: ClientSession):
        """Initialize the API client."""
        self._token = token
        self._server = server.rstrip('/')  # Remove trailing slash if present
        self._session = session
        self._base_url = f"{self._server}/{self._token}"

    async def get_pin_value(self, pin: str) -> list | None:
        """Get the value of a specific pin."""
        url = f"{self._base_url}/get/{pin}"
        try:
            async with self._session.get(url) as response:
                response.raise_for_status()
                # The API returns a JSON array, e.g., ["1024"]
                return await response.json()
        except ClientError as err:
            _LOGGER.error("Error getting pin %s: %s", pin, err)
            return None

    async def update_pin_value(self, pin: str, value: str | int) -> bool:
        """Update the value of a specific pin."""
        url = f"{self._base_url}/update/{pin}?value={value}"
        try:
            async with self._session.get(url) as response:
                response.raise_for_status()
                return True
        except ClientError as err:
            _LOGGER.error("Error updating pin %s: %s", pin, err)
            return False

    async def is_hardware_connected(self) -> bool:
        """Check if the hardware is connected to the server."""
        url = f"{self._base_url}/isHardwareConnected"
        try:
            async with self._session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except ClientError as err:
            _LOGGER.error("Error checking hardware status: %s", err)
            return False
