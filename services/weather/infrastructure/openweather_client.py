from __future__ import annotations

import httpx

from services.weather.core import settings
from services.weather.infrastructure.handlers.openweather_handler import (
    ensure_api_key,
    handle_openweather_response,
)


class OpenWeatherClient:
    def __init__(self):
        self._base = settings.OPENWEATHER_BASE_URL
        self._key = settings.OPENWEATHER_API_KEY
        self._timeout = settings.HTTP_TIMEOUT_SECONDS

    async def get_current_min(self, city: str):
        ensure_api_key(self._key)

        params = {"q": city, "appid": self._key, "units": "metric"}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(self._base, params=params)

            return handle_openweather_response(resp, city=city)

        except httpx.HTTPStatusError as e:
            raise ConnectionError(
                f"HTTP error from OpenWeather:"
                f" {e.response.status_code} {e.response.text}"
            ) from e

        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to OpenWeather API: {e}") from e

        except (PermissionError, LookupError):
            raise

        except Exception as e:
            raise RuntimeError(
                f"Unexpected error fetching weather for '{city}': {e}"
            ) from e
