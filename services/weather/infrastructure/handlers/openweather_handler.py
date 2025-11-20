from __future__ import annotations

from typing import Any, Dict, Tuple

import httpx


def ensure_api_key(api_key: str | None) -> None:
    if not api_key:
        raise PermissionError("Missing OPENWEATHER_API_KEY")


def map_status_or_raise(resp: httpx.Response, *, city: str) -> None:
    if resp.status_code == 401:
        raise PermissionError("Invalid API key")
    if resp.status_code == 404:
        raise LookupError(f"City not found: {city}")
    resp.raise_for_status()


def parse_openweather_payload(
    data: Dict[str, Any], *, fallback_city: str
) -> Tuple[str, float, str, int, float]:
    name = data.get("name") or fallback_city
    main = data.get("main") or {}
    temp_c = float(main.get("temp"))
    humidity = int(main.get("humidity", 0))
    weather_list = data.get("weather") or []
    w0 = weather_list[0] if weather_list else {}
    description = str(w0.get("description", "Unknown")).capitalize()
    wind = data.get("wind") or {}
    wind_speed = float(wind.get("speed", 0.0))
    return (name, temp_c, description, humidity, wind_speed)


def handle_openweather_response(
    resp: httpx.Response, *, city: str
) -> Tuple[str, float, str, int, float]:
    map_status_or_raise(resp, city=city)
    data = resp.json()
    return parse_openweather_payload(data, fallback_city=city)
