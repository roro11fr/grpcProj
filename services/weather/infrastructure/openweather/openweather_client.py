from __future__ import annotations

import httpx

from services.weather.core import settings

from .openweather_processor import process_openweather_response
from .openweather_types import WeatherTuple
from .openweather_validators import validate_api_key


class OpenWeatherClient:
    """Async client for accessing current weather data from OpenWeatherMap."""

    def __init__(self):
        self._base = settings.OPENWEATHER_BASE_URL
        self._key = settings.OPENWEATHER_API_KEY
        self._timeout = settings.HTTP_TIMEOUT_SECONDS

    async def get_current_weather(self, city: str) -> WeatherTuple:
        """Fetch and parse current weather data for a given city."""
        validate_api_key(self._key)
        params = {"q": city, "appid": self._key, "units": "metric"}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(self._base, params=params)
            return process_openweather_response(response, city=city)

        except httpx.HTTPStatusError as e:
            raise ConnectionError(
                f"HTTP error from OpenWeather:"
                f" {e.response.status_code} {e.response.text}"
            ) from e

        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to OpenWeather API: {e}") from e

        except (PermissionError, LookupError):
            raise  # propagate known exceptions

        except Exception as e:
            raise RuntimeError(
                f"Unexpected error fetching weather for '{city}': {e}"
            ) from e
