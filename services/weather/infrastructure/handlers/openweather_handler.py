from __future__ import annotations

from typing import Any, Dict, Tuple

import httpx


def ensure_api_key(api_key: str | None) -> None:
    """Verify that an API key exists before making any requests."""
    if not api_key:
        raise PermissionError("Missing OPENWEATHER_API_KEY")


def validate_status_code(resp: httpx.Response, *, city: str) -> None:
    """Raise friendly exceptions for common HTTP status codes."""
    if resp.status_code == 401:
        raise PermissionError("Invalid API key")
    if resp.status_code == 404:
        raise LookupError(f"City not found: {city}")
    resp.raise_for_status()


def extract_weather_fields(
    data: Dict[str, Any], *, fallback_city: str
) -> Tuple[str, float, str, int, float]:
    """
    Extract key weather information from the OpenWeather API payload.
    Returns: (city_name, temperature_celsius,
    weather_description, humidity_percent, wind_speed_mps)
    """
    city_name = data.get("name") or fallback_city

    main_info = data.get("main", {})
    temperature_celsius = float(main_info.get("temp", 0.0))
    humidity_percent = int(main_info.get("humidity", 0))

    weather_items = data.get("weather") or []
    first_weather_entry = weather_items[0] if weather_items else {}
    description = str(first_weather_entry.get("description", "Unknown")).capitalize()

    # section: wind data
    wind_info = data.get("wind", {})
    wind_speed_mps = float(wind_info.get("speed", 0.0))

    return city_name, temperature_celsius, description, humidity_percent, wind_speed_mps


def process_openweather_response(
    resp: httpx.Response, *, city: str
) -> Tuple[str, float, str, int, float]:
    """
    Validate response status, parse JSON and extract relevant weather fields.
    """
    validate_status_code(resp, city=city)
    data = resp.json()
    return extract_weather_fields(data, fallback_city=city)
