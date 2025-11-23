from services.weather.domain.repositories.weather_repository import WeatherRepository
from services.weather.infrastructure.openweather.openweather_client import (
    OpenWeatherClient,
)
from services.weather.interfaces.grpc.generated import weather_pb2_grpc

from .helpers import (
    abort_by_exception,
    fetch_weather,
    persist_reading,
    to_proto,
    validate_city,
)


class WeatherServiceImpl(weather_pb2_grpc.WeatherServiceServicer):
    def __init__(
        self,
        client: OpenWeatherClient | None = None,
        repo: WeatherRepository | None = None,
    ):
        self.client = client or OpenWeatherClient()
        self.repo = repo or WeatherRepository()

    async def GetCurrentWeather(self, request, context):
        try:
            city = validate_city(getattr(request, "city", None))
            name, temp_c, description, humidity, wind_speed = await fetch_weather(
                self.client, city
            )
            persist_reading(self.repo, name, temp_c, description, humidity, wind_speed)
            return to_proto(name, temp_c, description, humidity, wind_speed)
        except Exception as e:
            await abort_by_exception(context, e)
