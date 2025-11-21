from __future__ import annotations

import httpx


def validate_api_key(api_key: str | None) -> None:
    """Ensure an API key is configured before making requests."""
    if not api_key:
        raise PermissionError("Missing OPENWEATHER_API_KEY")


def verify_response_status(response: httpx.Response, *, city: str) -> None:
    """Raise friendly errors for common OpenWeather HTTP codes."""
    if response.status_code == 401:
        raise PermissionError("Invalid API key")
    if response.status_code == 404:
        raise LookupError(f"City not found: {city}")
    response.raise_for_status()
