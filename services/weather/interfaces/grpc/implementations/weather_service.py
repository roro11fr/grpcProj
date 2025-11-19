import grpc

from services.weather.infrastructure.openweather_client import OpenWeatherClient
from services.weather.interfaces.grpc.generated import weather_pb2, weather_pb2_grpc


class WeatherServiceImpl(weather_pb2_grpc.WeatherServiceServicer):
    def __init__(self):
        self.client = OpenWeatherClient()

    async def GetCurrentWeather(self, request, context):
        try:
            name, temp_c, description = await self.client.get_current_min(request.city)
            return weather_pb2.GetCurrentWeatherResponse(
                city=name,
                temp_c=temp_c,
                description=description,
            )
        except PermissionError as e:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except LookupError as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Internal error: {e}")
