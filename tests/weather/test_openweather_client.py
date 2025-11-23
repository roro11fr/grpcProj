import types

import httpx
import pytest

from services.weather.infrastructure.openweather.openweather_client import (
    OpenWeatherClient,
)

pytestmark = pytest.mark.unit


class DummyResponse:
    def __init__(self, json_data=None, status_code=200, text=""):
        self._json = json_data or {}
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "HTTP error",
                request=None,
                response=types.SimpleNamespace(
                    status_code=self.status_code, text=self.text
                ),
            )


@pytest.mark.asyncio
async def test_openweather_client_parses_payload(monkeypatch):
    client = OpenWeatherClient()
    client._key = "TEST_KEY"

    async def fake_get(self, url, params=None):
        return DummyResponse(
            {
                "name": "London",
                "main": {"temp": 18.5, "humidity": 82},
                "weather": [{"description": "light rain"}],
                "wind": {"speed": 4.6},
            },
            status_code=200,
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    name, temp_c, description, humidity, wind_speed = await client.get_current_weather(
        "London"
    )
    assert (
        name,
        round(temp_c, 1),
        description.lower(),
        humidity,
        round(wind_speed, 1),
    ) == ("London", 18.5, "light rain", 82, 4.6)


@pytest.mark.asyncio
async def test_openweather_client_missing_key_raises():
    client = OpenWeatherClient()
    client._key = None
    with pytest.raises(PermissionError):
        await client.get_current_weather("London")


@pytest.mark.asyncio
async def test_openweather_401_maps_to_permission(monkeypatch):
    client = OpenWeatherClient()
    client._key = "TEST_KEY"

    async def fake_get(self, url, params=None):
        return DummyResponse({}, status_code=401, text="unauthorized")

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    with pytest.raises(PermissionError):
        await client.get_current_weather("London")


@pytest.mark.asyncio
async def test_openweather_404_maps_to_lookup(monkeypatch):
    client = OpenWeatherClient()
    client._key = "TEST_KEY"

    async def fake_get(self, url, params=None):
        return DummyResponse({}, status_code=404, text="not found")

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    with pytest.raises(LookupError):
        await client.get_current_weather("NowhereVille")


@pytest.mark.asyncio
async def test_openweather_request_error_maps_to_connection(monkeypatch):
    client = OpenWeatherClient()
    client._key = "TEST_KEY"

    async def fake_get(self, url, params=None):
        raise httpx.RequestError("boom")

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get, raising=True)

    with pytest.raises(ConnectionError):
        await client.get_current_weather("London")
