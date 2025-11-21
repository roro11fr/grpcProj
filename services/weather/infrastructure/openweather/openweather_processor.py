from __future__ import annotations

import httpx

from .openweather_parsers import parse_weather_payload
from .openweather_types import WeatherTuple
from .openweather_validators import verify_response_status


def process_openweather_response(
    response: httpx.Response, *, city: str
) -> WeatherTuple:
    """Validate the HTTP response and parse the JSON payload."""
    verify_response_status(response, city=city)
    data = response.json()
    return parse_weather_payload(data, fallback_city=city)
