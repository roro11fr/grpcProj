import httpx

from services.weather.core import settings


class OpenWeatherClient:
    def __init__(self):
        self._base = settings.OPENWEATHER_BASE_URL
        self._key = settings.OPENWEATHER_API_KEY
        self._timeout = settings.HTTP_TIMEOUT_SECONDS

    async def get_current_min(self, city: str) -> tuple[str, float, str]:

        if not self._key:
            raise PermissionError("Missing OPENWEATHER_API_KEY")

        params = {"q": city, "appid": self._key, "units": "metric"}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.get(self._base, params=params)

        if r.status_code == 401:
            raise PermissionError("Invalid API key")
        if r.status_code == 404:
            raise LookupError(f"City not found: {city}")
        r.raise_for_status()

        data = r.json()
        name = data.get("name", city)
        temp_c = float(data["main"]["temp"])
        description = str(data["weather"][0]["description"]).capitalize()
        return name, temp_c, description
