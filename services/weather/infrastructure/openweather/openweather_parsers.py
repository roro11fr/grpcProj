from __future__ import annotations

from typing import Any, Dict

from .openweather_types import WeatherTuple


def parse_weather_payload(data: Dict[str, Any], *, fallback_city: str) -> WeatherTuple:
    """Extract relevant fields from OpenWeather JSON payload."""
    city_name = data.get("name") or fallback_city

    main = data.get("main", {})
    temp_c = float(main.get("temp", 0.0))
    humidity = int(main.get("humidity", 0))

    weather_items = data.get("weather") or []
    first_entry = weather_items[0] if weather_items else {}
    description = str(first_entry.get("description", "Unknown")).capitalize()

    wind = data.get("wind", {})
    wind_speed = float(wind.get("speed", 0.0))

    return city_name, temp_c, description, humidity, wind_speed
