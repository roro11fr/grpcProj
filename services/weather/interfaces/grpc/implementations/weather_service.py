from services.weather.interfaces.grpc.generated import weather_pb2, weather_pb2_grpc


class WeatherServiceImpl(weather_pb2_grpc.WeatherServiceServicer):
    async def GetCurrentWeather(self, request, context):
        return weather_pb2.GetCurrentWeatherResponse(
            city=request.city, temp_c=20.0, description="Clear"
        )
