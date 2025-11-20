import argparse
import asyncio

import grpc

from services.weather.core import settings
from services.weather.interfaces.grpc.generated import weather_pb2, weather_pb2_grpc


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    args = parser.parse_args()

    async with grpc.aio.insecure_channel(f"localhost:{settings.GRPC_PORT}") as ch:
        stub = weather_pb2_grpc.WeatherServiceStub(ch)
        md = (("x-api-key", settings.GRPC_API_KEY),) if settings.GRPC_API_KEY else ()

        try:
            resp = await stub.GetCurrentWeather(
                weather_pb2.GetCurrentWeatherRequest(city=args.city), metadata=md
            )
            print(f"Weather for {resp.city}:")
            print(f"  Temperature: {resp.temp_c:.1f} °C")
            print(f"  Humidity:    {resp.humidity}%")
            print(f"  Conditions:  {resp.description}")
            print(f"  Wind Speed:  {resp.wind_speed} m/s")
        except grpc.RpcError as e:
            print(f"[{e.code().name}] {e.details()}")


if __name__ == "__main__":
    asyncio.run(main())
