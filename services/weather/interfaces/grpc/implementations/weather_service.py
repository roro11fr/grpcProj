import grpc

from services.weather.domain.repositories.weather_repository import WeatherRepository
from services.weather.infrastructure.openweather_client import OpenWeatherClient
from services.weather.interfaces.grpc.generated import weather_pb2, weather_pb2_grpc


class WeatherServiceImpl(weather_pb2_grpc.WeatherServiceServicer):
    def __init__(self):
        self.client = OpenWeatherClient()
        self.repo = WeatherRepository()

    async def GetCurrentWeather(self, request, context):
        city = (request.city or "").strip()
        if not city:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "city is required")
        try:
            name, temp_c, description, humidity, wind_speed = (
                await self.client.get_current_weather(city)
            )
            try:
                await self.repo.insert_reading(
                    city=name,
                    temp_c=temp_c,
                    description=description,
                    humidity=humidity,
                    wind_speed=wind_speed,
                )
            except Exception:
                pass
            return weather_pb2.GetCurrentWeatherResponse(
                city=name,
                temp_c=temp_c,
                description=description,
                humidity=humidity,
                wind_speed=wind_speed,
            )
        except PermissionError as e:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except LookupError as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except ConnectionError as e:
            await context.abort(grpc.StatusCode.UNAVAILABLE, str(e))
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Internal error: {e}")
